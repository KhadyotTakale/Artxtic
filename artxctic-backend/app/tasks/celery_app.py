"""Celery application configuration."""

from __future__ import annotations

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "artxtic",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# Periodic tasks (Celery Beat)
celery_app.conf.beat_schedule = {
    "cleanup-expired-media": {
        "task": "app.tasks.media_cleanup.cleanup_expired_media",
        "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM UTC
    },
    "reset-monthly-usage": {
        "task": "app.tasks.media_cleanup.reset_monthly_usage",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),  # 1st of each month
    },
}

# Auto-discover tasks
celery_app.autodiscover_tasks(["app.tasks"])
