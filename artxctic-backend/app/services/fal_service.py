"""Fal.ai integration service for AI image/video generation."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

# Fal.ai API base URL
FAL_API_BASE = "https://queue.fal.run"

# ── Model Name → Fal.ai Endpoint Mappings ───────────────────────
# These maps accept internal keys, display names, short names, and
# full endpoints so the frontend can send any reasonable identifier.

VIDEO_MODEL_MAP: dict[str, str] = {
    # Internal keys (backward compat)
    "model-1": "fal-ai/kling-video/v1/standard/text-to-video",
    "model-2": "fal-ai/minimax/video-01",
    # Display names from frontend
    "Nano Banana": "fal-ai/minimax/video-01",
    # Short names
    "minimax": "fal-ai/minimax/video-01",
    "minmax": "fal-ai/minimax/video-01",  # typo guard
    "kling": "fal-ai/kling-video/v1/standard/text-to-video",
    "kling-pro": "fal-ai/kling-video/v1.6/pro/text-to-video",
    "luma": "fal-ai/luma-dream-machine",
    "luma-ray2": "fal-ai/luma-dream-machine/ray-2",
    # Full endpoints (pass-through)
    "fal-ai/minmax/video-01": "fal-ai/minimax/video-01",  # typo guard
    "fal-ai/minimax/video-01": "fal-ai/minimax/video-01",
    "fal-ai/kling-video/v1/standard/text-to-video": "fal-ai/kling-video/v1/standard/text-to-video",
    "fal-ai/kling-video/v1.6/pro/text-to-video": "fal-ai/kling-video/v1.6/pro/text-to-video",
    "fal-ai/luma-dream-machine": "fal-ai/luma-dream-machine",
    "fal-ai/luma-dream-machine/ray-2": "fal-ai/luma-dream-machine/ray-2",
}

IMAGE_MODEL_MAP: dict[str, str] = {
    # Internal keys (backward compat)
    "model-1": "fal-ai/flux/dev",
    "model-2": "fal-ai/fast-sdxl",
    # Display names from frontend
    "Flux Schnell": "fal-ai/flux/schnell",
    "Flux Dev": "fal-ai/flux/dev",
    "Flux Pro": "fal-ai/flux-pro",
    # Short names
    "flux-schnell": "fal-ai/flux/schnell",
    "flux-dev": "fal-ai/flux/dev",
    "flux-pro": "fal-ai/flux-pro",
    # Full endpoints (pass-through)
    "fal-ai/flux/schnell": "fal-ai/flux/schnell",
    "fal-ai/flux/dev": "fal-ai/flux/dev",
    "fal-ai/flux-pro": "fal-ai/flux-pro",
    "fal-ai/fast-sdxl": "fal-ai/fast-sdxl",
}

# Default endpoints used as fallbacks
_DEFAULT_VIDEO_ENDPOINT = "fal-ai/minimax/video-01"
_DEFAULT_IMAGE_ENDPOINT = "fal-ai/flux/dev"

# Backward-compatible aliases so existing imports still work
IMAGE_MODELS = IMAGE_MODEL_MAP
VIDEO_MODELS = VIDEO_MODEL_MAP


def resolve_video_model(model_name: str) -> str:
    """Convert any model name / display name to the correct Fal.ai endpoint."""
    resolved = VIDEO_MODEL_MAP.get(model_name, model_name)
    # If the resolved value still isn't a known endpoint, fall back to default
    if not resolved.startswith("fal-ai/"):
        logger.warning(
            "Unknown video model '%s', falling back to default: %s",
            model_name, _DEFAULT_VIDEO_ENDPOINT,
        )
        resolved = _DEFAULT_VIDEO_ENDPOINT
    return resolved


def resolve_image_model(model_name: str) -> str:
    """Convert any model name / display name to the correct Fal.ai endpoint."""
    resolved = IMAGE_MODEL_MAP.get(model_name, model_name)
    if not resolved.startswith("fal-ai/"):
        logger.warning(
            "Unknown image model '%s', falling back to default: %s",
            model_name, _DEFAULT_IMAGE_ENDPOINT,
        )
        resolved = _DEFAULT_IMAGE_ENDPOINT
    return resolved


class FalService:
    """Interact with the Fal.ai API for AI generation."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.FAL_API_KEY
        self.headers = {
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json",
        }

    async def submit_image_generation(
        self,
        prompt: str,
        model: str = "model-1",
        aspect_ratio: str = "1:1",
        reference_image_url: str | None = None,
    ) -> dict[str, Any]:
        """Submit an async image generation request to Fal.ai.

        Returns: {"request_id": "...", "status": "IN_QUEUE"}
        """
        model_endpoint = resolve_image_model(model)
        logger.info("Image generation: input model='%s' → resolved='%s'", model, model_endpoint)

        # Map aspect ratios to image sizes
        size_map = {
            "1:1": {"width": 1024, "height": 1024},
            "16:9": {"width": 1344, "height": 768},
            "9:16": {"width": 768, "height": 1344},
            "4:3": {"width": 1152, "height": 896},
        }
        size = size_map.get(aspect_ratio, size_map["1:1"])

        payload: dict[str, Any] = {
            "prompt": prompt,
            "image_size": size,
            "num_images": 4,
        }
        if reference_image_url:
            payload["image_url"] = reference_image_url

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{FAL_API_BASE}/{model_endpoint}",
                headers=self.headers,
                json=payload,
            )
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                try:
                    error_detail = response.json().get("detail", str(e))
                except Exception:
                    error_detail = str(e)
                raise Exception(error_detail) from e

            data = response.json()
            logger.info("Image generation queued: %s", data.get("request_id"))
            return data

    async def submit_video_generation(
        self,
        prompt: str,
        model: str = "model-1",
        aspect_ratio: str = "16:9",
        reference_image_url: str | None = None,
    ) -> dict[str, Any]:
        """Submit an async video generation request to Fal.ai."""
        model_endpoint = resolve_video_model(model)
        logger.info("Video generation: input model='%s' → resolved='%s'", model, model_endpoint)

        payload: dict[str, Any] = {
            "prompt": prompt,
        }
        if reference_image_url:
            payload["image_url"] = reference_image_url

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{FAL_API_BASE}/{model_endpoint}",
                headers=self.headers,
                json=payload,
            )
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                try:
                    error_detail = response.json().get("detail", str(e))
                except Exception:
                    error_detail = str(e)
                raise Exception(error_detail) from e

            data = response.json()
            logger.info("Video generation queued: %s", data.get("request_id"))
            return data

    async def check_status(self, model_endpoint: str, request_id: str, status_url: str | None = None) -> dict[str, Any]:
        """Poll the status of a queued generation request.

        Returns: {"status": "IN_QUEUE" | "IN_PROGRESS" | "COMPLETED", ...}
        """
        url = status_url if status_url else f"{FAL_API_BASE}/{model_endpoint}/requests/{request_id}/status"
        
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                url,
                headers=self.headers,
            )
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                try:
                    error_detail = response.json().get("detail", str(e))
                except Exception:
                    error_detail = str(e)
                raise Exception(error_detail) from e
            return response.json()

    async def get_result(self, model_endpoint: str, request_id: str, response_url: str | None = None) -> dict[str, Any]:
        """Fetch the completed result of a generation request."""
        url = response_url if response_url else f"{FAL_API_BASE}/{model_endpoint}/requests/{request_id}"
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(
                url,
                headers=self.headers,
            )
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                try:
                    error_detail = response.json().get("detail", str(e))
                except Exception:
                    error_detail = str(e)
                raise Exception(error_detail) from e
            return response.json()
