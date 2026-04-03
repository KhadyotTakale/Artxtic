"""Snowflake ID generator for producing unique BigInt primary keys.

Generates 64-bit IDs composed of:
  - 41 bits: millisecond timestamp (custom epoch)
  - 5 bits:  datacenter id
  - 5 bits:  worker id
  - 12 bits: sequence number (per-millisecond)

This yields up to 4096 unique IDs per millisecond per worker.
"""

from __future__ import annotations

import threading
import time


# Custom epoch: 2024-01-01 00:00:00 UTC (in milliseconds)
_EPOCH = 1_704_067_200_000

_DATACENTER_ID_BITS = 5
_WORKER_ID_BITS = 5
_SEQUENCE_BITS = 12

_MAX_DATACENTER_ID = (1 << _DATACENTER_ID_BITS) - 1
_MAX_WORKER_ID = (1 << _WORKER_ID_BITS) - 1
_MAX_SEQUENCE = (1 << _SEQUENCE_BITS) - 1

_WORKER_ID_SHIFT = _SEQUENCE_BITS
_DATACENTER_ID_SHIFT = _SEQUENCE_BITS + _WORKER_ID_BITS
_TIMESTAMP_SHIFT = _SEQUENCE_BITS + _WORKER_ID_BITS + _DATACENTER_ID_BITS


class SnowflakeGenerator:
    """Thread-safe Snowflake ID generator."""

    def __init__(self, worker_id: int = 1, datacenter_id: int = 1) -> None:
        if worker_id < 0 or worker_id > _MAX_WORKER_ID:
            raise ValueError(f"worker_id must be between 0 and {_MAX_WORKER_ID}")
        if datacenter_id < 0 or datacenter_id > _MAX_DATACENTER_ID:
            raise ValueError(f"datacenter_id must be between 0 and {_MAX_DATACENTER_ID}")

        self._worker_id = worker_id
        self._datacenter_id = datacenter_id
        self._sequence = 0
        self._last_timestamp = -1
        self._lock = threading.Lock()

    def _current_millis(self) -> int:
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp: int) -> int:
        ts = self._current_millis()
        while ts <= last_timestamp:
            ts = self._current_millis()
        return ts

    def generate(self) -> int:
        """Generate a unique Snowflake ID (BigInt)."""
        with self._lock:
            timestamp = self._current_millis()

            if timestamp < self._last_timestamp:
                raise RuntimeError("Clock moved backwards. Refusing to generate ID.")

            if timestamp == self._last_timestamp:
                self._sequence = (self._sequence + 1) & _MAX_SEQUENCE
                if self._sequence == 0:
                    timestamp = self._wait_next_millis(self._last_timestamp)
            else:
                self._sequence = 0

            self._last_timestamp = timestamp

            snowflake_id = (
                ((timestamp - _EPOCH) << _TIMESTAMP_SHIFT)
                | (self._datacenter_id << _DATACENTER_ID_SHIFT)
                | (self._worker_id << _WORKER_ID_SHIFT)
                | self._sequence
            )
            return snowflake_id


# Module-level singleton — initialized lazily in generate_id()
_generator: SnowflakeGenerator | None = None


def _get_generator() -> SnowflakeGenerator:
    global _generator
    if _generator is None:
        from app.core.config import settings
        _generator = SnowflakeGenerator(
            worker_id=settings.WORKER_ID,
            datacenter_id=settings.DATACENTER_ID,
        )
    return _generator


def generate_id() -> int:
    """Generate a unique Snowflake BigInt ID."""
    return _get_generator().generate()
