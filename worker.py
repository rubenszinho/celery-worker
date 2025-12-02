"""
Celery Worker Entrypoint

This script is the entry point for starting Celery workers.
"""

from app.celery_config import celery_app

# Import tasks to register them with Celery
from app.tasks import (
    async_processing_task,
    batch_processing_task,
    database_task,
    example_task,
    long_running_task,
)

if __name__ == "__main__":
    celery_app.start()
