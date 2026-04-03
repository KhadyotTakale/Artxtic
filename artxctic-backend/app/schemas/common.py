"""Common response schemas used across the API."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Structured error payload."""
    code: str
    message: str
    details: dict[str, Any] | None = None


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response wrapper."""
    success: bool = True
    data: T | None = None
    message: str | None = None


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""
    success: bool = False
    error: ErrorDetail


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response."""
    success: bool = True
    data: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
