"""Custom exception classes for structured error handling."""

from __future__ import annotations

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception."""

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        code: str = "BAD_REQUEST",
        message: str = "An error occurred",
        details: dict | None = None,
    ) -> None:
        self.code = code
        self.error_message = message
        self.details = details
        super().__init__(status_code=status_code, detail=message)


class NotFoundError(AppException):
    def __init__(self, resource: str = "Resource", message: str | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
            message=message or f"{resource} not found",
        )


class DuplicateError(AppException):
    def __init__(self, field: str = "Resource", message: str | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="DUPLICATE",
            message=message or f"{field} already exists",
        )


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Not authenticated") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="UNAUTHORIZED",
            message=message,
        )


class ForbiddenError(AppException):
    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            message=message,
        )


class RateLimitError(AppException):
    def __init__(self, message: str = "Too many requests") -> None:
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="RATE_LIMITED",
            message=message,
        )


class ValidationError(AppException):
    def __init__(self, message: str = "Validation error", details: dict | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="VALIDATION_ERROR",
            message=message,
            details=details,
        )


class UsageLimitExceeded(AppException):
    def __init__(self, media_type: str = "generation") -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="USAGE_LIMIT_EXCEEDED",
            message=f"Monthly {media_type} generation limit exceeded. Please upgrade your plan.",
        )
