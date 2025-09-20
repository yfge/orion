from unittest.mock import patch


def test_endpoints_send_test_smtp(client):
    # Create business system
    r = client.post("/api/v1/systems/", json={"name": "sys3"})
    assert r.status_code == 201
    sys_bid = r.json()["business_system_bid"]

    # Create smtp endpoint
    ep_payload = {
        "name": "smtp",
        "transport": "smtp",
        "adapter_key": "smtp.generic",
        "endpoint_url": None,
        "config": {
            "host": "smtp.example.com",
            "port": 587,
            "use_tls": True,
            "from": "noreply@example.com",
            "to": "test@example.com",
        },
    }
    r = client.post(f"/api/v1/systems/{sys_bid}/endpoints", json=ep_payload)
    assert r.status_code == 201
    ep_bid = r.json()["notification_api_bid"]

    captured = {}

    def fake_send(self, *, endpoint, payload):  # type: ignore[no-redef]
        captured["endpoint"] = endpoint
        captured["payload"] = payload
        return {"status_code": 250, "body": {}}

    with patch("backend.app.api.v1.endpoints.SmtpSender.send", new=fake_send):
        r = client.post(f"/api/v1/endpoints/{ep_bid}/send-test", json={"text": "Hello SMTP"})
        assert r.status_code == 200
        p = captured["payload"]
        assert p["from"] == "noreply@example.com"
        assert p["to"] == "test@example.com"
        assert p["text"] == "Hello SMTP"

