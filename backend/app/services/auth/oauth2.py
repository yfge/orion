from __future__ import annotations

from typing import Any

import time
import httpx

from .base import AuthProvider


class OAuth2CCProvider(AuthProvider):
    def __init__(self, config: dict[str, Any]) -> None:
        self.token_url: str = config.get("token_url", "")
        self.client_id: str = config.get("client_id", "")
        self.client_secret: str = config.get("client_secret", "")
        self.scope: str | None = config.get("scope")
        self.audience: str | None = config.get("audience")
        self.cache_ttl: int = int(config.get("cache_ttl", 300))
        self._cached_token: str | None = None
        self._expires_at: float = 0

    def _need_refresh(self) -> bool:
        return not self._cached_token or time.time() >= self._expires_at

    def _fetch_token(self) -> str:
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if self.scope:
            data["scope"] = self.scope
        if self.audience:
            data["audience"] = self.audience
        with httpx.Client(timeout=10) as client:
            resp = client.post(self.token_url, data=data)
            resp.raise_for_status()
            payload = resp.json()
        token = payload.get("access_token")
        ttl = int(payload.get("expires_in", self.cache_ttl))
        self._cached_token = token
        self._expires_at = time.time() + max(30, ttl - 30)
        return token

    def apply(self, request: dict[str, Any]) -> dict[str, Any]:
        if self._need_refresh():
            self._fetch_token()
        headers = dict(request.get("headers") or {})
        headers["Authorization"] = f"Bearer {self._cached_token}"
        return {**request, "headers": headers}

