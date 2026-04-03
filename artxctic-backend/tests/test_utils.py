"""Tests for utility modules: validators, helpers, exceptions."""

from __future__ import annotations

import pytest

from app.utils.validators import validate_password, validate_prompt
from app.utils.helpers import is_valid_email, truncate_string


class TestPasswordValidation:
    def test_valid_password(self):
        errors = validate_password("StrongPass1")
        assert errors == []

    def test_password_too_short(self):
        errors = validate_password("Ab1")
        assert any("8 characters" in e for e in errors)

    def test_password_too_long(self):
        errors = validate_password("A" * 129)
        assert any("128" in e for e in errors)

    def test_password_no_uppercase(self):
        errors = validate_password("weakpass1")
        assert any("uppercase" in e for e in errors)

    def test_password_no_lowercase(self):
        errors = validate_password("STRONGPASS1")
        assert any("lowercase" in e for e in errors)

    def test_password_no_digit(self):
        errors = validate_password("StrongPass")
        assert any("digit" in e for e in errors)

    def test_password_all_failures(self):
        errors = validate_password("ab")
        assert len(errors) >= 2  # too short + no uppercase + no digit


class TestPromptValidation:
    def test_valid_prompt(self):
        errors = validate_prompt("A beautiful sunset over the ocean with vivid colors")
        assert errors == []

    def test_prompt_too_short(self):
        errors = validate_prompt("short")
        assert any("10 characters" in e for e in errors)

    def test_prompt_too_long(self):
        errors = validate_prompt("A" * 1001)
        assert any("1000" in e for e in errors)

    def test_prompt_exactly_10_chars(self):
        errors = validate_prompt("1234567890")
        assert errors == []


class TestEmailValidation:
    def test_valid_email(self):
        assert is_valid_email("user@example.com") is True

    def test_valid_email_with_dots(self):
        assert is_valid_email("first.last@example.com") is True

    def test_invalid_email_no_at(self):
        assert is_valid_email("noatsign.com") is False

    def test_invalid_email_no_domain(self):
        assert is_valid_email("user@") is False

    def test_invalid_email_empty(self):
        assert is_valid_email("") is False


class TestTruncateString:
    def test_short_string_unchanged(self):
        assert truncate_string("hello", 100) == "hello"

    def test_long_string_truncated(self):
        result = truncate_string("A" * 200, 100)
        assert len(result) == 100
        assert result.endswith("...")

    def test_exact_length_unchanged(self):
        s = "A" * 100
        assert truncate_string(s, 100) == s
