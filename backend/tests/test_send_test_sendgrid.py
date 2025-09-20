from unittest.mock import patch


def test_endpoints_send_test_sendgrid(client, monkeypatch):
    # Create business system
    r = client.post("/api/v1/systems/", json={"name": "sys2"})
    assert r.status_code == 201
    sys_bid = r.json()["business_system_bid"]

    # Create sendgrid endpoint
    ep_payload = {
        "name": "sg",
        "transport": "http",
        "adapter_key": "http.sendgrid",
        "endpoint_url": "https://api.sendgrid.com/v3/mail/send",
        "config": {
            "url": "https://api.sendgrid.com/v3/mail/send",
            "api_key": "SG.key",
            "from": "noreply@example.com",
            "to": "bob@example.com",
        },
    }
    r = client.post(f"/api/v1/systems/{sys_bid}/endpoints", json=ep_payload)
    assert r.status_code == 201
    ep_bid = r.json()["notification_api_bid"]

    captured = {}

    def fake_send(self, *, endpoint, payload):  # type: ignore[no-redef]
        captured["payload"] = payload
        return {"status_code": 202, "body": "accepted"}

    with patch("backend.app.api.v1.endpoints.HttpSender.send", new=fake_send):
        r = client.post(f"/api/v1/endpoints/{ep_bid}/send-test", json={"text": "Hello SG"})
        assert r.status_code == 200
        p = captured["payload"]
        assert p["from"]["email"] == "noreply@example.com"
        assert p["personalizations"][0]["to"][0]["email"] == "bob@example.com"
        assert p["content"][0]["value"] == "Hello SG"

