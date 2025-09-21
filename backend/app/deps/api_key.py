import base64

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ..core.config import settings
from ..deps.db import get_db
from ..repository import api_keys as keys_repo


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
    db: Session = Depends(get_db),
) -> None:
    expected = settings.PUBLIC_API_KEY
    if expected is None:
        # If not configured, allow for now (could be tightened later)
        return
    if x_api_key == expected:
        return
    # Try Bearer/Basic against env key
    if _check_bearer_auth(authorization, expected) or _check_basic_auth(authorization, expected):
        return
    # If request provided any key, check DB api_keys
    provided = None
    if x_api_key:
        provided = x_api_key
    else:
        # try parse from Authorization if any
        try:
            parts = (authorization or "").split(" ", 1)
            if len(parts) == 2:
                scheme, token = parts[0].lower(), parts[1]
                if scheme in ("bearer", "basic"):
                    if scheme == "basic":
                        # decode and take password part
                        import base64

                        decoded = base64.b64decode(token).decode("utf-8", errors="ignore")
                        if ":" in decoded:
                            provided = decoded.split(":", 1)[1]
                    else:
                        provided = token
        except Exception:
            provided = None
    if provided and keys_repo.exists_by_token(db, token=provided):
        return
    raise HTTPException(status_code=401, detail="Invalid API key")
