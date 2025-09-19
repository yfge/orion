import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import jwt
from passlib.context import CryptContext

from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_secret_key() -> str:
    # Fallback for dev; encourage setting ORION_SECRET_KEY in .env
    return getattr(settings, "SECRET_KEY", None) or "dev-secret-change-me"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(hours=1)
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    token = jwt.encode(payload, get_secret_key(), algorithm="HS256")
    return token


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, get_secret_key(), algorithms=["HS256"])  # type: ignore[no-any-return]

