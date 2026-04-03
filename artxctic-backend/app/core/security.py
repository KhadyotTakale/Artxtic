"""JWT token management, password hashing, and cookie utilities."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
import bcrypt as _bcrypt

from app.core.config import settings

# ── Password Hashing ────────────────────────────────────────────


def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt."""
    return _bcrypt.hashpw(password.encode("utf-8"), _bcrypt.gensalt(12)).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash."""
    return _bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ── JWT Tokens ───────────────────────────────────────────────────
def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict[str, Any] | None:
    """Decode and verify a JWT token. Returns None if invalid."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


# ── OTP ──────────────────────────────────────────────────────────
def generate_otp(length: int | None = None) -> str:
    """Generate a random numeric OTP of the configured length."""
    n = length or settings.OTP_LENGTH
    # Generate a cryptographically-secure random number with exactly `n` digits
    lower = 10 ** (n - 1)
    upper = (10**n) - 1
    return str(secrets.randbelow(upper - lower + 1) + lower)


# ── Misc ─────────────────────────────────────────────────────────
def generate_secure_token() -> str:
    """Generate a cryptographically secure URL-safe token."""
    return secrets.token_urlsafe(48)
