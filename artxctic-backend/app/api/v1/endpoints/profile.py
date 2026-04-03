"""User profile API endpoints (3 endpoints)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.subscription import Subscription, SubscriptionPlan
from app.models.usage import UsageLimit
from app.models.user import User
from app.schemas.common import SuccessResponse
from app.schemas.user import UpdateProfileRequest, UserProfileResponse, UserSubscriptionResponse

router = APIRouter(prefix="/user", tags=["User Profile"])


# ── 20. GET /user/profile ───────────────────────────────────────
@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserProfileResponse:
    """Get the current user's profile."""
    # Determine plan name
    plan_name = "free"
    result = await db.execute(
        select(Subscription)
        .where(Subscription.user_id == current_user.id, Subscription.status == "active")
        .order_by(Subscription.created_at.desc())
    )
    subscription = result.scalar_one_or_none()
    if subscription and subscription.plan_id:
        plan_result = await db.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.id == subscription.plan_id)
        )
        plan = plan_result.scalar_one_or_none()
        if plan:
            plan_name = plan.name.lower()

    return UserProfileResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        country=current_user.country,
        is_verified=current_user.is_verified,
        oauth_provider=current_user.oauth_provider,
        plan=plan_name,
        created_at=current_user.created_at,
    )


# ── 21. PUT /user/profile ───────────────────────────────────────
@router.put("/profile", response_model=SuccessResponse)
async def update_profile(
    body: UpdateProfileRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SuccessResponse:
    """Update user profile (name, country)."""
    if body.name is not None:
        current_user.name = body.name
    if body.country is not None:
        current_user.country = body.country

    await db.flush()
    return SuccessResponse(message="Profile updated successfully")


# ── 22. GET /user/subscription ───────────────────────────────────
@router.get("/subscription", response_model=UserSubscriptionResponse)
async def get_subscription(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserSubscriptionResponse:
    """Get user's subscription details and usage."""
    # Get active subscription
    result = await db.execute(
        select(Subscription)
        .where(Subscription.user_id == current_user.id, Subscription.status == "active")
        .order_by(Subscription.created_at.desc())
    )
    subscription = result.scalar_one_or_none()

    plan_name = "Free"
    image_limit = 10
    video_limit = 0
    current_period_end = None
    cancel_at_period_end = False

    if subscription and subscription.plan_id:
        plan_result = await db.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.id == subscription.plan_id)
        )
        plan = plan_result.scalar_one_or_none()
        if plan:
            plan_name = plan.name
            image_limit = plan.image_limit_monthly
            video_limit = plan.video_limit_monthly
        current_period_end = subscription.current_period_end
        cancel_at_period_end = subscription.cancel_at_period_end

    # Get usage
    usage_result = await db.execute(
        select(UsageLimit).where(UsageLimit.user_id == current_user.id)
    )
    usage = usage_result.scalar_one_or_none()
    images_used = usage.image_count if usage else 0
    videos_used = usage.video_count if usage else 0

    return UserSubscriptionResponse(
        plan_name=plan_name,
        status=subscription.status if subscription else "active",
        image_limit=image_limit,
        video_limit=video_limit,
        images_used=images_used,
        videos_used=videos_used,
        current_period_end=current_period_end,
        cancel_at_period_end=cancel_at_period_end,
    )
