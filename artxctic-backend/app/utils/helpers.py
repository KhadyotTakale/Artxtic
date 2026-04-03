"""Utility helpers."""

from __future__ import annotations

import re


def is_valid_email(email: str) -> bool:
    """Check if string is a valid email address."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def extract_r2_key_from_url(url: str) -> str:
    """Extract the R2 object key from a full URL."""
    if "/" in url:
        parts = url.split("/")
        # Key is everything after the bucket URL
        if len(parts) > 3:
            return "/".join(parts[3:])
    return ""


def truncate_string(s: str, max_length: int = 100) -> str:
    """Truncate a string with ellipsis."""
    if len(s) <= max_length:
        return s
    return s[:max_length - 3] + "..."
