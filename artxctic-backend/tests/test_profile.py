"""Tests for user profile API endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


class TestGetProfile:
    """GET /api/v1/user/profile"""

    async def test_get_profile_authenticated(self, auth_client: AsyncClient, registered_user):
        resp = await auth_client.get("/api/v1/user/profile")
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"

    async def test_get_profile_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/user/profile")
        assert resp.status_code == 401


class TestUpdateProfile:
    """PATCH /api/v1/user/profile"""

    async def test_update_name(self, auth_client: AsyncClient, registered_user):
        resp = await auth_client.put("/api/v1/user/profile", json={
            "name": "Updated Name",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True

    async def test_update_country(self, auth_client: AsyncClient, registered_user):
        resp = await auth_client.put("/api/v1/user/profile", json={
            "country": "India",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True

    async def test_update_profile_unauthenticated(self, client: AsyncClient):
        resp = await client.put("/api/v1/user/profile", json={
            "name": "Hacker",
        })
        assert resp.status_code == 401


class TestGetSubscriptionDetails:
    """GET /api/v1/user/subscription"""

    async def test_get_subscription_authenticated(self, auth_client: AsyncClient, registered_user):
        resp = await auth_client.get("/api/v1/user/subscription")
        assert resp.status_code == 200
        data = resp.json()
        assert "plan_name" in data

    async def test_get_subscription_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/user/subscription")
        assert resp.status_code == 401
