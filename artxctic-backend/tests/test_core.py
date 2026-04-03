"""Tests for core modules: security, snowflake, and config."""

from __future__ import annotations

import time

import pytest

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_otp,
    generate_secure_token,
    hash_password,
    verify_password,
)
from app.core.snowflake import SnowflakeGenerator, generate_id


# ── Password Hashing ───────────────────────────────────────────

class TestPasswordHashing:
    def test_hash_password_produces_hash(self):
        hashed = hash_password("MyPassword123")
        assert hashed.startswith("$2b$")
        assert hashed != "MyPassword123"

    def test_verify_correct_password(self):
        hashed = hash_password("MyPassword123")
        assert verify_password("MyPassword123", hashed) is True

    def test_verify_wrong_password(self):
        hashed = hash_password("MyPassword123")
        assert verify_password("WrongPassword", hashed) is False

    def test_different_hashes_for_same_password(self):
        h1 = hash_password("Same")
        h2 = hash_password("Same")
        assert h1 != h2  # bcrypt uses random salt


# ── JWT Tokens ─────────────────────────────────────────────────

class TestJWTTokens:
    def test_create_and_decode_access_token(self):
        token = create_access_token({"sub": "12345"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "12345"
        assert payload["type"] == "access"

    def test_create_and_decode_refresh_token(self):
        token = create_refresh_token({"sub": "12345"})
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "12345"
        assert payload["type"] == "refresh"

    def test_decode_invalid_token_returns_none(self):
        assert decode_token("invalid.token.here") is None

    def test_decode_empty_string_returns_none(self):
        assert decode_token("") is None

    def test_token_contains_expiry(self):
        token = create_access_token({"sub": "1"})
        payload = decode_token(token)
        assert "exp" in payload

    def test_access_and_refresh_tokens_are_different(self):
        access = create_access_token({"sub": "1"})
        refresh = create_refresh_token({"sub": "1"})
        assert access != refresh


# ── OTP ────────────────────────────────────────────────────────

class TestOTP:
    def test_otp_default_length(self):
        otp = generate_otp()
        assert len(otp) == 6
        assert otp.isdigit()

    def test_otp_custom_length(self):
        otp = generate_otp(length=8)
        assert len(otp) == 8
        assert otp.isdigit()

    def test_otp_is_random(self):
        otps = {generate_otp() for _ in range(20)}
        assert len(otps) > 1  # should not all be the same

    def test_otp_no_leading_zeros_lost(self):
        # OTP should always maintain its length
        for _ in range(50):
            otp = generate_otp(length=4)
            assert len(otp) == 4

    def test_secure_token_is_url_safe(self):
        token = generate_secure_token()
        assert len(token) > 20
        assert " " not in token


# ── Snowflake IDs ──────────────────────────────────────────────

class TestSnowflakeGenerator:
    def test_generates_positive_integer(self):
        gen = SnowflakeGenerator(worker_id=0, datacenter_id=0)
        sid = gen.generate()
        assert isinstance(sid, int)
        assert sid > 0

    def test_generates_unique_ids(self):
        gen = SnowflakeGenerator(worker_id=1, datacenter_id=1)
        ids = [gen.generate() for _ in range(1000)]
        assert len(set(ids)) == 1000

    def test_ids_are_monotonically_increasing(self):
        gen = SnowflakeGenerator(worker_id=1, datacenter_id=1)
        ids = [gen.generate() for _ in range(100)]
        assert ids == sorted(ids)

    def test_invalid_worker_id_raises(self):
        with pytest.raises(ValueError):
            SnowflakeGenerator(worker_id=32, datacenter_id=0)

    def test_invalid_datacenter_id_raises(self):
        with pytest.raises(ValueError):
            SnowflakeGenerator(worker_id=0, datacenter_id=32)

    def test_negative_worker_id_raises(self):
        with pytest.raises(ValueError):
            SnowflakeGenerator(worker_id=-1, datacenter_id=0)

    def test_module_level_generate_id(self):
        sid = generate_id()
        assert isinstance(sid, int)
        assert sid > 0

    def test_ids_fit_in_64_bits(self):
        gen = SnowflakeGenerator(worker_id=1, datacenter_id=1)
        for _ in range(100):
            sid = gen.generate()
            assert sid < (1 << 63)  # fits in signed 64-bit
