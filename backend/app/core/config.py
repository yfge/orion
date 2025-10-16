from __future__ import annotations

from functools import lru_cache
import json

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _wechat_retryable_error_codes() -> list[int]:
    return [-1, 45009, 50002]


def _wechat_non_retryable_error_codes() -> list[int]:
    return [40001, 40003, 40037, 41028, 41029, 42001, 48001, 48002]


class RetryPolicyConfig(BaseModel):
    max_attempts: int = 3
    initial_interval_seconds: float = 0.5
    max_interval_seconds: float = 30.0
    multiplier: float = 2.0
    jitter: float = 0.1


class RateLimitConfig(BaseModel):
    requests_per_minute: int = 400
    burst_size: int = 40


class CircuitBreakerConfig(BaseModel):
    failure_rate_threshold: float = Field(0.5, ge=0.0, le=1.0)
    recovery_timeout_seconds: int = 60
    minimum_calls: int = 20


class WechatOfficialAccountAPIConfig(BaseModel):
    base_url: AnyHttpUrl = Field(
        "https://api.weixin.qq.com",
        description="WeChat Official Account API base domain.",
    )
    token_endpoint: str = "/cgi-bin/token"
    template_send_endpoint: str = "/cgi-bin/message/template/send"
    custom_send_endpoint: str = "/cgi-bin/message/custom/send"
    token_ttl_seconds: int = 7000


class WechatOfficialAccountSettings(BaseModel):
    app_id: str | None = None
    app_secret: str | None = None
    token: str | None = None
    encoding_aes_key: str | None = None
    api: WechatOfficialAccountAPIConfig = WechatOfficialAccountAPIConfig()
    rate_limit: RateLimitConfig = RateLimitConfig()
    retry_policy: RetryPolicyConfig = RetryPolicyConfig()
    circuit_breaker: CircuitBreakerConfig = CircuitBreakerConfig()
    retryable_error_codes: list[int] = Field(default_factory=_wechat_retryable_error_codes)
    non_retryable_error_codes: list[int] = Field(default_factory=_wechat_non_retryable_error_codes)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_prefix="ORION_")

    APP_NAME: str = "Orion"
    ENV: str = "dev"
    DEBUG: bool = True

    # Example: sqlite:///./orion.db or postgresql+psycopg://user:pass@host:5432/db
    DATABASE_URL: str = "sqlite:///./orion.db"

    # Security
    SECRET_KEY: str | None = None
    PUBLIC_API_KEY: str | None = None

    # CORS (supports '*', comma-separated, or JSON array via env); if empty, use sensible dev defaults in app
    CORS_ORIGINS: list[str] | str | None = []

    WECHAT_OFFICIAL_ACCOUNT: WechatOfficialAccountSettings = WechatOfficialAccountSettings()

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
