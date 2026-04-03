"""Email background tasks."""

from __future__ import annotations

import asyncio
import logging

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


def _run_async(coro):  # type: ignore[no-untyped-def]
    """Helper to run async code from sync Celery tasks."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_verification_email_task(self, to_email: str, otp: str, name: str | None = None) -> bool:  # type: ignore[no-untyped-def]
    """Send verification OTP email (background)."""
    try:
        from app.services.email_service import EmailService
        result = _run_async(EmailService.send_verification_otp(to_email, otp, name))
        if not result:
            raise Exception("Email sending failed")
        return True
    except Exception as exc:
        logger.error("Email task failed for %s: %s", to_email, str(exc))
        self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email_task(self, to_email: str, token: str, name: str | None = None) -> bool:  # type: ignore[no-untyped-def]
    """Send password reset email (background)."""
    try:
        from app.services.email_service import EmailService
        result = _run_async(EmailService.send_password_reset(to_email, token, name))
        if not result:
            raise Exception("Email sending failed")
        return True
    except Exception as exc:
        logger.error("Password reset email failed for %s: %s", to_email, str(exc))
        self.retry(exc=exc)
