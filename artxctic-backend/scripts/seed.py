"""Seed subscription plans into the database."""

import asyncio
import sys
sys.path.insert(0, ".")

# Import all models so relationships resolve
from app.models.user import User  # noqa: F401
from app.models.auth import EmailVerificationToken, PasswordResetToken, RefreshToken  # noqa: F401
from app.models.media import Media  # noqa: F401
from app.models.usage import UsageLimit  # noqa: F401
from app.models.queue import GenerationJob  # noqa: F401
from app.models.audit import AuditLog  # noqa: F401

from app.core.database import async_session_factory
from app.core.snowflake import generate_id
from app.models.subscription import SubscriptionPlan, Subscription  # noqa: F401


PLANS = [
    {
        "name": "Free",
        "price_monthly": None,
        "price_yearly": None,
        "image_limit_monthly": 10,
        "video_limit_monthly": 2,
        "features": {
            "quality": "standard",
            "watermark": True,
            "priority_support": False,
            "api_access": False,
        },
        "is_active": True,
        "dodopayments_plan_id": None,
    },
    {
        "name": "Pro",
        "price_monthly": 9.99,
        "price_yearly": 99.00,
        "image_limit_monthly": 100,
        "video_limit_monthly": 20,
        "features": {
            "quality": "high",
            "watermark": False,
            "priority_support": False,
            "api_access": False,
        },
        "is_active": True,
        "dodopayments_plan_id": "pdt_0NYorELDUamm1LlbxzP3L",
    },
    {
        "name": "Enterprise",
        "price_monthly": 29.99,
        "price_yearly": 299.00,
        "image_limit_monthly": -1,  # Unlimited
        "video_limit_monthly": -1,  # Unlimited
        "features": {
            "quality": "ultra",
            "watermark": False,
            "priority_support": True,
            "api_access": True,
        },
        "is_active": True,
        "dodopayments_plan_id": "pdt_0NYorEOJP8paoCWAh5l3X",
    },
]


async def seed():
    async with async_session_factory() as db:
        for plan_data in PLANS:
            plan = SubscriptionPlan(id=generate_id(), **plan_data)
            db.add(plan)
            print(f"  ✓ Created plan: {plan.name}")
        await db.commit()
    print("\n✅ Seeding complete!")


if __name__ == "__main__":
    print("🌱 Seeding subscription plans...\n")
    asyncio.run(seed())
