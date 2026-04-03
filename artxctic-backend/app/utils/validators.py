"""Input validation utilities."""

from __future__ import annotations

import re


def validate_password(password: str) -> list[str]:
    """Validate password strength. Returns list of error messages."""
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if len(password) > 128:
        errors.append("Password must be at most 128 characters")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least 1 uppercase letter")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least 1 lowercase letter")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least 1 digit")
    return errors


def validate_prompt(prompt: str) -> list[str]:
    """Validate a generation prompt. Returns list of error messages."""
    errors = []
    if len(prompt) < 10:
        errors.append("Prompt must be at least 10 characters")
    if len(prompt) > 1000:
        errors.append("Prompt must be at most 1000 characters")
    return errors
