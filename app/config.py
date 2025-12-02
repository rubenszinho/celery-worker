"""
Configuration management using pydantic-settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Worker settings loaded from environment variables."""

    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"

    # Celery Configuration
    celery_broker_url: str = ""  # Will default to redis_url if not set
    celery_result_backend: str = ""  # Will default to redis_url if not set

    # Worker Configuration
    worker_concurrency: int = 4
    worker_prefetch_multiplier: int = 1
    worker_max_tasks_per_child: int = 1000

    # Task Configuration
    task_acks_late: bool = True
    task_reject_on_worker_lost: bool = True
    task_max_retries: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_broker_url(self) -> str:
        """Get Celery broker URL (defaults to Redis)."""
        return self.celery_broker_url or self.redis_url

    def get_result_backend(self) -> str:
        """Get Celery result backend URL (defaults to Redis)."""
        return self.celery_result_backend or self.redis_url


# Global settings instance
settings = Settings()
