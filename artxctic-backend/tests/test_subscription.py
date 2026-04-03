"""Tests for subscription API endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.snowflake import generate_id
from app.models.subscription import SubscriptionPlan


class TestListPlans:
    """GET /api/v1/subscription/plans"""

    async def test_list_plans_returns_plans(self, client: AsyncClient, db_session: AsyncSession):
        # Seed a plan for this test
        plan = SubscriptionPlan(
            id=generate_id(),
            name="TestPlan",
            image_limit_monthly=50,
            video_limit_monthly=5,
            features={"image_generation": True},
            is_active=True,
        )
        db_session.add(plan)
        await db_session.flush()

        resp = await client.get("/api/v1/subscription/plans")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
        assert len(data["data"]) >= 1

    async def test_list_plans_no_auth_required(self, client: AsyncClient):
        resp = await client.get("/api/v1/subscription/plans")
        assert resp.status_code == 200


class TestCreateCheckout:
    """POST /api/v1/subscription/checkout"""

    async def test_checkout_unauthenticated(self, client: AsyncClient):
        resp = await client.post("/api/v1/subscription/checkout", json={
            "plan_id": "12345",
        })
        assert resp.status_code == 401


class TestCustomerPortal:
    """GET /api/v1/subscription/portal"""

    async def test_portal_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/subscription/portal")
        assert resp.status_code in (401, 405)  # GET or POST depending on implementation


class TestHealthCheck:
    """GET /health"""

    async def test_health_check(self, client: AsyncClient):
        resp = await client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["app"] == "Artxtic Backend"
        assert data["version"] == "0.1.0"

    async def test_root_endpoint(self, client: AsyncClient):
        resp = await client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert "app" in data
        assert data["docs"] == "/docs"


class TestValidation:
    """Tests for input validation across endpoints."""

    async def test_register_email_validation(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Test",
            "email": "not-valid",
            "password": "StrongPass1",
        })
        assert resp.status_code == 422

    async def test_register_password_too_short(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Test",
            "email": "valid@email.com",
            "password": "Ab1",
        })
        assert resp.status_code == 422

    async def test_empty_json_body(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/login", json={})
        assert resp.status_code == 422

    async def test_login_missing_password(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
        })
        assert resp.status_code == 422
