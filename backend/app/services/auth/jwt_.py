from __future__ import annotations

from typing import Any
from datetime import datetime, timedelta, timezone

import jwt

from .base import AuthProvider


class JWTSignerProvider(AuthProvider):
    def __init__(self, config: dict[str, Any]) -> None:
        self.iss: str | None = config.get("iss")
        self.kid: str | None = config.get("kid")
        self.private_key: str | None = config.get("private_key")
        self.algorithm: str = config.get("algorithm", "RS256")
        self.ttl_seconds: int = int(config.get("ttl_seconds", 300))
        self.claims_template: dict[str, Any] = config.get("claims_template") or {}

    def apply(self, request: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        claims = {**self.claims_template}
        claims.setdefault("iat", int(now.timestamp()))
        claims.setdefault("exp", int((now + timedelta(seconds=self.ttl_seconds)).timestamp()))
        if self.iss:
            claims.setdefault("iss", self.iss)
        headers: dict[str, Any] = {}
        if self.kid:
            headers["kid"] = self.kid
        token = jwt.encode(claims, self.private_key or "", algorithm=self.algorithm, headers=headers or None)
        hdrs = dict(request.get("headers") or {})
        hdrs["Authorization"] = f"Bearer {token}"
        return {**request, "headers": hdrs}

