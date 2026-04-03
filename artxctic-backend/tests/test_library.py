"""Tests for library API endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


class TestStarredList:
    """GET /api/v1/library/starred"""

    async def test_starred_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/library/starred")
        assert resp.status_code == 401

    async def test_starred_empty_list(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/library/starred")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["data"] == []

    async def test_starred_with_pagination(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/library/starred?page=1&page_size=10")
        assert resp.status_code == 200


class TestHistoryList:
    """GET /api/v1/library/history"""

    async def test_history_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/library/history")
        assert resp.status_code == 401

    async def test_history_empty_list(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/library/history")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["data"] == []

    async def test_history_with_type_filter(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/library/history?media_type=image")
        assert resp.status_code == 200


class TestStarToggle:
    """POST /api/v1/library/star/{media_id}"""

    async def test_star_unauthenticated(self, client: AsyncClient):
        resp = await client.post("/api/v1/library/star/12345")
        assert resp.status_code == 401

    async def test_star_nonexistent_media(self, auth_client: AsyncClient):
        resp = await auth_client.post("/api/v1/library/star/99999999999")
        assert resp.status_code == 404


class TestDeleteMedia:
    """DELETE /api/v1/library/{media_id}"""

    async def test_delete_unauthenticated(self, client: AsyncClient):
        resp = await client.delete("/api/v1/library/12345")
        assert resp.status_code == 401

    async def test_delete_nonexistent_media(self, auth_client: AsyncClient):
        resp = await auth_client.delete("/api/v1/library/99999999999")
        assert resp.status_code == 404


class TestFilter:
    """GET /api/v1/library/filter"""

    async def test_filter_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/library/filter")
        assert resp.status_code == 401

    async def test_filter_returns_empty(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/library/filter")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True


class TestDownload:
    """GET /api/v1/library/download/{media_id}"""

    async def test_download_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/library/download/12345")
        assert resp.status_code == 401

    async def test_download_nonexistent_media(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/library/download/99999999999")
        assert resp.status_code == 404
