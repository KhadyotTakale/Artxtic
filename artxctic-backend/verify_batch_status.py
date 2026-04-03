
import asyncio
import sys
from app.core.database import async_session_factory
from app.api.v1.endpoints.generation import get_generation_status
from app.models.user import User

# Mock user and request
async def verify():
    # We need a valid job_id. Let's pick one from recent logs if possible, or just fail gracefully.
    # Actually, let's just create a dummy job and media in DB to test the function logic? 
    # Or better, just check the code again. 
    # A script is better. I'll search for the most recent job ID from the DB.
    
    from sqlalchemy import select, desc
    from app.models.queue import GenerationJob
    
    async with async_session_factory() as session:
        # Get latest job
        result = await session.execute(select(GenerationJob).order_by(desc(GenerationJob.created_at)).limit(1))
        job = result.scalar_one_or_none()
        
        if not job:
            print("No jobs found to test.")
            return

        print(f"Testing with Job ID: {job.id}")
        
        # Get user for this job to mock auth
        user_result = await session.execute(select(User).where(User.id == job.user_id))
        user = user_result.scalar_one_or_none()
        
        try:
            response = await get_generation_status(str(job.id), session, user)
            print(f"Status: {response.status}")
            if response.media:
                print(f"Media count: {len(response.media)}")
                print(f"Media type: {type(response.media)}")
                if isinstance(response.media, list):
                     print("SUCCESS: Media is a list.")
                else:
                     print("FAILURE: Media is NOT a list.")
                     
                for m in response.media:
                    print(f" - Media ID: {m.id}, URL: {m.url[:50]}...")
            else:
                print("No media returned (job might be failed or pending).")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
