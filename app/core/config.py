from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    REDIS_URL: str = "redis://localhost:6379/0"
    API_BASE_URL: str = "https://fakerapi.it/api/v2"
    DATABASE_NAME: str = "user_data_db"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
