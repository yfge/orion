from fastapi import Header, HTTPException

from ..core.config import settings


def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    expected = settings.PUBLIC_API_KEY
    if expected is None:
        # If not configured, allow for now (could be tightened later)
        return
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid API key")

