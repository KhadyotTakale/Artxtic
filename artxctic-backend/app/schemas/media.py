"""Media and generation request/response schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.core.config import settings
from app.services.storage_service import StorageService


# ── Generation ───────────────────────────────────────────────────
class GenerateImageRequest(BaseModel):
    """Request to generate an image via Fal.ai."""
    prompt: str = Field(..., min_length=10, max_length=1000)
    aspect_ratio: Literal["16:9", "9:16", "1:1", "4:3"] = "1:1"
    model: str = "model-1"
    reference_image_url: str | None = None


class GenerateVideoRequest(BaseModel):
    """Request to generate a video via Fal.ai."""
    prompt: str = Field(..., min_length=10, max_length=1000)
    aspect_ratio: Literal["16:9", "9:16", "1:1", "4:3"] = "16:9"
    model: str = "model-1"
    reference_image_url: str | None = None


class GenerationJobResponse(BaseModel):
    """Returned after submitting a generation request."""
    job_id: str
    status: str = "pending"
    message: str = "Generation queued"
    error_message: str | None = None


# ── Media ────────────────────────────────────────────────────────
class MediaResponse(BaseModel):
    """Single media item response."""
    id: str
    type: str
    url: str
    thumbnail_url: str | None = None
    prompt: str
    aspect_ratio: str | None = None
    model_used: str | None = None
    file_size: int | None = None
    width: int | None = None
    height: int | None = None
    duration: float | None = None
    is_starred: bool = False
    created_at: datetime

    @field_validator("url", mode="before")
    @classmethod
    def ensure_presigned_url(cls, v: str) -> str:
        """Ensure the URL is accessible (presigned if private)."""
        if not v:
            return v
        try:
            # If it's a bare key (not a URL), presign it
            if not v.startswith("http"):
                key = v.lstrip("/")
                return StorageService.get_presigned_url(key)

            # If it's a full R2 URL, extract key and presign
            if settings.R2_PUBLIC_URL and v.startswith(settings.R2_PUBLIC_URL):
                key = v[len(settings.R2_PUBLIC_URL):].lstrip("/")
                return StorageService.get_presigned_url(key)

            # Also catch any R2-style URL by domain pattern
            if ".r2.cloudflarestorage.com/" in v:
                key = StorageService.extract_file_key(v)
                return StorageService.get_presigned_url(key)

        except Exception:
            # If presigning fails, return original URL rather than crashing
            pass
        return v

    @field_validator("thumbnail_url", mode="before")
    @classmethod
    def ensure_presigned_thumbnail_url(cls, v: str | None) -> str | None:
        """Ensure thumbnail URL is presigned if it's a private R2 URL."""
        if not v:
            return v
        try:
            if not v.startswith("http"):
                key = v.lstrip("/")
                return StorageService.get_presigned_url(key)

            if settings.R2_PUBLIC_URL and v.startswith(settings.R2_PUBLIC_URL):
                key = v[len(settings.R2_PUBLIC_URL):].lstrip("/")
                return StorageService.get_presigned_url(key)

            if ".r2.cloudflarestorage.com/" in v:
                key = StorageService.extract_file_key(v)
                return StorageService.get_presigned_url(key)
        except Exception:
            pass
        return v

    model_config = {"from_attributes": True}


class GenerationStatusResponse(BaseModel):
    """Status of a generation job."""
    job_id: str
    status: str  # pending, processing, completed, failed
    media: list[MediaResponse] | None = None
    error_message: str | None = None


class MediaDownloadResponse(BaseModel):
    """Presigned download URL response."""
    download_url: str
    expires_in: int  # seconds


# ── Library Filters ──────────────────────────────────────────────
class LibraryFilterParams(BaseModel):
    """Query parameters for library filtering."""
    media_type: Literal["all", "image", "video"] = "all"
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
