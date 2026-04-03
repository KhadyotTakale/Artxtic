"""Authentication API endpoints (9 endpoints)."""

from __future__ import annotations

import asyncio
import logging
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.security import create_access_token, create_refresh_token
from app.core.snowflake import generate_id
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    GoogleAuthRequest,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    ResetPasswordRequest,
    SendOTPRequest,
    UserBrief,
    VerifyEmailRequest,
    VerifyOTPLoginRequest,
)
from app.schemas.common import SuccessResponse
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.services.oauth_service import OAuthService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """Set JWT tokens as HTTP-only cookies."""
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN or None,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN or None,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/api/v1/auth",
    )


def _clear_auth_cookies(response: Response) -> None:
    """Clear JWT cookies."""
    response.delete_cookie("access_token", domain=settings.COOKIE_DOMAIN or None)
    response.delete_cookie("refresh_token", domain=settings.COOKIE_DOMAIN or None, path="/api/v1/auth")


# ── 1. POST /auth/register ──────────────────────────────────────
@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RegisterResponse:
    """Register a new user and send OTP verification email."""
    auth_service = AuthService(db)
    user, otp = await auth_service.register(body.name, body.email, body.password)

    # Send verification email (fire-and-forget)
    asyncio.create_task(EmailService.send_verification_otp(user.email, otp, user.name))

    return RegisterResponse(email=user.email)


# ── 2. POST /auth/verify-email ──────────────────────────────────
@router.post("/verify-email", response_model=SuccessResponse)
async def verify_email(
    body: VerifyEmailRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SuccessResponse:
    """Verify email using OTP and auto-login the user."""
    auth_service = AuthService(db)
    user = await auth_service.verify_email(body.email, body.otp)

    # Auto-login after verification
    access_token, refresh_token = await auth_service._create_tokens(user)
    _set_auth_cookies(response, access_token, refresh_token)

    return SuccessResponse(message="Email verified successfully")


# ── 3. POST /auth/send-otp ──────────────────────────────────────
@router.post("/send-otp", response_model=RegisterResponse)
async def send_otp(
    body: SendOTPRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RegisterResponse:
    """Send OTP for login/registration (creates user if new)."""
    auth_service = AuthService(db)
    otp = await auth_service.send_otp_login(body.email, body.name)

    # Send OTP email (fire-and-forget — don't block the response)
    asyncio.create_task(EmailService.send_verification_otp(body.email, otp, body.name))

    return RegisterResponse(message="OTP sent to email", email=body.email)


# ── 4. POST /auth/verify-otp-login ──────────────────────────────
@router.post("/verify-otp-login", response_model=LoginResponse)
async def verify_otp_login(
    body: VerifyOTPLoginRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LoginResponse:
    """Verify OTP and login (create session)."""
    auth_service = AuthService(db)
    user, access_token, refresh_token = await auth_service.verify_otp_login(
        body.email, body.otp, body.name
    )

    _set_auth_cookies(response, access_token, refresh_token)

    return LoginResponse(
        user=UserBrief(
            id=str(user.id),
            email=user.email,
            name=user.name,
            is_verified=user.is_verified,
        ),
    )


# ── 5. POST /auth/login ─────────────────────────────────────────
@router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LoginResponse:
    """Login with email and password."""
    auth_service = AuthService(db)
    user, access_token, refresh_token = await auth_service.login(body.email, body.password)

    _set_auth_cookies(response, access_token, refresh_token)

    return LoginResponse(
        user=UserBrief(
            id=str(user.id),
            email=user.email,
            name=user.name,
            is_verified=user.is_verified,
        ),
    )


# ── 4. POST /auth/logout ────────────────────────────────────────
@router.post("/logout", response_model=SuccessResponse)
async def logout(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    refresh_token: str | None = Cookie(default=None),
) -> SuccessResponse:
    """Logout and invalidate tokens."""
    auth_service = AuthService(db)
    await auth_service.logout(current_user.id, refresh_token)
    _clear_auth_cookies(response)
    return SuccessResponse(message="Logged out successfully")


# ── 5. POST /auth/forgot-password ───────────────────────────────
@router.post("/forgot-password", response_model=SuccessResponse)
async def forgot_password(
    body: ForgotPasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SuccessResponse:
    """Request a password reset email."""
    auth_service = AuthService(db)
    token = await auth_service.forgot_password(body.email)

    if token:
        # Get user name for email
        result = await db.execute(select(User).where(User.email == body.email.lower()))
        user = result.scalar_one_or_none()
        asyncio.create_task(EmailService.send_password_reset(body.email, token, user.name if user else None))

    # Always return success (don't reveal if email exists)
    return SuccessResponse(message="If an account exists, a password reset email has been sent")


# ── 6. POST /auth/reset-password ────────────────────────────────
@router.post("/reset-password", response_model=SuccessResponse)
async def reset_password(
    body: ResetPasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SuccessResponse:
    """Reset password using a valid reset token."""
    auth_service = AuthService(db)
    await auth_service.reset_password(body.token, body.new_password)
    return SuccessResponse(message="Password reset successfully")


# ── 7. POST /auth/google ────────────────────────────────────────
@router.post("/google", response_model=LoginResponse)
async def google_oauth(
    body: GoogleAuthRequest,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LoginResponse:
    """Google OAuth login/registration."""
    # Exchange code for Google profile
    google_user = await OAuthService.authenticate(body.code)

    # Check if user exists
    result = await db.execute(select(User).where(User.email == google_user["email"]))
    user = result.scalar_one_or_none()

    if not user:
        # Create new user
        user = User(
            id=generate_id(),
            email=google_user["email"],
            name=google_user.get("name"),
            is_verified=True,  # Google accounts are pre-verified
            oauth_provider="google",
            oauth_id=google_user["google_id"],
        )
        db.add(user)
        await db.flush()
    elif not user.oauth_provider:
        # Link existing email account to Google
        user.oauth_provider = "google"
        user.oauth_id = google_user["google_id"]
        if not user.is_verified:
            user.is_verified = True
        await db.flush()

    auth_service = AuthService(db)
    access_token, refresh_token = await auth_service._create_tokens(user)
    _set_auth_cookies(response, access_token, refresh_token)

    return LoginResponse(
        user=UserBrief(
            id=str(user.id),
            email=user.email,
            name=user.name,
            is_verified=user.is_verified,
        ),
    )


# ── 8. GET /auth/me ─────────────────────────────────────────────
@router.get("/me")
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Get the currently authenticated user."""
    return {
        "success": True,
        "data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "name": current_user.name,
            "country": current_user.country,
            "is_verified": current_user.is_verified,
            "oauth_provider": current_user.oauth_provider,
            "created_at": current_user.created_at.isoformat(),
        },
    }


# ── 9. POST /auth/refresh ───────────────────────────────────────
@router.post("/refresh", response_model=SuccessResponse)
async def refresh_token(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
    refresh_token: str | None = Cookie(default=None),
) -> SuccessResponse:
    """Refresh the access token using the refresh token cookie."""
    from app.utils.exceptions import UnauthorizedError

    if not refresh_token:
        raise UnauthorizedError("No refresh token provided")

    auth_service = AuthService(db)
    new_access, new_refresh = await auth_service.refresh_access_token(refresh_token)
    _set_auth_cookies(response, new_access, new_refresh)

    return SuccessResponse(message="Token refreshed")
