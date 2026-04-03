
import asyncio
from app.core.database import async_session_factory
from app.api.v1.endpoints.generation import generate_image
from app.schemas.media import GenerateImageRequest
from app.models.user import User
from sqlalchemy import select

async def debug_post():
    async with async_session_factory() as session:
        # Get a user
        result = await session.execute(select(User).limit(1))
        user = result.scalar_one()
        
        request = GenerateImageRequest(
            prompt="A cute baby banana",
            aspect_ratio="1:1",
            model="model-1"
        )
        
        print(f"Testing generation for user {user.id}...")
        try:
            response = await generate_image(request, session, user)
            print("Success!")
            print(response)
        except Exception as e:
            print("Failed!")
            print(e)
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_post())
