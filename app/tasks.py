"""
Celery task definitions.

This module contains example tasks that demonstrate:
- Simple synchronous tasks
- Tasks with retry logic
- Tasks with error handling
- Data processing tasks
"""

import logging
import time
from typing import Any, Dict, List

from app.celery_config import celery_app
from celery import Task

logger = logging.getLogger(__name__)


@celery_app.task(name="example_task")
def example_task(message: str) -> Dict[str, Any]:
    """
    Example task that processes a simple message.

    Args:
        message: Message to process

    Returns:
        Processing result
    """
    logger.info(f"Processing message: {message}")

    # Simulate some work
    time.sleep(1)

    result = {
        "processed": message,
        "length": len(message),
        "uppercase": message.upper(),
        "timestamp": time.time(),
    }

    logger.info(f"Task completed: {result}")
    return result


@celery_app.task(name="async_processing_task", bind=True, max_retries=3)
def async_processing_task(self: Task, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example task for async data processing with retry logic.

    Args:
        data: Data dictionary to process

    Returns:
        Processed data
    """
    try:
        logger.info(f"Processing data: {data}")

        # Simulate processing
        time.sleep(2)

        # Example: validate data
        if not data:
            raise ValueError("Empty data provided")

        # Process data
        result = {
            "status": "completed",
            "input": data,
            "processed_keys": list(data.keys()),
            "timestamp": time.time(),
        }

        logger.info("Async processing completed successfully")
        return result

    except Exception as e:
        logger.error(f"Error in async_processing_task: {e}")

        # Retry with exponential backoff
        try:
            raise self.retry(exc=e, countdown=2**self.request.retries)
        except self.MaxRetriesExceededError:
            logger.error("Max retries exceeded")
            return {"status": "failed", "error": str(e), "retries_exhausted": True}


@celery_app.task(name="batch_processing_task")
def batch_processing_task(items: List[str]) -> Dict[str, Any]:
    """
    Example task for batch processing.

    Args:
        items: List of items to process

    Returns:
        Processing results
    """
    logger.info(f"Processing batch of {len(items)} items")

    results = []
    errors = []

    for idx, item in enumerate(items):
        try:
            # Simulate processing each item
            processed = item.upper()
            results.append({"index": idx, "original": item, "processed": processed})
            time.sleep(0.1)  # Simulate work
        except Exception as e:
            errors.append({"index": idx, "item": item, "error": str(e)})
            logger.error(f"Error processing item {idx}: {e}")

    return {
        "total": len(items),
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors,
        "timestamp": time.time(),
    }


@celery_app.task(name="long_running_task")
def long_running_task(duration: int = 10) -> Dict[str, Any]:
    """
    Example long-running task with progress updates.

    Args:
        duration: How long to run (seconds)

    Returns:
        Task result
    """
    logger.info(f"Starting long-running task (duration: {duration}s)")

    start_time = time.time()

    for i in range(duration):
        # Update task state
        long_running_task.update_state(
            state="PROGRESS",
            meta={
                "current": i + 1,
                "total": duration,
                "status": f"Processing step {i+1}/{duration}",
            },
        )
        time.sleep(1)

    elapsed = time.time() - start_time

    return {
        "status": "completed",
        "duration": duration,
        "actual_time": elapsed,
        "timestamp": time.time(),
    }


@celery_app.task(name="database_task")
def database_task(query: str) -> Dict[str, Any]:
    """
    Example task that simulates database operations.

    Replace this with your actual database logic.

    Args:
        query: Database query (placeholder)

    Returns:
        Query results
    """
    logger.info(f"Executing database query: {query}")

    # TODO: Replace with actual database operations
    # Example:
    # from app.database import get_db_session
    # with get_db_session() as session:
    #     result = session.execute(query)
    #     return result.fetchall()

    time.sleep(1)  # Simulate DB operation

    return {
        "status": "completed",
        "query": query,
        "rows_affected": 42,  # Placeholder
        "timestamp": time.time(),
    }


# Task error handler
@celery_app.task(bind=True)
def error_handler(self, uuid):
    """
    Error handler for failed tasks.
    """
    result = self.app.AsyncResult(uuid)
    logger.error(f"Task {uuid} failed: {result.traceback}")
