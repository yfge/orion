from __future__ import annotations

import hmac
import hashlib
from typing import Any

from .base import AuthProvider


class HMACProvider(AuthProvider):
    def __init__(self, config: dict[str, Any]) -> None:
        self.access_key: str = config.get("access_key", "")
        self.secret_key: str = config.get("secret_key", "")
        self.algo: str = (config.get("algo") or "sha256").lower()
        self.header_name: str = config.get("header_name", "X-Signature")

    def apply(self, request: dict[str, Any]) -> dict[str, Any]:
        body_bytes = (request.get("body_bytes") or b"")
        if self.algo == "sha256":
            digestmod = hashlib.sha256
        else:
            digestmod = hashlib.sha1
        sig = hmac.new(self.secret_key.encode(), body_bytes, digestmod).hexdigest()
        headers = dict(request.get("headers") or {})
        headers[self.header_name] = sig
        return {**request, "headers": headers}

