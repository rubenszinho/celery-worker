# Celery Worker Template

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/celery-worker)

Production-ready Celery worker with example tasks, retry logic, error handling, and Railway deployment support.

## Quick Start

### Local Development with Docker

```bash
# Clone or copy this template
cd celery-worker-template

# Create env.example file
cp env.example .env

# Start services
docker-compose up

# Worker will start processing tasks
```

### Manual Setup

```bash
# Install dependencies
pip install .

# Or with dev dependencies
pip install -e ".[dev]"

# Start Redis (in separate terminal)
redis-server

# Start Celery Worker
celery -A worker.celery_app worker --loglevel=info
```

## Example Tasks

### 1. Simple Message Processing

```python
from app.tasks import example_task

result = example_task.delay("Hello, World!")
print(result.get())
# Output: {"processed": "Hello, World!", "length": 13, ...}
```

### 2. Async Data Processing

```python
from app.tasks import async_processing_task

data = {"user_id": 123, "action": "signup"}
result = async_processing_task.delay(data)
```

### 3. Batch Processing

```python
from app.tasks import batch_processing_task

items = ["item1", "item2", "item3"]
result = batch_processing_task.delay(items)
```

### 4. Long Running Task

```python
from app.tasks import long_running_task

result = long_running_task.delay(duration=30)
# Check progress: result.info
```

## Deploy to Railway

### One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/celery-worker)

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

1. FastAPI template (triggers tasks)
2. This Worker template (processes tasks)
3. Celery Beat template (schedules tasks)

All should share the same Redis instance via `${{Redis.REDIS_URL}}`.

## Environment Variables

| Variable                     | Required | Default                  | Description                  |
| ---------------------------- | -------- | ------------------------ | ---------------------------- |
| `REDIS_URL`                  | Yes      | redis://localhost:6379/0 | Redis connection string      |
| `CELERY_BROKER_URL`          | No       | Uses REDIS_URL           | Celery broker URL            |
| `CELERY_RESULT_BACKEND`      | No       | Uses REDIS_URL           | Celery result backend        |
| `WORKER_CONCURRENCY`         | No       | 4                        | Number of worker processes   |
| `WORKER_PREFETCH_MULTIPLIER` | No       | 1                        | Task prefetch multiplier     |
| `WORKER_MAX_TASKS_PER_CHILD` | No       | 1000                     | Max tasks per worker process |
| `TASK_MAX_RETRIES`           | No       | 3                        | Max retry attempts           |

## Project Structure

```
celery-worker-template/
├── app/
│   ├── __init__.py          # Package init
│   ├── celery_config.py     # Celery configuration
│   ├── config.py            # Environment configuration
│   └── tasks.py             # Task definitions
├── worker.py                # Worker entrypoint
├── Dockerfile               # Production container
├── docker-compose.yml       # Local development
├── pyproject.toml           # Python dependencies
├── env.example              # Environment template
├── railway.json             # Railway configuration
└── README.md               # This file
```

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

## Production Checklist

Set worker concurrency, task timeouts, error tracking, monitoring, Redis password, task routing.

## Related Templates

[FastAPI Template](../fastapi-template) | [Celery Beat Template](../celery-beat-template)

## Performance Tips

Use batching, set timeouts, use task routing, monitor memory, enable result expiration.

## License

GPL-3.0
