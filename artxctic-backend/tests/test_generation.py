"""Tests for generation API endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


class TestGenerateImage:
    """POST /api/v1/generate/image"""

    async def test_generate_image_unauthenticated(self, client: AsyncClient):
        resp = await client.post("/api/v1/generate/image", json={
            "prompt": "A beautiful sunset over mountains",
            "model": "flux",
        })
        assert resp.status_code == 401

    async def test_generate_image_missing_prompt(self, auth_client: AsyncClient):
        resp = await auth_client.post("/api/v1/generate/image", json={
            "model": "flux",
        })
        assert resp.status_code == 422

    async def test_generate_image_empty_prompt(self, auth_client: AsyncClient):
        resp = await auth_client.post("/api/v1/generate/image", json={
            "prompt": "",
            "model": "flux",
        })
        assert resp.status_code == 422


class TestGenerateVideo:
    """POST /api/v1/generate/video"""

    async def test_generate_video_unauthenticated(self, client: AsyncClient):
        resp = await client.post("/api/v1/generate/video", json={
            "prompt": "A cinematic drone shot of a city",
            "model": "minimax",
        })
        assert resp.status_code == 401

    async def test_generate_video_missing_prompt(self, auth_client: AsyncClient):
        resp = await auth_client.post("/api/v1/generate/video", json={
            "model": "minimax",
        })
        assert resp.status_code == 422


class TestGenerationStatus:
    """GET /api/v1/generate/status/{job_id}"""

    async def test_status_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/generate/status/12345")
        assert resp.status_code == 401

    async def test_status_nonexistent_job(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/generate/status/99999999999")
        assert resp.status_code == 404
