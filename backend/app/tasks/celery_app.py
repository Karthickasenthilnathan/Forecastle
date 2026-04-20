"""Celery application configuration.

Uses Redis as both broker and result backend.
Includes beat schedule for periodic tasks.
"""

from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery_app = Celery(
    "pulseflow",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.forecast_tasks",
        "app.tasks.ingestion_tasks",
    ],
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

# Beat schedule — periodic tasks
celery_app.conf.beat_schedule = {
    # Retrain models every Sunday at 2 AM UTC
    "weekly-model-retrain": {
        "task": "app.tasks.forecast_tasks.scheduled_retrain",
        "schedule": crontab(hour=2, minute=0, day_of_week=0),
    },
    # Collect signals every 6 hours
    "periodic-signal-ingestion": {
        "task": "app.tasks.ingestion_tasks.collect_all_signals",
        "schedule": crontab(hour="*/6", minute=15),
    },
}
