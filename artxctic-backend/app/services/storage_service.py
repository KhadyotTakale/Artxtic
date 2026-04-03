"""Cloudflare R2 storage service (S3-compatible).

Provides file upload, download, presigned URL generation, and deletion
for private R2 buckets.
"""

from __future__ import annotations

import logging
from io import BytesIO
from typing import Any

import boto3
import httpx
from boto3.s3.transfer import TransferConfig
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError

from app.core.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """Cloudflare R2 file operations via S3-compatible API."""

    _client = None

    @classmethod
    def _get_client(cls) -> Any:
        """Lazy-init the S3 client (not async, but boto3 is I/O-fast for presigned ops)."""
        if cls._client is None:
            cls._client = boto3.client(
                "s3",
                endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
                region_name="auto",
                config=BotoConfig(
                    signature_version="s3v4",
                    retries={"max_attempts": 3, "mode": "standard"},
                ),
            )
        return cls._client

    # ── Key Extraction ───────────────────────────────────────────

    @classmethod
    def extract_file_key(cls, url_or_key: str) -> str:
        """Extract file key from a full R2 URL or return as-is if already a key.

        Input:  https://xxx.r2.cloudflarestorage.com/user_id/file.mp4
        Output: user_id/file.mp4

        Input:  user_id/file.mp4
        Output: user_id/file.mp4
        """
        if not url_or_key:
            return url_or_key
        if ".r2.cloudflarestorage.com/" in url_or_key:
            return url_or_key.split(".r2.cloudflarestorage.com/", 1)[1]
        # Remove leading slash if present
        return url_or_key.lstrip("/")

    @classmethod
    def build_file_key(cls, user_id: int, media_id: int, media_type: str) -> str:
        """Build consistent file key: {user_id}/{media_id}.{ext}"""
        extension = "mp4" if media_type == "video" else "png"
        return f"{user_id}/{media_id}.{extension}"

    @classmethod
    def get_content_type(cls, media_type: str) -> str:
        """Get correct content type for media."""
        return "video/mp4" if media_type == "video" else "image/png"

    # ── Upload ───────────────────────────────────────────────────

    @classmethod
    def upload_file(
        cls,
        file_bytes: bytes,
        key: str,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Upload a file to R2 and return the stored URL (private)."""
        client = cls._get_client()
        # Use a high multipart threshold to prevent chunked uploads.
        # R2 doesn't support the streaming payload signature used in
        # multipart transfers, causing SignatureDoesNotMatch errors
        # on large files (e.g. videos).
        transfer_config = TransferConfig(
            multipart_threshold=200 * 1024 * 1024,  # 200 MB
        )
        client.upload_fileobj(
            BytesIO(file_bytes),
            settings.R2_BUCKET_NAME,
            key,
            ExtraArgs={"ContentType": content_type},
            Config=transfer_config,
        )
        url = f"{settings.R2_PUBLIC_URL}/{key}"
        logger.info("Uploaded file: %s (%d bytes)", key, len(file_bytes))
        return url

    @classmethod
    async def upload_from_url(
        cls,
        source_url: str,
        file_key: str,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Download a file from an external URL and upload to R2.

        Returns the stored R2 URL (private — use get_presigned_url to serve).
        """
        logger.info("Downloading from: %s", source_url)
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.get(source_url)
            response.raise_for_status()
            file_bytes = response.content

            # Auto-detect content type from response headers
            detected_type = response.headers.get("content-type", content_type)
            if "video" in detected_type or source_url.endswith(".mp4"):
                content_type = "video/mp4"
            elif "image" in detected_type:
                content_type = detected_type.split(";")[0]

        logger.info("Downloaded %d bytes, uploading to R2 as %s", len(file_bytes), file_key)
        return cls.upload_file(file_bytes, file_key, content_type)

    # ── Presigned URLs ───────────────────────────────────────────

    @classmethod
    def get_presigned_url(cls, key_or_url: str, expiration: int | None = None) -> str:
        """Generate a presigned download URL.

        Accepts either a bare key or a full R2 URL — key will be extracted
        automatically if a URL is passed.
        """
        client = cls._get_client()
        key = cls.extract_file_key(key_or_url)
        url = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.R2_BUCKET_NAME, "Key": key},
            ExpiresIn=expiration or settings.PRESIGNED_URL_EXPIRATION,
        )
        return url

    @classmethod
    def get_presigned_url_safe(
        cls,
        key_or_url: str | None,
        expiration: int | None = None,
    ) -> str | None:
        """Safe version that returns None instead of raising on None input.

        Use this for nullable fields like thumbnail_url.
        """
        if not key_or_url:
            return None
        try:
            return cls.get_presigned_url(key_or_url, expiration)
        except Exception as e:
            logger.warning("Could not generate presigned URL for %s: %s", key_or_url, e)
            return None

    # ── Delete ───────────────────────────────────────────────────

    @classmethod
    def delete_file(cls, key_or_url: str) -> bool:
        """Delete a file from R2. Accepts key or full URL."""
        try:
            client = cls._get_client()
            key = cls.extract_file_key(key_or_url)
            client.delete_object(Bucket=settings.R2_BUCKET_NAME, Key=key)
            logger.info("Deleted file: %s", key)
            return True
        except Exception as e:
            logger.error("Failed to delete %s: %s", key_or_url, str(e))
            return False

    @classmethod
    def delete_files(cls, keys_or_urls: list[str]) -> int:
        """Batch delete files from R2. Returns count of successfully deleted."""
        if not keys_or_urls:
            return 0
        try:
            client = cls._get_client()
            objects = [{"Key": cls.extract_file_key(k)} for k in keys_or_urls]
            client.delete_objects(
                Bucket=settings.R2_BUCKET_NAME,
                Delete={"Objects": objects},
            )
            logger.info("Batch deleted %d files", len(keys_or_urls))
            return len(keys_or_urls)
        except Exception as e:
            logger.error("Batch delete failed: %s", str(e))
            return 0

    # ── Verification ─────────────────────────────────────────────

    @classmethod
    def verify_file_exists(cls, key_or_url: str) -> bool:
        """Check if a file exists in R2."""
        key = cls.extract_file_key(key_or_url)
        try:
            client = cls._get_client()
            client.head_object(Bucket=settings.R2_BUCKET_NAME, Key=key)
            return True
        except ClientError:
            return False


# Global singleton instance for convenience imports
storage_service = StorageService()
