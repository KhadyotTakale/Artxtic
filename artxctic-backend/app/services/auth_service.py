"""Authentication service — registration, login, OTP, tokens."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_otp,
    generate_secure_token,
    hash_password,
    verify_password,
)
from app.core.snowflake import generate_id
from app.models.auth import EmailVerificationToken, PasswordResetToken, RefreshToken
from app.models.user import User
from app.utils.exceptions import DuplicateError, NotFoundError, UnauthorizedError, ValidationError

logger = logging.getLogger(__name__)


class AuthService:
    """Handles all authentication business logic."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # ── Registration ─────────────────────────────────────────────
    async def register(self, name: str, email: str, password: str) -> tuple[User, str]:
        """Register a new user and return (user, otp)."""
        # Check if email already exists
        result = await self.db.execute(select(User).where(User.email == email.lower()))
        if result.scalar_one_or_none():
            raise DuplicateError("Email", "An account with this email already exists")

        user = User(
            id=generate_id(),
            email=email.lower(),
            password_hash=hash_password(password),
            name=name,
            is_verified=False,
        )
        self.db.add(user)
        await self.db.flush()

        otp = await self._create_email_verification(user.id)
        logger.info("User registered: %s", user.email)
        return user, otp

    async def _create_email_verification(self, user_id: int) -> str:
        """Create an OTP token for email verification."""
        # Delete any existing tokens for this user
        await self.db.execute(
            delete(EmailVerificationToken).where(EmailVerificationToken.user_id == user_id)
        )

        otp = generate_otp()
        token = EmailVerificationToken(
            id=generate_id(),
            user_id=user_id,
            token=otp,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES),
        )
        self.db.add(token)
        await self.db.flush()
        return otp

    # ── Email Verification ───────────────────────────────────────
    async def verify_email(self, email: str, otp: str) -> User:
        """Verify user's email with OTP."""
        result = await self.db.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("User")

        if user.is_verified:
            raise ValidationError("Email already verified")

        # Find valid OTP
        result = await self.db.execute(
            select(EmailVerificationToken)
            .where(
                EmailVerificationToken.user_id == user.id,
                EmailVerificationToken.token == otp,
                EmailVerificationToken.expires_at > datetime.now(timezone.utc),
            )
        )
        token_record = result.scalar_one_or_none()

        if not token_record:
            raise ValidationError("Invalid or expired OTP")

        if token_record.attempts >= settings.OTP_MAX_ATTEMPTS:
            raise ValidationError("Maximum OTP attempts exceeded. Please request a new OTP.")

        token_record.attempts += 1

        if token_record.token != otp:
            await self.db.flush()
            raise ValidationError("Invalid OTP")

        # Mark user as verified and clean up
        user.is_verified = True
        await self.db.execute(
            delete(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id)
        )
        await self.db.flush()
        logger.info("Email verified: %s", user.email)
        return user

    # ── Resend OTP ───────────────────────────────────────────────
    async def resend_otp(self, email: str) -> str:
        """Resend OTP for email verification."""
        result = await self.db.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("User")

        if user.is_verified:
            raise ValidationError("Email already verified")

        otp = await self._create_email_verification(user.id)
        logger.info("OTP resent for: %s", user.email)
        return otp

    # ── OTP Login (Passwordless) ─────────────────────────────────
    async def send_otp_login(self, email: str, name: str | None = None) -> str:
        """Send OTP for login/registration. Creates user if not exists."""
        result = await self.db.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()

        if not user:
            # Create new user (unverified initially)
            try:
                user = User(
                    id=generate_id(),
                    email=email.lower(),
                    name=name,
                    password_hash=None,  # No password for OTP users
                    is_verified=False,
                )
                self.db.add(user)
                await self.db.flush()
                logger.info("New user created via OTP: %s", user.email)
            except IntegrityError:
                # Race condition: another request created this user concurrently
                await self.db.rollback()
                result = await self.db.execute(select(User).where(User.email == email.lower()))
                user = result.scalar_one_or_none()
                if not user:
                    raise ValidationError("Failed to create user. Please try again.")
                logger.info("User already exists (concurrent creation): %s", user.email)
        elif name and not user.name:
            # Update name if provided and not set
            user.name = name
            await self.db.flush()

        if not user.is_active:
            raise UnauthorizedError("Account is deactivated")

        return await self._create_email_verification(user.id)

    async def verify_otp_login(self, email: str, otp: str, name: str | None = None) -> tuple[User, str, str]:
        """Verify OTP login/registration. Returns (user, access_token, refresh_token)."""
        result = await self.db.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("User")

        # Find valid OTP
        result = await self.db.execute(
            select(EmailVerificationToken)
            .where(
                EmailVerificationToken.user_id == user.id,
                EmailVerificationToken.token == otp,
                EmailVerificationToken.expires_at > datetime.now(timezone.utc),
            )
        )
        token_record = result.scalar_one_or_none()

        if not token_record:
            raise ValidationError("Invalid or expired OTP")

        if token_record.attempts >= settings.OTP_MAX_ATTEMPTS:
            raise ValidationError("Maximum OTP attempts exceeded. Please request a new OTP.")

        token_record.attempts += 1

        if token_record.token != otp:
            await self.db.flush()
            raise ValidationError("Invalid OTP")

        # Success - Mark verified/active
        if not user.is_verified:
            user.is_verified = True
        
        if name and not user.name:
            user.name = name

        # Clean up tokens
        await self.db.execute(
            delete(EmailVerificationToken).where(EmailVerificationToken.user_id == user.id)
        )
        await self.db.flush()

        access_token, refresh_token = await self._create_tokens(user)
        logger.info("User logged in via OTP: %s", user.email)
        return user, access_token, refresh_token

    # ── Login ────────────────────────────────────────────────────
    async def login(self, email: str, password: str) -> tuple[User, str, str]:
        """Authenticate user and return (user, access_token, refresh_token)."""
        result = await self.db.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()

        if not user or not user.password_hash:
            raise UnauthorizedError("Invalid email or password")

        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        if not user.is_verified:
            raise UnauthorizedError("Please verify your email before logging in")

        if not user.is_active:
            raise UnauthorizedError("Account is deactivated")

        access_token, refresh_token = await self._create_tokens(user)
        logger.info("User logged in: %s", user.email)
        return user, access_token, refresh_token

    # ── Token Management ─────────────────────────────────────────
    async def _create_tokens(self, user: User) -> tuple[str, str]:
        """Create access + refresh token pair and store refresh token in DB."""
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        # Store refresh token in DB
        rt = RefreshToken(
            id=generate_id(),
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        self.db.add(rt)
        await self.db.flush()
        return access_token, refresh_token

    async def refresh_access_token(self, refresh_token_value: str) -> tuple[str, str]:
        """Validate refresh token and issue new token pair."""
        payload = decode_token(refresh_token_value)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid refresh token")

        user_id = int(payload["sub"])

        # Verify token exists in DB
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token == refresh_token_value,
                RefreshToken.user_id == user_id,
                RefreshToken.expires_at > datetime.now(timezone.utc),
            )
        )
        db_token = result.scalar_one_or_none()
        if not db_token:
            raise UnauthorizedError("Refresh token revoked or expired")

        # Delete old refresh token (rotate)
        await self.db.delete(db_token)

        # Get user
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or deactivated")

        new_access, new_refresh = await self._create_tokens(user)
        return new_access, new_refresh

    # ── Logout ───────────────────────────────────────────────────
    async def logout(self, user_id: int, refresh_token_value: str | None = None) -> None:
        """Invalidate refresh tokens for the user."""
        if refresh_token_value:
            await self.db.execute(
                delete(RefreshToken).where(RefreshToken.token == refresh_token_value)
            )
        else:
            # Delete all refresh tokens for user
            await self.db.execute(
                delete(RefreshToken).where(RefreshToken.user_id == user_id)
            )
        await self.db.flush()
        logger.info("User logged out: %d", user_id)

    # ── Password Reset ───────────────────────────────────────────
    async def forgot_password(self, email: str) -> str | None:
        """Create a password reset token. Returns token (or None if user not found — silent for security)."""
        result = await self.db.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()
        if not user:
            return None  # Don't reveal whether email exists

        # Delete existing reset tokens
        await self.db.execute(
            delete(PasswordResetToken).where(PasswordResetToken.user_id == user.id)
        )

        token_value = generate_secure_token()
        token = PasswordResetToken(
            id=generate_id(),
            user_id=user.id,
            token=token_value,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        self.db.add(token)
        await self.db.flush()
        return token_value

    async def reset_password(self, token_value: str, new_password: str) -> None:
        """Reset user's password using a valid reset token."""
        result = await self.db.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.token == token_value,
                PasswordResetToken.expires_at > datetime.now(timezone.utc),
            )
        )
        token_record = result.scalar_one_or_none()
        if not token_record:
            raise ValidationError("Invalid or expired reset token")

        result = await self.db.execute(select(User).where(User.id == token_record.user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundError("User")

        user.password_hash = hash_password(new_password)

        # Delete all reset tokens and refresh tokens for this user
        await self.db.execute(
            delete(PasswordResetToken).where(PasswordResetToken.user_id == user.id)
        )
        await self.db.execute(
            delete(RefreshToken).where(RefreshToken.user_id == user.id)
        )
        await self.db.flush()
        logger.info("Password reset for: %s", user.email)
