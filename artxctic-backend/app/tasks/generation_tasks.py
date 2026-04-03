"""Background Celery tasks for AI media generation via Fal.ai.

Handles:
  - Image generation (submit → poll → download → R2 upload → DB)
  - Video generation (submit → poll → download → R2 upload → DB)
  - Retry logic (max 3 attempts)
  - Timeout handling for long-running jobs
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone

import httpx

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────────
MAX_POLL_SECONDS_IMAGE = 300   # 5 minutes max for image generation
MAX_POLL_SECONDS_VIDEO = 900   # 15 minutes max for video generation
POLL_INTERVAL_SECONDS = 3      # Poll every 3 seconds


def _run_async(coro):  # type: ignore[no-untyped-def]
    """Helper to run async code from sync Celery tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ── Core processing logic ────────────────────────────────────────

async def _poll_until_complete(
    fal_service,
    model_endpoint: str,
    request_id: str,
    status_url: str | None,
    timeout_seconds: int,
) -> dict:
    """Poll Fal.ai until the job completes, fails, or times out.

    Returns the status response dict with ``status`` key.
    Raises ``TimeoutError`` if the job exceeds *timeout_seconds*.
    """
    start = time.monotonic()

    while True:
        elapsed = time.monotonic() - start
        if elapsed >= timeout_seconds:
            raise TimeoutError(
                f"Fal.ai job {request_id} timed out after {timeout_seconds}s"
            )

        status = await fal_service.check_status(
            model_endpoint, request_id, status_url=status_url,
        )
        state = status.get("status", "")

        if state == "COMPLETED":
            return status
        if state in ("FAILED", "ERROR"):
            error_msg = status.get("error", "Generation failed on Fal.ai")
            raise Exception(f"Fal.ai generation failed: {error_msg}")

        # IN_QUEUE or IN_PROGRESS — wait and retry
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


async def _download_file(url: str) -> bytes:
    """Download a file from a URL and return the raw bytes."""
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.content


async def _process_image_result(
    fal_result: dict,
    job_id: int,
    user_id: int,
    prompt: str,
    config: dict,
    fal_request_id: str,
) -> list[int]:
    """Download generated images, upload to R2, and create Media records.

    Returns a list of created Media IDs.
    """
    from sqlalchemy import select
    from app.core.database import async_session_factory
    from app.core.snowflake import generate_id
    from app.models.media import Media
    from app.models.queue import GenerationJob
    from app.services.storage_service import StorageService

    images = fal_result.get("images", [])
    if not images:
        raise Exception("No images returned from Fal.ai")

    media_ids: list[int] = []

    async with async_session_factory() as db:
        try:
            for i, img_data in enumerate(images):
                img_url = img_data.get("url", "")
                if not img_url:
                    continue

                # Download from Fal.ai CDN
                file_bytes = await _download_file(img_url)

                # Upload to Cloudflare R2
                r2_key = f"{user_id}/{job_id}_{i}.png"
                stored_url = StorageService.upload_file(
                    file_bytes, r2_key, "image/png",
                )

                # Create Media record
                now = datetime.now(timezone.utc)
                media = Media(
                    id=generate_id(),
                    user_id=user_id,
                    type="image",
                    url=stored_url,
                    prompt=prompt,
                    aspect_ratio=config.get("aspect_ratio"),
                    model_used=config.get("model"),
                    fal_request_id=fal_request_id,
                    width=img_data.get("width"),
                    height=img_data.get("height"),
                    file_size=len(file_bytes),
                    created_at=now,
                    updated_at=now,
                )
                db.add(media)
                media_ids.append(media.id)

            # Link first media to the job
            if media_ids:
                result = await db.execute(
                    select(GenerationJob).where(GenerationJob.id == job_id)
                )
                job = result.scalar_one_or_none()
                if job:
                    job.media_id = media_ids[0]

            await db.commit()
            logger.info(
                "Stored %d image(s) for job %s", len(media_ids), job_id,
            )
        except Exception:
            await db.rollback()
            raise

    return media_ids


