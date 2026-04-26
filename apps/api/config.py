"""Application settings loaded from environment."""
import os
from dataclasses import dataclass



DEFAULT_PAGE_SIZE = 20

DEFAULT_PAGE_SIZE = 20

@dataclass
class Settings:
    database_url: str = os.environ.get("DATABASE_URL", "postgresql://localhost/tsbench")
    secret_key: str = os.environ.get("SECRET_KEY", "dev-secret")
    stripe_api_key: str = os.environ.get("STRIPE_API_KEY", "")
    stripe_webhook_secret: str = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    redis_url: str = os.environ.get("REDIS_URL", "redis://localhost:6379")
    log_level: str = os.environ.get("LOG_LEVEL", "INFO")
    allowed_origins: str = os.environ.get("ALLOWED_ORIGINS", "*")
    # UNDECL-001 / UNDECL-002 planted later
    max_page_size: int = int(os.environ.get("MAX_PAGE_SIZE", "100"))
    default_page_size: int = int(os.environ.get("DEFAULT_PAGE_SIZE", str(DEFAULT_PAGE_SIZE)))


settings = Settings()
