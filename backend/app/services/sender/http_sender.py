from __future__ import annotations

from typing import Any

import httpx

from ..auth.base import build_auth_provider
from .base import MessageSender


class HttpSender(MessageSender):
    def send(self, *, endpoint: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        cfg = endpoint.get("config") or {}
        method: str = (cfg.get("method") or "POST").upper()
        url: str = cfg.get("url") or endpoint.get("endpoint_url")
        headers = dict(cfg.get("headers") or {})
        params = dict(cfg.get("query") or {})
        auth_type = endpoint.get("auth_type") or endpoint.get("auth") or None
        auth_cfg = endpoint.get("auth_config") or {}

        req_desc = {
            "method": method,
            "url": url,
            "headers": headers,
            "query": params,
            "body": payload,
            "body_bytes": None,
        }
        # naive JSON encode to sign
        import json

        req_desc["body_bytes"] = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        provider = build_auth_provider(auth_type, auth_cfg)
        req_desc = provider.apply(req_desc)

        with httpx.Client(timeout=cfg.get("timeout", 10)) as client:
            resp = client.request(method, url, headers=req_desc.get("headers"), params=params, json=payload)
            return {"status_code": resp.status_code, "body": resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text}