async def _process_video_result(
    fal_result: dict,
    job_id: int,
    user_id: int,
    prompt: str,
    config: dict,
    fal_request_id: str,
) -> int:
    """Download generated video, upload to R2, and create a Media record.

    Returns the created Media ID.
    """
    from sqlalchemy import select
    from app.core.database import async_session_factory
    from app.core.snowflake import generate_id
    from app.models.media import Media
    from app.models.queue import GenerationJob
    from app.services.storage_service import StorageService

    video_data = fal_result.get("video", {})
    video_url = video_data.get("url", "")
    if not video_url:
        raise Exception("No video URL returned from Fal.ai")

    # Download from Fal.ai CDN
    file_bytes = await _download_file(video_url)

    # Upload to Cloudflare R2
    r2_key = f"{user_id}/{job_id}.mp4"
    stored_url = StorageService.upload_file(
        file_bytes, r2_key, "video/mp4",
    )

    async with async_session_factory() as db:
        try:
            now = datetime.now(timezone.utc)
            media = Media(
                id=generate_id(),
                user_id=user_id,
                type="video",
                url=stored_url,
                prompt=prompt,
                aspect_ratio=config.get("aspect_ratio"),
                model_used=config.get("model"),
                fal_request_id=fal_request_id,
                file_size=len(file_bytes),
                created_at=now,
                updated_at=now,
            )
            db.add(media)
            await db.flush()

            # Link media to the job
            result = await db.execute(
                select(GenerationJob).where(GenerationJob.id == job_id)
            )
            job = result.scalar_one_or_none()
            if job:
                job.media_id = media.id

            await db.commit()
            logger.info("Stored video for job %s → media %s", job_id, media.id)
            return media.id
        except Exception:
            await db.rollback()
            raise


async def _process_generation(job_id: int) -> None:
    """Full async pipeline: poll Fal.ai → download → R2 → DB updates."""
    from sqlalchemy import select
    from app.core.database import async_session_factory
    from app.models.queue import GenerationJob
    from app.services.fal_service import FalService, IMAGE_MODELS, VIDEO_MODELS, resolve_image_model, resolve_video_model

    # ── 1. Load the job ──────────────────────────────────────────
    async with async_session_factory() as db:
        result = await db.execute(
            select(GenerationJob).where(GenerationJob.id == job_id)
        )
        job = result.scalar_one_or_none()
        if not job:
            logger.error("Generation job %s not found", job_id)
            return

        if job.status not in ("processing", "pending"):
            logger.info(
                "Job %s has status '%s', skipping", job_id, job.status,
            )
            return

        # Increment attempt counter
        job.attempts += 1
        job.status = "processing"
        await db.commit()

    # Capture job fields for use outside the session
    job_type = job.type
    job_prompt = job.prompt
    job_config = dict(job.config)
    fal_request_id = job.fal_request_id
    user_id = job.user_id
    status_url = job_config.get("status_url")
    response_url = job_config.get("response_url")

    # ── 2. Resolve model endpoint ────────────────────────────────
    model_name = job_config.get("model", "model-1")
    if job_type == "image":
        model_endpoint = resolve_image_model(model_name)
    else:
        model_endpoint = resolve_video_model(model_name)
    logger.info("Job %s: model '%s' → endpoint '%s'", job_id, model_name, model_endpoint)
    timeout = MAX_POLL_SECONDS_IMAGE if job_type == "image" else MAX_POLL_SECONDS_VIDEO

    fal = FalService()

    try:
        # ── 3. Submit to Fal.ai if not yet submitted ─────────────
        if not fal_request_id:
            if job_type == "image":
                submit_result = await fal.submit_image_generation(
                    prompt=job_prompt,
                    model=job_config.get("model", "model-1"),
                    aspect_ratio=job_config.get("aspect_ratio", "1:1"),
                    reference_image_url=job_config.get("reference_image_url"),
                )
            else:
                submit_result = await fal.submit_video_generation(
                    prompt=job_prompt,
                    model=job_config.get("model", "model-1"),
                    aspect_ratio=job_config.get("aspect_ratio", "16:9"),
                    reference_image_url=job_config.get("reference_image_url"),
                )

            fal_request_id = submit_result.get("request_id")
            status_url = submit_result.get("status_url")
            response_url = submit_result.get("response_url")

            # Persist the request ID and URLs
            async with async_session_factory() as db:
                result = await db.execute(
                    select(GenerationJob).where(GenerationJob.id == job_id)
                )
                job_row = result.scalar_one()
                job_row.fal_request_id = fal_request_id
                updated_config = dict(job_row.config)
                if status_url:
                    updated_config["status_url"] = status_url
                if response_url:
                    updated_config["response_url"] = response_url
                job_row.config = updated_config
                await db.commit()

            logger.info(
                "Submitted %s job %s → fal request %s",
                job_type, job_id, fal_request_id,
            )

        # ── 4. Poll until complete ───────────────────────────────
        await _poll_until_complete(
            fal, model_endpoint, fal_request_id, status_url, timeout,
        )

        # ── 5. Fetch the full result ─────────────────────────────
        fal_result = await fal.get_result(
            model_endpoint, fal_request_id, response_url=response_url,
        )

        # Guard: check for error in result — do NOT process errors as media
        if "error" in fal_result or "detail" in fal_result:
            error_msg = fal_result.get("error") or fal_result.get("detail", "Unknown error")
            raise Exception(f"Fal.ai returned error in result: {error_msg}")

        # ── 6. Download, upload to R2, and create Media records ──
        if job_type == "image":
            await _process_image_result(
                fal_result, job_id, user_id, job_prompt, job_config, fal_request_id,
            )
        else:
            await _process_video_result(
                fal_result, job_id, user_id, job_prompt, job_config, fal_request_id,
            )

        # ── 7. Mark job as completed ─────────────────────────────
        async with async_session_factory() as db:
            result = await db.execute(
                select(GenerationJob).where(GenerationJob.id == job_id)
            )
            job_row = result.scalar_one()
            job_row.status = "completed"
            job_row.error_message = None
            await db.commit()

        logger.info("Job %s completed successfully", job_id)

    except Exception as e:
        # ── Mark job as failed ───────────────────────────────────
        error_msg = str(e)[:500]  # Truncate very long errors
        logger.error("Job %s failed: %s", job_id, error_msg)

        async with async_session_factory() as db:
            result = await db.execute(
                select(GenerationJob).where(GenerationJob.id == job_id)
            )
            job_row = result.scalar_one_or_none()
            if job_row:
                job_row.status = "failed"
                job_row.error_message = error_msg
                await db.commit()

        # Re-raise so Celery can handle retries
        raise


