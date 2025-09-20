import base64
from unittest.mock import patch

import httpx

from backend.app.services.sender.http_sender import HttpSender


def test_http_sender_mailgun_form_and_basic_auth(monkeypatch):
    sender = HttpSender()
    endpoint = {
        "adapter_key": "http.mailgun",
        "endpoint_url": "https://api.mailgun.net/v3/example.com/messages",
        "config": {
            "url": "https://api.mailgun.net/v3/example.com/messages",
            "api_key": "key-123456",
            "timeout": 5,
        },
    }
    payload = {
        "from": "noreply@example.com",
        "to": "alice@example.com",
        "subject": "Hi",
        "text": "Hello",
    }

    captured = {}

    def fake_request(self, method, url, headers=None, params=None, json=None, data=None):  # type: ignore[no-redef]
        captured["method"] = method
        captured["url"] = url
        captured["headers"] = headers or {}
        captured["params"] = params or {}
        captured["json"] = json
        captured["data"] = data
        class R:
            status_code = 200
            headers = {"content-type": "application/json"}
            def json(self):
                return {"ok": True}
            @property
            def text(self):
                return "ok"
        return R()

    with patch.object(httpx.Client, "request", new=fake_request):
        res = sender.send(endpoint=endpoint, payload=payload)

    assert res["status_code"] == 200
    assert captured["method"] == "POST"
    assert captured["url"].endswith("/messages")
    # Should use form-encoded, not JSON
    assert captured["json"] is None
    assert captured["data"] == payload
    # Basic auth header present
    auth = captured["headers"].get("Authorization")
    assert auth and auth.startswith("Basic ")
    token = auth.split()[1]
    decoded = base64.b64decode(token).decode()
    assert decoded == "api:key-123456"
    # Content-Type should be x-www-form-urlencoded
    assert captured["headers"].get("Content-Type", "").startswith("application/x-www-form-urlencoded")

