import base64

from fastapi import Header, HTTPException

from ..core.config import settings


def _check_basic_auth(auth_header: str | None, expected: str) -> bool:
    if not auth_header:
        return False
    try:
        parts = auth_header.split(" ", 1)
        if len(parts) != 2:
            return False
        scheme, token = parts[0], parts[1]
        if scheme.lower() != "basic":
            return False
        decoded = base64.b64decode(token).decode("utf-8", errors="ignore")
        # Accept formats: "api:<key>" (Mailgun style), or ":<key>" (empty user)
        if ":" not in decoded:
            return False
        username, password = decoded.split(":", 1)
        if password == expected and (username == "api" or username == "" or username == "key"):
            return True
        return False
    except Exception:
        return False


def _check_bearer_auth(auth_header: str | None, expected: str) -> bool:
    if not auth_header:
        return False
    try:
        parts = auth_header.split(" ", 1)
        if len(parts) != 2:
            return False
        scheme, token = parts[0], parts[1]
        if scheme.lower() != "bearer":
            return False
        return token == expected
    except Exception:
        return False


def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> None:
    expected = settings.PUBLIC_API_KEY
    if expected is None:
        # If not configured, allow for now (could be tightened later)
        return
    if x_api_key == expected:
        return
    if _check_bearer_auth(authorization, expected):
        return
    if _check_basic_auth(authorization, expected):
        return
    raise HTTPException(status_code=401, detail="Invalid API key")
