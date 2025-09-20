from unittest.mock import patch

def test_endpoints_send_test_mailgun(client, monkeypatch):

    # Create business system
    r = client.post("/api/v1/systems/", json={"name": "sys1"})
    assert r.status_code == 201
    sys_bid = r.json()["business_system_bid"]

    # Create mailgun endpoint
    ep_payload = {
        "name": "mg",
        "transport": "http",
        "adapter_key": "http.mailgun",
        "endpoint_url": "https://api.mailgun.net/v3/example.com/messages",
        "config": {
            "url": "https://api.mailgun.net/v3/example.com/messages",
            "api_key": "key-123",
            "from": "noreply@example.com",
            "to": "alice@example.com",
        },
    }
    r = client.post(f"/api/v1/systems/{sys_bid}/endpoints", json=ep_payload)
    assert r.status_code == 201
    ep_bid = r.json()["notification_api_bid"]

    captured = {}

    def fake_send(self, *, endpoint, payload):  # type: ignore[no-redef]
        captured["endpoint"] = endpoint
        captured["payload"] = payload
        return {"status_code": 200, "body": {"ok": True}}

    with patch("backend.app.services.notify.HttpSender", autospec=True), \
         patch("backend.app.api.v1.endpoints.HttpSender.send", new=fake_send):
        r = client.post(f"/api/v1/endpoints/{ep_bid}/send-test", json={"text": "Hello"})
        assert r.status_code == 200
        assert captured["payload"]["to"] == "alice@example.com"
        assert captured["payload"]["text"] == "Hello"
