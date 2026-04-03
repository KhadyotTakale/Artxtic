import asyncio
from sqlalchemy import select
from app.core.database import async_session_factory
from app.models.user import User
from app.models.subscription import Subscription
from app.models.media import Media
from app.models.usage import UsageLimit

async def check_users():
    async with async_session_factory() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"Found {len(users)} users:")
        for user in users:
            # Get usage
            usage_result = await session.execute(
                select(UsageLimit).where(UsageLimit.user_id == user.id)
            )
            usage = usage_result.scalar_one_or_none()
            usage_str = f"Images: {usage.image_count}, Videos: {usage.video_count}" if usage else "No usage record"
            print(f"ID: {user.id}, Email: {user.email}, Name: {user.name}, Verified: {user.is_verified}, Active: {user.is_active}, Usage: {usage_str}")

if __name__ == "__main__":
    asyncio.run(check_users())
