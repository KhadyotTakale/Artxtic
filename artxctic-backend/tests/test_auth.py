"""Tests for authentication API endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


class TestRegister:
    """POST /api/v1/auth/register"""

    async def test_register_success(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "StrongPass1",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "alice@example.com"

    async def test_register_duplicate_email(self, client: AsyncClient, registered_user):
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Duplicate",
            "email": "test@example.com",  # same as registered_user
            "password": "StrongPass1",
        })
        assert resp.status_code in (400, 409)

    async def test_register_missing_name(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "email": "noname@example.com",
            "password": "StrongPass1",
        })
        assert resp.status_code == 422

    async def test_register_invalid_email(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Bad",
            "email": "not-an-email",
            "password": "StrongPass1",
        })
        assert resp.status_code == 422

    async def test_register_short_password(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/register", json={
            "name": "Short",
            "email": "short@example.com",
            "password": "Ab1",
        })
        assert resp.status_code == 422


class TestLogin:
    """POST /api/v1/auth/login"""

    async def test_login_success(self, client: AsyncClient, registered_user):
        resp = await client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "StrongPass1",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["user"]["email"] == "test@example.com"
        assert "access_token" in resp.cookies

    async def test_login_wrong_password(self, client: AsyncClient, registered_user):
        resp = await client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "WrongPassword1",
        })
        assert resp.status_code == 401

    async def test_login_nonexistent_email(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/login", json={
            "email": "nobody@example.com",
            "password": "StrongPass1",
        })
        assert resp.status_code == 401

    async def test_login_missing_email(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/login", json={
            "password": "StrongPass1",
        })
        assert resp.status_code == 422

    async def test_login_sets_cookies(self, client: AsyncClient, registered_user):
        resp = await client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "StrongPass1",
        })
        assert resp.status_code == 200
        assert "access_token" in resp.cookies


class TestGetMe:
    """GET /api/v1/auth/me"""

    async def test_get_me_authenticated(self, auth_client: AsyncClient, registered_user):
        resp = await auth_client.get("/api/v1/auth/me")
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["data"]["email"] == "test@example.com"
        assert data["data"]["name"] == "Test User"

    async def test_get_me_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    async def test_get_me_invalid_token(self, client: AsyncClient):
        client.cookies.set("access_token", "invalid-jwt-token")
        resp = await client.get("/api/v1/auth/me")
        assert resp.status_code == 401


class TestLogout:
    """POST /api/v1/auth/logout"""

    async def test_logout_authenticated(self, auth_client: AsyncClient):
        resp = await auth_client.post("/api/v1/auth/logout")
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_logout_unauthenticated(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/logout")
        assert resp.status_code == 401


class TestForgotPassword:
    """POST /api/v1/auth/forgot-password"""

    async def test_forgot_password_existing_email(self, client: AsyncClient, registered_user):
        resp = await client.post("/api/v1/auth/forgot-password", json={
            "email": "test@example.com",
        })
        # Should always return 200 (don't reveal if email exists)
        assert resp.status_code == 200
        assert resp.json()["success"] is True

    async def test_forgot_password_nonexistent_email(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/forgot-password", json={
            "email": "nobody@example.com",
        })
        assert resp.status_code == 200  # silent failure


class TestRefreshToken:
    """POST /api/v1/auth/refresh"""

    async def test_refresh_without_cookie(self, client: AsyncClient):
        resp = await client.post("/api/v1/auth/refresh")
        assert resp.status_code == 401
