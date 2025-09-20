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
        adapter_key: str = (endpoint.get("adapter_key") or "").lower()

        # Body format: json (default) or form (urlencoded). Mailgun prefers form.
        body_format: str = (cfg.get("body_format") or ("form" if adapter_key.startswith("http.mailgun") else "json")).lower()

        # Basic auth support via config.basic_auth {username,password}
        basic = cfg.get("basic_auth") or {}
        # Mailgun convenience: if api_key given, use api:API_KEY
        if adapter_key.startswith("http.mailgun") and not basic and cfg.get("api_key"):
            basic = {"username": "api", "password": cfg.get("api_key")}
        if basic.get("username") and basic.get("password"):
            import base64

            token = base64.b64encode(f"{basic['username']}:{basic['password']}".encode()).decode()
            headers.setdefault("Authorization", f"Basic {token}")

        # SendGrid convenience: Bearer token via config.api_key
        if adapter_key.startswith("http.sendgrid") and cfg.get("api_key"):
            headers.setdefault("Authorization", f"Bearer {cfg.get('api_key')}")

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

        if body_format == "json":
            req_desc["body_bytes"] = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        else:
            # form-encoded canonical bytes for signing
            from urllib.parse import urlencode

            req_desc["body_bytes"] = urlencode(payload or {}, doseq=True).encode("utf-8")

        provider = build_auth_provider(auth_type, auth_cfg)
        req_desc = provider.apply(req_desc)

        with httpx.Client(timeout=cfg.get("timeout", 10)) as client:
            if body_format == "json":
                resp = client.request(method, url, headers=req_desc.get("headers"), params=params, json=payload)
            else:
                # ensure content-type
                hdrs = dict(req_desc.get("headers") or {})
                hdrs.setdefault("Content-Type", "application/x-www-form-urlencoded")
                resp = client.request(method, url, headers=hdrs, params=params, data=payload)
            return {"status_code": resp.status_code, "body": resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text}
