"""
Celery configuration and app initialization.
"""

import logging

from app.config import settings
from celery import Celery

logger = logging.getLogger(__name__)

# Initialize Celery app
celery_app = Celery(
    "worker",
    broker=settings.get_broker_url(),
    backend=settings.get_result_backend(),
    include=["app.tasks"],  # Import tasks module
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Result backend settings
    result_expires=86400,  # Results expire after 24 hours
    # Worker settings
    worker_prefetch_multiplier=settings.worker_prefetch_multiplier,
    worker_max_tasks_per_child=settings.worker_max_tasks_per_child,
    worker_concurrency=settings.worker_concurrency,
    # Task execution settings
    task_acks_late=settings.task_acks_late,
    task_reject_on_worker_lost=settings.task_reject_on_worker_lost,
    task_track_started=True,
    # Retry settings
    task_default_retry_delay=60,
    task_max_retries=settings.task_max_retries,
)

logger.info("Celery worker configured successfully")
