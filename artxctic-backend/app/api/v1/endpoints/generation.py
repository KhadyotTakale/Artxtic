"""Generation API endpoints (3 endpoints)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_verified_user
from app.core.snowflake import generate_id
from app.models.queue import GenerationJob
from app.models.media import Media
from app.models.user import User
from app.schemas.media import (
    GenerateImageRequest,
    GenerateVideoRequest,
    GenerationJobResponse,
    GenerationStatusResponse,
    MediaResponse,
)
from app.services.fal_service import FalService, IMAGE_MODELS, VIDEO_MODELS, resolve_image_model, resolve_video_model
from app.services.storage_service import StorageService
from app.services.usage_service import UsageService
from app.utils.exceptions import NotFoundError, ForbiddenError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/generate", tags=["Generation"])


# ── 10. POST /generate/image ────────────────────────────────────
@router.post("/image", response_model=GenerationJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def generate_image(
    body: GenerateImageRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> GenerationJobResponse:
    """Submit an image generation request."""
    logger.info("Received image request - model: %s, prompt: %s", body.model, body.prompt[:50])
    # Check usage limits
    usage_service = UsageService(db)
    await usage_service.check_and_increment(current_user.id, "image")

    # Create job record
    job = GenerationJob(
        id=generate_id(),
        user_id=current_user.id,
        type="image",
        prompt=body.prompt,
        config={
            "aspect_ratio": body.aspect_ratio,
            "model": body.model,
            "reference_image_url": body.reference_image_url,
        },
        status="pending",
    )
    db.add(job)
    await db.flush()

    # Submit to Fal.ai (async)
    try:
        fal = FalService()
        result = await fal.submit_image_generation(
            prompt=body.prompt,
            model=body.model,
            aspect_ratio=body.aspect_ratio,
            reference_image_url=body.reference_image_url,
        )
        job.status = "processing"
        job.fal_request_id = result.get("request_id")
        # Store status_url if available to avoid 405 errors
        # Store status_url and response_url if available
        new_config = dict(job.config)
        if "status_url" in result:
            new_config["status_url"] = result.get("status_url")
        if "response_url" in result:
            new_config["response_url"] = result.get("response_url")
        job.config = new_config
        
        await db.flush()
    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        await db.flush()
        logger.error("Image generation failed: %s", str(e))

    return GenerationJobResponse(
        job_id=str(job.id),
        status=job.status,
        message="Image generation submitted" if job.status != "failed" else "Generation failed",
        error_message=job.error_message if job.status == "failed" else None,
    )


# ── 11. POST /generate/video ────────────────────────────────────
@router.post("/video", response_model=GenerationJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def generate_video(
    body: GenerateVideoRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> GenerationJobResponse:
    """Submit a video generation request."""
    logger.info("Received video request - model: %s, prompt: %s", body.model, body.prompt[:50])
    usage_service = UsageService(db)
    await usage_service.check_and_increment(current_user.id, "video")

    job = GenerationJob(
        id=generate_id(),
        user_id=current_user.id,
        type="video",
        prompt=body.prompt,
        config={
            "aspect_ratio": body.aspect_ratio,
            "model": body.model,
            "reference_image_url": body.reference_image_url,
        },
        status="pending",
    )
    db.add(job)
    await db.flush()

    try:
        fal = FalService()
        result = await fal.submit_video_generation(
            prompt=body.prompt,
            model=body.model,
            aspect_ratio=body.aspect_ratio,
            reference_image_url=body.reference_image_url,
        )
        job.status = "processing"
        job.fal_request_id = result.get("request_id")
        # Store status_url if available
        # Store status_url and response_url if available
        new_config = dict(job.config)
        if "status_url" in result:
            new_config["status_url"] = result.get("status_url")
        if "response_url" in result:
            new_config["response_url"] = result.get("response_url")
        job.config = new_config

        await db.flush()
    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        await db.flush()
        logger.error("Video generation failed: %s", str(e))

    return GenerationJobResponse(
        job_id=str(job.id),
        status=job.status,
        message="Video generation submitted" if job.status != "failed" else "Generation failed",
        error_message=job.error_message if job.status == "failed" else None,
    )


# ── 12. GET /generate/status/{job_id} ───────────────────────────
@router.get("/status/{job_id}", response_model=GenerationStatusResponse)
async def get_generation_status(
    job_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> GenerationStatusResponse:
    """Poll the status of a generation job."""
    result = await db.execute(
        select(GenerationJob).where(GenerationJob.id == int(job_id))
    )
    job = result.scalar_one_or_none()

    if not job:
        raise NotFoundError("Generation job")
    if job.user_id != current_user.id:
        raise ForbiddenError("You don't have access to this job")

    # If job is processing and has a Fal request ID, check Fal.ai status
    if job.status == "processing" and job.fal_request_id:
        try:
            fal = FalService()
            model_name = job.config.get("model", "model-1")
            if job.type == "image":
                model_endpoint = resolve_image_model(model_name)
            else:
                model_endpoint = resolve_video_model(model_name)

            fal_status = await fal.check_status(
                model_endpoint, 
                job.fal_request_id,
                status_url=job.config.get("status_url")
            )
            fal_state = fal_status.get("status", "")

            if fal_state == "COMPLETED":
                # Optimistic locking: try to set status to 'uploading'
                # Only proceed if we successfully updated the row
                stmt = (
                    update(GenerationJob)
                    .where(GenerationJob.id == job.id)
                    .where(GenerationJob.status == "processing")
                    .values(status="uploading")
                )
                result_proxy = await db.execute(stmt)
                await db.commit()  # Commit immediately to release lock/make visible

                if result_proxy.rowcount == 0:
                    # Another request beat us to it, or status changed
                    # Refresh job to get current state
                    await db.refresh(job)
                else:
                    # We won the race, proceed with upload
                    try:
                        # Fetch result and store
                        fal_result = await fal.get_result(
                            model_endpoint, 
                            job.fal_request_id,
                            response_url=job.config.get("response_url")
                        )

                        # Guard: check for error in result — do NOT save errors as media
                        if "error" in fal_result or "detail" in fal_result:
                            error_msg = fal_result.get("error") or fal_result.get("detail", "Unknown error")
                            logger.error("Fal.ai returned error in result: %s", error_msg)
                            job.status = "failed"
                            job.error_message = f"Fal.ai error: {str(error_msg)[:500]}"
                            await db.flush()
                            return GenerationStatusResponse(
                                job_id=str(job.id),
                                status="failed",
                                error_message=job.error_message,
                            )

                        # Download and upload to R2
                        import httpx
                        media_response = None

                        if job.type == "image":
                            images = fal_result.get("images", [])
                            for i, img_data in enumerate(images):
                                img_url = img_data.get("url", "")
                                if img_url:
                                    async with httpx.AsyncClient() as client:
                                        resp = await client.get(img_url)
                                        file_bytes = resp.content

                                    r2_key = f"{current_user.id}/{job.id}_{i}.png"
                                    stored_url = StorageService.upload_file(
                                        file_bytes, r2_key, "image/png"
                                    )

                                    now = datetime.now(timezone.utc)
                                    media = Media(
                                        id=generate_id(),
                                        user_id=current_user.id,
                                        type="image",
                                        url=stored_url,
                                        prompt=job.prompt,
                                        aspect_ratio=job.config.get("aspect_ratio"),
                                        model_used=job.config.get("model"),
                                        fal_request_id=job.fal_request_id,
                                        width=img_data.get("width"),
                                        height=img_data.get("height"),
                                        file_size=len(file_bytes),
                                        created_at=now,
                                        updated_at=now,
                                    )
                                    db.add(media)
                                    if i == 0:
                                        job.media_id = media.id
                                        media_response = MediaResponse(
                                            id=str(media.id),
                                            type=media.type,
                                            url=media.url,
                                            prompt=media.prompt,
                                            aspect_ratio=media.aspect_ratio,
                                            model_used=media.model_used,
                                            width=media.width,
                                            height=media.height,
                                            file_size=media.file_size,
                                            created_at=now,
                                        )
                        else:
                            # Video result
                            video_data = fal_result.get("video", {})
                            video_url = video_data.get("url", "")
                            if video_url:
                                async with httpx.AsyncClient() as client:
                                    resp = await client.get(video_url)
                                    file_bytes = resp.content

                                r2_key = f"{current_user.id}/{job.id}.mp4"
                                stored_url = StorageService.upload_file(
                                    file_bytes, r2_key, "video/mp4"
                                )

                                now = datetime.now(timezone.utc)
                                media = Media(
                                    id=generate_id(),
                                    user_id=current_user.id,
                                    type="video",
                                    url=stored_url,
                                    prompt=job.prompt,
                                    aspect_ratio=job.config.get("aspect_ratio"),
                                    model_used=job.config.get("model"),
                                    fal_request_id=job.fal_request_id,
                                    file_size=len(file_bytes),
                                    created_at=now,
                                    updated_at=now,
                                )
                                db.add(media)
                                job.media_id = media.id
                                media_response = MediaResponse(
                                    id=str(media.id),
                                    type=media.type,
                                    url=media.url,
                                    prompt=media.prompt,
                                    aspect_ratio=media.aspect_ratio,
                                    model_used=media.model_used,
                                    file_size=media.file_size,
                                    created_at=now,
                                )

                        job.status = "completed"
                        await db.flush()

                        return GenerationStatusResponse(
                            job_id=str(job.id),
                            status="completed",
                            media=[media_response] if media_response else None,
                        )

                    except Exception as e:
                        # If something went wrong during upload, revert status so it can be retried 
                        # OR mark as failed. Mark as failed is safer to avoid loops.
                        logger.error("Error processing completion: %s", str(e))
                        job.status = "failed"
                        job.error_message = f"Processing failed: {str(e)}"
                        await db.flush()
                        
            elif fal_state in ("FAILED", "ERROR"):
                job.status = "failed"
                job.error_message = fal_status.get("error", "Generation failed")
                await db.flush()

        except Exception as e:
            logger.error("Status check error: %s", str(e))
            job.status = "failed"
            job.error_message = f"Status check failed: {str(e)}"
            await db.flush()

    # Return current status
    media_response_list = []
    if job.fal_request_id:
        result = await db.execute(select(Media).where(Media.fal_request_id == job.fal_request_id))
        media_items = result.scalars().all()
        for media in media_items:
            media_response_list.append(
                MediaResponse(
                    id=str(media.id),
                    type=media.type,
                    url=media.url,
                    prompt=media.prompt,
                    aspect_ratio=media.aspect_ratio,
                    model_used=media.model_used,
                    width=media.width,
                    height=media.height,
                    file_size=media.file_size,
                    duration=media.duration,
                    is_starred=media.is_starred,
                    created_at=media.created_at,
                )
            )

    return GenerationStatusResponse(
        job_id=str(job.id),
        status=job.status,
        media=media_response_list if media_response_list else None,
        error_message=job.error_message,
    )
