from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class AuthProvider(ABC):
    @abstractmethod
    def apply(self, request: dict[str, Any]) -> dict[str, Any]:
        """
        Given a request descriptor {method, url, headers, query, body},
        return a new descriptor with auth applied (e.g., Authorization header, signature).
        """


class NoAuth(AuthProvider):
    def apply(self, request: dict[str, Any]) -> dict[str, Any]:
        return request


def build_auth_provider(kind: Optional[str], config: Optional[dict[str, Any]] = None) -> AuthProvider:
    kind = (kind or "none").lower()
    if kind in ("none", "disabled"):
        return NoAuth()
    if kind == "oauth2_client_credentials":
        from .oauth2 import OAuth2CCProvider

        return OAuth2CCProvider(config or {})
    if kind == "hmac":
        from .hmac_ import HMACProvider

        return HMACProvider(config or {})
    if kind == "jwt":
        from .jwt_ import JWTSignerProvider

        return JWTSignerProvider(config or {})
    # Fallback
    return NoAuth()

