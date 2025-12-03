
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    redis_url: str = "redis://localhost:6379/0"
    
    worker_concurrency: int = 4
    worker_prefetch_multiplier: int = 1
    worker_max_tasks_per_child: int = 1000

    
    task_acks_late: bool = True
    task_reject_on_worker_lost: bool = True
    task_max_retries: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
