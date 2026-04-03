"""Usage limit tracking and enforcement service."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.snowflake import generate_id
from app.models.subscription import Subscription, SubscriptionPlan
from app.models.usage import UsageLimit
from app.utils.exceptions import UsageLimitExceeded

logger = logging.getLogger(__name__)

# Default free tier limits
FREE_IMAGE_LIMIT = 10
FREE_VIDEO_LIMIT = 2


class UsageService:
    """Track and enforce monthly generation limits."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_or_create_usage(self, user_id: int) -> UsageLimit:
        """Get or create usage limit record for a user."""
        result = await self.db.execute(
            select(UsageLimit).where(UsageLimit.user_id == user_id)
        )
        usage = result.scalar_one_or_none()

        if not usage:
            now = datetime.now(timezone.utc)
            next_month = now + relativedelta(months=1, day=1)
            usage = UsageLimit(
                id=generate_id(),
                user_id=user_id,
                image_count=0,
                video_count=0,
                reset_date=next_month,
            )
            self.db.add(usage)
            await self.db.flush()

        # Check if we need to reset
        if datetime.now(timezone.utc) >= usage.reset_date:
            usage.image_count = 0
            usage.video_count = 0
            now = datetime.now(timezone.utc)
            usage.reset_date = now + relativedelta(months=1, day=1)
            await self.db.flush()

        return usage

    async def get_limits_for_user(self, user_id: int) -> tuple[int, int]:
        """Get (image_limit, video_limit) for a user based on their subscription."""
        result = await self.db.execute(
            select(Subscription)
            .where(Subscription.user_id == user_id, Subscription.status == "active")
            .order_by(Subscription.created_at.desc())
        )
        subscription = result.scalar_one_or_none()

        if not subscription or not subscription.plan_id:
            return FREE_IMAGE_LIMIT, FREE_VIDEO_LIMIT

        result = await self.db.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.id == subscription.plan_id)
        )
        plan = result.scalar_one_or_none()

        if not plan:
            return FREE_IMAGE_LIMIT, FREE_VIDEO_LIMIT

        return plan.image_limit_monthly, plan.video_limit_monthly

    async def check_and_increment(self, user_id: int, media_type: str) -> None:
        """Check if the user can generate, and increment their usage.

        Raises UsageLimitExceeded if the limit is reached.
        -1 means unlimited (no limit check).
        """
        usage = await self.get_or_create_usage(user_id)
        image_limit, video_limit = await self.get_limits_for_user(user_id)

        if media_type == "image":
            # -1 means unlimited
            if image_limit >= 0 and usage.image_count >= image_limit:
                raise UsageLimitExceeded("image")
            usage.image_count += 1
        elif media_type == "video":
            # -1 means unlimited
            if video_limit >= 0 and usage.video_count >= video_limit:
                raise UsageLimitExceeded("video")
            usage.video_count += 1

        await self.db.flush()
        logger.info(
            "Usage updated for user %d: images=%d/%s videos=%d/%s",
            user_id,
            usage.image_count,
            "∞" if image_limit < 0 else str(image_limit),
            usage.video_count,
            "∞" if video_limit < 0 else str(video_limit),
        )

    async def reset_monthly_usage(self, user_id: int) -> None:
        """Reset usage counts to 0 and advance the reset date.

        Called when a subscription renews.
        """
        usage = await self.get_or_create_usage(user_id)
        usage.image_count = 0
        usage.video_count = 0
        now = datetime.now(timezone.utc)
        usage.reset_date = now + relativedelta(months=1, day=1)
        await self.db.flush()
        logger.info("Usage reset for user %d", user_id)

    async def initialize_usage(
        self,
        user_id: int,
        subscription_id: int | None = None,
    ) -> UsageLimit:
        """Initialize or reset usage limits when a subscription is created.

        Links the usage record to the subscription if provided.
        """
        usage = await self.get_or_create_usage(user_id)
        usage.image_count = 0
        usage.video_count = 0
        usage.subscription_id = subscription_id
        now = datetime.now(timezone.utc)
        usage.reset_date = now + relativedelta(months=1, day=1)
        await self.db.flush()
        logger.info("Usage initialized for user %d (sub=%s)", user_id, subscription_id)
        return usage
