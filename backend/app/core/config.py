from functools import lru_cache
import json
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="ORION_")

    APP_NAME: str = "Orion"
    ENV: str = "dev"
    DEBUG: bool = True

    # Example: sqlite:///./orion.db or postgresql+psycopg://user:pass@host:5432/db
    DATABASE_URL: str = "sqlite:///./orion.db"

    # Security
    SECRET_KEY: str | None = None

    # CORS (supports '*', comma-separated, or JSON array via env); if empty, use sensible dev defaults in app
    CORS_ORIGINS: list[str] | str | None = []

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _parse_cors(cls, v):
        if v is None or v == "" or v == []:
            return []
        if isinstance(v, str):
            s = v.strip()
            if s == "*":
                return ["*"]
            # try JSON array first
            try:
                data = json.loads(s)
                if isinstance(data, list):
                    return [str(x) for x in data]
            except Exception:
                pass
            # fallback: comma-separated
            return [i.strip() for i in s.split(",") if i.strip()]
        if isinstance(v, (list, tuple)):
            return [str(x) for x in v]
        return []


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