# ══════════════════════════════════════════════════════════════════
# Public Celery Tasks
# ══════════════════════════════════════════════════════════════════

@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=30,
    acks_late=True,
    name="app.tasks.generation_tasks.process_generation",
)
def process_generation(self, job_id: int) -> None:  # type: ignore[no-untyped-def]
    """Process a single generation job (image or video).

    This is the main entry point called after a job is submitted via the
    API. It handles the full lifecycle: poll Fal.ai → download result →
    upload to R2 → create Media record → update GenerationJob status.

    Args:
        job_id: The ``GenerationJob.id`` to process.
    """
    try:
        _run_async(_process_generation(job_id))
    except Exception as exc:
        logger.error(
            "Task process_generation failed for job %s (attempt %d/%d): %s",
            job_id, self.request.retries + 1, self.max_retries + 1, str(exc),
        )
        # Retry with exponential back-off: 30s, 60s, 120s
        retry_delay = 30 * (2 ** self.request.retries)
        try:
            self.retry(exc=exc, countdown=retry_delay)
        except self.MaxRetriesExceededError:
            logger.error(
                "Job %s permanently failed after %d retries",
                job_id, self.max_retries,
            )


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=30,
    acks_late=True,
    name="app.tasks.generation_tasks.process_image_generation",
)
def process_image_generation(self, job_id: int) -> None:  # type: ignore[no-untyped-def]
    """Convenience alias: process an image generation job.

    Delegates to :func:`process_generation`.
    """
    process_generation(job_id)


@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=30,
    acks_late=True,
    name="app.tasks.generation_tasks.process_video_generation",
)
def process_video_generation(self, job_id: int) -> None:  # type: ignore[no-untyped-def]
    """Convenience alias: process a video generation job.

    Delegates to :func:`process_generation`.
    """
    process_generation(job_id)
