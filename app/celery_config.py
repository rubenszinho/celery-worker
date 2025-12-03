
import logging

from app.config import settings
from celery import Celery

logger = logging.getLogger(__name__)


celery_app = Celery(
    "worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks"],  
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    result_expires=86400,  
    
    worker_prefetch_multiplier=settings.worker_prefetch_multiplier,
    worker_max_tasks_per_child=settings.worker_max_tasks_per_child,
    worker_concurrency=settings.worker_concurrency,
    
    task_acks_late=settings.task_acks_late,
    task_reject_on_worker_lost=settings.task_reject_on_worker_lost,
    task_track_started=True,
    
    task_default_retry_delay=60,
    task_max_retries=settings.task_max_retries,
)

logger.info("Celery worker configured successfully")
