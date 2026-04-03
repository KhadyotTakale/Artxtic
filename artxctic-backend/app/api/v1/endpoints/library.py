"""Library API endpoints (7 endpoints)."""

from __future__ import annotations

import logging
import math
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_verified_user
from app.models.media import Media
from app.models.user import User
from app.schemas.common import PaginatedResponse, SuccessResponse
from app.schemas.media import MediaDownloadResponse, MediaResponse
from app.services.storage_service import StorageService
from app.utils.exceptions import ForbiddenError, NotFoundError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/library", tags=["Library"])

HISTORY_RETENTION_DAYS = 15


def _media_to_response(media: Media) -> MediaResponse:
    return MediaResponse(
        id=str(media.id),
        type=media.type,
        url=media.url,
        thumbnail_url=media.thumbnail_url,
        prompt=media.prompt,
        aspect_ratio=media.aspect_ratio,
        model_used=media.model_used,
        file_size=media.file_size,
        width=media.width,
        height=media.height,
        duration=media.duration,
        is_starred=media.is_starred,
        created_at=media.created_at,
    )


# ── 13. GET /library/starred ────────────────────────────────────
@router.get("/starred")
async def get_starred(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    media_type: str = Query("all", regex="^(all|image|video)$"),
) -> dict:
    """Get paginated starred media."""
    conditions = [Media.user_id == current_user.id, Media.is_starred == True]
    if media_type != "all":
        conditions.append(Media.type == media_type)

    # Count
    count_q = select(func.count()).select_from(Media).where(and_(*conditions))
    total = (await db.execute(count_q)).scalar() or 0

    # Fetch
    query = (
        select(Media)
        .where(and_(*conditions))
        .order_by(Media.updated_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    items = [_media_to_response(m) for m in result.scalars().all()]

    return {
        "success": True,
        "data": [item.model_dump() for item in items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if total else 0,
    }


# ── 14. GET /library/history ────────────────────────────────────
@router.get("/history")
async def get_history(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    media_type: str = Query("all", regex="^(all|image|video)$"),
) -> dict:
    """Get paginated history (last 15 days)."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=HISTORY_RETENTION_DAYS)
    conditions = [Media.user_id == current_user.id, Media.created_at >= cutoff]
    if media_type != "all":
        conditions.append(Media.type == media_type)

    count_q = select(func.count()).select_from(Media).where(and_(*conditions))
    total = (await db.execute(count_q)).scalar() or 0

    query = (
        select(Media)
        .where(and_(*conditions))
        .order_by(Media.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    items = [_media_to_response(m) for m in result.scalars().all()]

    return {
        "success": True,
        "data": [item.model_dump() for item in items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if total else 0,
    }


# ── 15. POST /library/star/{media_id} ───────────────────────────
@router.post("/star/{media_id}", response_model=SuccessResponse)
async def star_media(
    media_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> SuccessResponse:
    """Star a media item."""
    result = await db.execute(select(Media).where(Media.id == int(media_id)))
    media = result.scalar_one_or_none()
    if not media:
        raise NotFoundError("Media")
    if media.user_id != current_user.id:
        raise ForbiddenError()

    media.is_starred = True
    await db.flush()
    return SuccessResponse(message="Media starred")


# ── 16. DELETE /library/star/{media_id} ──────────────────────────
@router.delete("/star/{media_id}", response_model=SuccessResponse)
async def unstar_media(
    media_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> SuccessResponse:
    """Unstar a media item."""
    result = await db.execute(select(Media).where(Media.id == int(media_id)))
    media = result.scalar_one_or_none()
    if not media:
        raise NotFoundError("Media")
    if media.user_id != current_user.id:
        raise ForbiddenError()

    media.is_starred = False
    await db.flush()
    return SuccessResponse(message="Media unstarred")


# ── 17. DELETE /library/{media_id} ───────────────────────────────
@router.delete("/{media_id}", response_model=SuccessResponse)
async def delete_media(
    media_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> SuccessResponse:
    """Delete a media item (from DB and R2)."""
    result = await db.execute(select(Media).where(Media.id == int(media_id)))
    media = result.scalar_one_or_none()
    if not media:
        raise NotFoundError("Media")
    if media.user_id != current_user.id:
        raise ForbiddenError()

    # Delete from R2
    if media.url:
        key = StorageService.extract_file_key(media.url)
        if key:
            StorageService.delete_file(key)

    await db.delete(media)
    await db.flush()
    return SuccessResponse(message="Media deleted")


# ── 18. GET /library/filter ──────────────────────────────────────
@router.get("/filter")
async def filter_library(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
    media_type: str = Query("all", regex="^(all|image|video)$"),
    starred: bool | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> dict:
    """Filter media with multiple criteria."""
    conditions = [Media.user_id == current_user.id]
    if media_type != "all":
        conditions.append(Media.type == media_type)
    if starred is not None:
        conditions.append(Media.is_starred == starred)

    count_q = select(func.count()).select_from(Media).where(and_(*conditions))
    total = (await db.execute(count_q)).scalar() or 0

    query = (
        select(Media)
        .where(and_(*conditions))
        .order_by(Media.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    items = [_media_to_response(m) for m in result.scalars().all()]

    return {
        "success": True,
        "data": [item.model_dump() for item in items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if total else 0,
    }


# ── 19. GET /media/{media_id}/download ───────────────────────────
@router.get("/download/{media_id}", response_model=MediaDownloadResponse)
async def download_media(
    media_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_verified_user)],
) -> MediaDownloadResponse:
    """Get a presigned download URL for a media item."""
    result = await db.execute(select(Media).where(Media.id == int(media_id)))
    media = result.scalar_one_or_none()
    if not media:
        raise NotFoundError("Media")
    if media.user_id != current_user.id:
        raise ForbiddenError()

    # Generate a longer-lived presigned URL for download (24 hours)
    download_url = StorageService.get_presigned_url(media.url, expiration=86400)

    return MediaDownloadResponse(
        download_url=download_url,
        expires_in=86400,
    )
