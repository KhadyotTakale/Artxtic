"""Google OAuth service."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


class OAuthService:
    """Handle Google OAuth flow."""

    @staticmethod
    async def exchange_code_for_tokens(code: str) -> dict[str, Any]:
        """Exchange the authorization code for access and ID tokens."""
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                },
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_user_info(access_token: str) -> dict[str, Any]:
        """Fetch the authenticated user's Google profile info."""
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            data = response.json()
            logger.info("Google user info fetched: %s", data.get("email"))
            return data

    @staticmethod
    async def authenticate(code: str) -> dict[str, str]:
        """Full OAuth flow: exchange code → get profile.

        Returns: {"email": "...", "name": "...", "google_id": "..."}
        """
        tokens = await OAuthService.exchange_code_for_tokens(code)
        access_token = tokens["access_token"]
        user_info = await OAuthService.get_user_info(access_token)

        return {
            "email": user_info["email"],
            "name": user_info.get("name", ""),
            "google_id": user_info["id"],
            "picture": user_info.get("picture", ""),
        }
