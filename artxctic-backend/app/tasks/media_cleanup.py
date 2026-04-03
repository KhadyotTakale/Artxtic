"""Media cleanup cron tasks."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


def _run_async(coro):  # type: ignore[no-untyped-def]
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


async def _cleanup_expired_media() -> int:
    """Delete un-starred media older than 15 days from DB and R2."""
    from sqlalchemy import select, delete, and_
    from app.core.database import async_session_factory
    from app.models.media import Media
    from app.services.storage_service import StorageService

    cutoff = datetime.now(timezone.utc) - timedelta(days=15)
    deleted_count = 0

    async with async_session_factory() as db:
        try:
            # Find expired, un-starred media
            result = await db.execute(
                select(Media).where(
                    and_(
                        Media.is_starred == False,
                        Media.created_at < cutoff,
                    )
                )
            )
            expired_media = result.scalars().all()

            if not expired_media:
                logger.info("No expired media to clean up")
                return 0

            # Collect R2 keys
            r2_keys = []
            media_ids = []
            for media in expired_media:
                media_ids.append(media.id)
                if media.url:
                    key = media.url.split("/", 4)[-1] if "/" in media.url else ""
                    if key:
                        r2_keys.append(key)

            # Delete from R2
            if r2_keys:
                StorageService.delete_files(r2_keys)

            # Delete from DB
            if media_ids:
                await db.execute(
                    delete(Media).where(Media.id.in_(media_ids))
                )
                await db.commit()

            deleted_count = len(media_ids)
            logger.info("Cleaned up %d expired media items", deleted_count)

        except Exception as e:
            logger.error("Cleanup failed: %s", str(e))
            await db.rollback()

    return deleted_count


async def _reset_monthly_usage() -> int:
    """Reset all usage counters on the 1st of each month."""
    from sqlalchemy import update
    from app.core.database import async_session_factory
    from app.models.usage import UsageLimit

    async with async_session_factory() as db:
        try:
            next_reset = datetime.now(timezone.utc) + timedelta(days=30)
            result = await db.execute(
                update(UsageLimit).values(
                    image_count=0,
                    video_count=0,
                    reset_date=next_reset,
                )
            )
            await db.commit()
            count = result.rowcount
            logger.info("Reset usage for %d users", count)
            return count
        except Exception as e:
            logger.error("Usage reset failed: %s", str(e))
            await db.rollback()
            return 0


@celery_app.task
def cleanup_expired_media() -> int:
    """Celery task: clean up expired media."""
    return _run_async(_cleanup_expired_media())


@celery_app.task
def reset_monthly_usage() -> int:
    """Celery task: reset monthly usage counters."""
    return _run_async(_reset_monthly_usage())
