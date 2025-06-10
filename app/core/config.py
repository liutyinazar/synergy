import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGODB_URL: Optional[str] = None
    REDIS_URL: Optional[str] = None
    API_BASE_URL: Optional[str] = None
    DATABASE_NAME: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env.test" if os.getenv("TESTING") else ".env"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
