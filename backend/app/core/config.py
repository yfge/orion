from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="ORION_")

    APP_NAME: str = "Orion"
    ENV: str = "dev"
    DEBUG: bool = True

    # Example: sqlite:///./orion.db or postgresql+psycopg://user:pass@host:5432/db
    DATABASE_URL: str = "sqlite:///./orion.db"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

