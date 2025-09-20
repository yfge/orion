from unittest.mock import patch

import httpx

from backend.app.services.sender.http_sender import HttpSender


def test_http_sender_sendgrid_bearer_and_json():
    sender = HttpSender()
    endpoint = {
        "adapter_key": "http.sendgrid",
        "endpoint_url": "https://api.sendgrid.com/v3/mail/send",
        "config": {
            "url": "https://api.sendgrid.com/v3/mail/send",
            "api_key": "SG.xxxxxx",
            "timeout": 8,
        },
    }
    payload = {
        "personalizations": [{"to": [{"email": "alice@example.com"}]}],
        "from": {"email": "noreply@example.com"},
        "subject": "Hi",
        "content": [{"type": "text/plain", "value": "Hello"}],
    }

    captured = {}

    def fake_request(self, method, url, headers=None, params=None, json=None, data=None):  # type: ignore[no-redef]
        captured["method"] = method
        captured["url"] = url
        captured["headers"] = headers or {}
        captured["json"] = json
        captured["data"] = data
        class R:
            status_code = 202
            headers = {"content-type": "text/plain"}
            @property
            def text(self):
                return "accepted"
        return R()

    with patch.object(httpx.Client, "request", new=fake_request):
        res = sender.send(endpoint=endpoint, payload=payload)

    assert res["status_code"] == 202
    assert captured["url"].endswith("/mail/send")
    # Should use JSON for SendGrid
    assert captured["json"] == payload
    assert captured["data"] is None
    assert captured["headers"].get("Authorization") == "Bearer SG.xxxxxx"

