"""User profile request/response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field
import re


class UserProfileResponse(BaseModel):
    """Full user profile."""
    id: str
    email: str
    name: str | None = None
    country: str | None = None
    is_verified: bool
    oauth_provider: str | None = None
    plan: str = "free"
    created_at: datetime

    model_config = {"from_attributes": True}


class UpdateProfileRequest(BaseModel):
    """Update user profile fields."""
    name: str | None = Field(None, min_length=2, max_length=100)
    country: str | None = Field(None, max_length=100)

    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is not None and not re.match(r"^[a-zA-Z\s\-]+$", v):
            raise ValueError("Name can only contain letters, spaces, and hyphens")
        return v.strip() if v else v


class UserSubscriptionResponse(BaseModel):
    """User's subscription details."""
    plan_name: str = "Free"
    status: str = "active"
    image_limit: int = 10
    video_limit: int = 0
    images_used: int = 0
    videos_used: int = 0
    current_period_end: datetime | None = None
    cancel_at_period_end: bool = False
