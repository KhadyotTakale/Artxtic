"""Authentication request/response schemas."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, field_validator
import re


# ── Registration ─────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    """Register a new user with email and password."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least 1 uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least 1 lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least 1 digit")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z\s\-]+$", v):
            raise ValueError("Name can only contain letters, spaces, and hyphens")
        return v.strip()


class RegisterResponse(BaseModel):
    """Response after successful registration — OTP sent."""
    message: str = "Verification email sent"
    email: str


# ── Email Verification (OTP) ────────────────────────────────────
class VerifyEmailRequest(BaseModel):
    """Verify email with OTP code."""
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")


class SendOTPRequest(BaseModel):
    """Request OTP for login/registration."""
    email: EmailStr
    name: str | None = Field(None, min_length=2, max_length=100)


class VerifyOTPLoginRequest(BaseModel):
    """Login/Register with OTP."""
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")
    name: str | None = None  # Optional name update during verification


# ── Login ────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    """Login with email and password."""
    email: EmailStr
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    """Returned on successful login (tokens set via cookies)."""
    message: str = "Login successful"
    user: UserBrief


class UserBrief(BaseModel):
    """Minimal user info returned in auth responses."""
    id: str
    email: str
    name: str | None = None
    plan: str = "free"
    is_verified: bool = False

    model_config = {"from_attributes": True}


# ── Forgot / Reset Password ─────────────────────────────────────
class ForgotPasswordRequest(BaseModel):
    """Request a password-reset email."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Set a new password using a reset token."""
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least 1 uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least 1 lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least 1 digit")
        return v


# ── Google OAuth ─────────────────────────────────────────────────
class GoogleAuthRequest(BaseModel):
    """Google OAuth callback with auth code."""
    code: str


# ── Token Refresh ────────────────────────────────────────────────
class RefreshTokenRequest(BaseModel):
    """Explicit refresh request (optional — can also use cookie)."""
    refresh_token: str | None = None
