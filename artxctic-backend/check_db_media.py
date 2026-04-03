
import asyncio
from sqlalchemy import text
from app.core.database import async_session_factory

async def check_media():
    user_id = 280172431551893504
    async with async_session_factory() as session:
        # Check media count
        result = await session.execute(text("SELECT count(*) FROM media WHERE user_id = :uid"), {"uid": user_id})
        count = result.scalar()
        print(f"Media count for user {user_id}: {count}")
        
        # Check recent media
        result = await session.execute(text("SELECT id, created_at, url FROM media WHERE user_id = :uid ORDER BY created_at DESC LIMIT 5"), {"uid": user_id})
        rows = result.fetchall()
        print("Recent media:")
        for row in rows:
            print(f"ID: {row[0]}, Created: {row[1]}, URL: {row[2]}")

if __name__ == "__main__":
    asyncio.run(check_media())
