import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

try:
    import jwt  # type: ignore
except Exception:  # pragma: no cover
    jwt = None  # fallback implementation below
from passlib.context import CryptContext

from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_secret_key() -> str:
    # Fallback for dev; encourage setting ORION_SECRET_KEY in .env
    return getattr(settings, "SECRET_KEY", None) or "dev-secret-change-me"


def _truncate_password(password: str) -> str:
    """Truncate password to 72 bytes for bcrypt compatibility."""
    # bcrypt has a maximum password length of 72 bytes
    # Encode to bytes, truncate, then decode back to string
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes and decode, ignoring errors
        password_bytes = password_bytes[:72]
    return password_bytes.decode('utf-8', errors='ignore')


def hash_password(password: str) -> str:
    password = _truncate_password(password)
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    password = _truncate_password(password)
    return pwd_context.verify(password, hashed)


def _encode_jwt_hs256(payload: dict[str, Any], secret: str) -> str:  # fallback
    import json, base64, hmac, hashlib

    def b64url(data: bytes) -> bytes:
        return base64.urlsafe_b64encode(data).rstrip(b"=")

    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = b64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = header_b64 + b"." + payload_b64
    sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    token = signing_input + b"." + b64url(sig)
    return token.decode()


def _decode_jwt_hs256(token: str, secret: str) -> dict[str, Any]:  # fallback
    import json, base64, hmac, hashlib, time

    def b64url_decode(s: str) -> bytes:
        pad = '=' * (-len(s) % 4)
        return base64.urlsafe_b64decode(s + pad)

    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("invalid token")
    header_b64, payload_b64, sig_b64 = parts
    signing_input = (header_b64 + "." + payload_b64).encode()
    expected = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    import hmac as _h

    if not _h.compare_digest(expected, b64url_decode(sig_b64)):
        raise ValueError("invalid signature")
    payload = json.loads(b64url_decode(payload_b64))
    exp = payload.get("exp")
    if exp is not None and int(time.time()) >= int(exp):
        raise ValueError("token expired")
    return payload


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(hours=1)
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    secret = get_secret_key()
    if jwt is not None:
        return jwt.encode(payload, secret, algorithm="HS256")  # type: ignore
    # fallback
    return _encode_jwt_hs256(payload, secret)


def decode_token(token: str) -> dict[str, Any]:
    secret = get_secret_key()
    if jwt is not None:
        return jwt.decode(token, secret, algorithms=["HS256"])  # type: ignore[no-any-return]
    # fallback
    return _decode_jwt_hs256(token, secret)
