
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator
from typing import Literal

# Mock settings and StorageService
class Settings:
    R2_PUBLIC_URL = "https://r2.example.com"
settings = Settings()

class StorageService:
    @staticmethod
    def get_presigned_url(key):
        return f"https://presigned.example.com/{key}"

# Copied schemas
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
    created_at: datetime  # Defined twice in the original file, checking if that matters

    # created_at: datetime # The original file had this duplicate line

    @field_validator("url", mode="before")
    @classmethod
    def ensure_presigned_url(cls, v: str) -> str:
        if v and (not v.startswith("http") or (settings.R2_PUBLIC_URL and v.startswith(settings.R2_PUBLIC_URL))):
            if v.startswith("/"):
                key = v.lstrip("/")
                return StorageService.get_presigned_url(key)
            if settings.R2_PUBLIC_URL and v.startswith(settings.R2_PUBLIC_URL):
                 key = v[len(settings.R2_PUBLIC_URL):].lstrip("/")
                 return StorageService.get_presigned_url(key)
        return v

    model_config = {"from_attributes": True}

class GenerationStatusResponse(BaseModel):
    """Status of a generation job."""
    job_id: str
    status: str
    media: list[MediaResponse] | None = None
    error_message: str | None = None

# Test
def test_validation():
    now = datetime.now(timezone.utc)
    media_item = MediaResponse(
        id="123",
        type="image",
        url="https://r2.example.com/test.png",
        prompt="test prompt",
        aspect_ratio="1:1",
        created_at=now
    )
    
    print(f"Created MediaResponse: {media_item}")
    print(f"Type of media_item: {type(media_item)}")
    
    # Simulate the list construction
    media_list = [media_item]
    
    try:
        response = GenerationStatusResponse(
            job_id="job_123",
            status="completed",
            media=media_list
        )
        print("Validation SUCCESS")
        print(response.model_dump())
    except Exception as e:
        print("Validation FAILED")
        print(e)

if __name__ == "__main__":
    test_validation()
