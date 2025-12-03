# Celery Worker Template

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/fastapi-celery-beat-worker-flower?referralCode=5oF91f&utm_medium=integration&utm_source=template&utm_campaign=generic)

Production-ready Celery worker with example tasks, retry logic, error handling, and Railway deployment support.

### Manual Deployment

1. **Add Redis to your Railway project**

   ```
   New → Database → Add Redis
   ```

2. **Deploy this service**

   ```
   New → GitHub Repo → Select this repository
   ```

3. **Set environment variables**

   ```
   REDIS_URL = ${{Redis.REDIS_URL}}
   WORKER_CONCURRENCY = 4
   ```

4. **Deploy!** Railway will automatically detect the Dockerfile

### Deploy with API and Beat

For full functionality, deploy all three templates:

1. [FastAPI template](https://github.com/rubenszinho/celery-worker) (triggers tasks)
2. This Celery Worker template
3. [Celery Beat template](https://github.com/rubenszinho/celery-beat) (schedules tasks)

All should share the same Redis instance via `${{Redis.REDIS_URL}}`.

## Adding Custom Tasks

Edit `app/tasks.py`:

```python
@celery_app.task(name="your_task")
def your_task(data):
    """Your custom task logic"""
    # Process data
    result = process_data(data)
    return result
```

### Task with Retry Logic

```python
@celery_app.task(name="your_task", bind=True, max_retries=3)
def your_task(self, data):
    try:
        # Your logic
        return result
    except Exception as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
```

### Task with Progress Updates

```python
@celery_app.task(name="your_task", bind=True)
def your_task(self, items):
    for i, item in enumerate(items):
        # Update progress
        self.update_state(
            state='PROGRESS',
            meta={'current': i, 'total': len(items)}
        )
        # Process item
    return {"status": "completed"}
```

## Configuration

### Worker Concurrency

Adjust based on your workload:

```bash
# For CPU-intensive tasks
WORKER_CONCURRENCY=4

# For I/O-intensive tasks
WORKER_CONCURRENCY=10
```

### Task Timeouts

In `app/celery_config.py`:

```python
celery_app.conf.update(
    task_soft_time_limit=300,  # 5 minutes
    task_time_limit=600,       # 10 minutes
)
```

### Task Routing

Route different tasks to different queues:

```python
celery_app.conf.task_routes = {
    'app.tasks.slow_task': {'queue': 'slow'},
    'app.tasks.fast_task': {'queue': 'fast'},
}
```

## Monitoring

### Check Worker Status

```python
from app.celery_config import celery_app

inspect = celery_app.control.inspect()
print(inspect.active())      # Active tasks
print(inspect.registered())  # Registered tasks
print(inspect.stats())       # Worker stats
```

### Task Result

```python
from celery.result import AsyncResult

result = AsyncResult(task_id)
print(result.state)      # PENDING, STARTED, SUCCESS, FAILURE
print(result.info)       # Progress info
print(result.result)     # Final result
```

## Common Use Cases

Email sending, image processing, data import/export, report generation, API integrations, database cleanup.

## Troubleshooting

### Worker not starting

```bash
# Check Redis connection
redis-cli -u $REDIS_URL ping

# Check worker logs
docker-compose logs worker

# Verify dependencies
pip list | grep celery
```

### Tasks not executing

```bash
# Check if tasks are registered
celery -A worker.celery_app inspect registered

# Check active tasks
celery -A worker.celery_app inspect active

# Check worker status
celery -A worker.celery_app status
```

### Memory issues

```bash
# Reduce concurrency
WORKER_CONCURRENCY=2

# Reduce max tasks per child
WORKER_MAX_TASKS_PER_CHILD=100
```

## Performance Tips

Use batching, set timeouts, use task routing, monitor memory, enable result expiration.

## License

GPL-3.0
