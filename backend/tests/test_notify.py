from unittest.mock import patch


def setup_system_endpoint_and_message(client):
    rs = client.post("/api/v1/systems", json={"name": "sys-a", "base_url": "https://a.example.com"})
    sys_bid = rs.json()["business_system_bid"]
    re = client.post(f"/api/v1/systems/{sys_bid}/endpoints", json={
        "name": "feishu-webhook",
        "transport": "http",
        "adapter_key": "http.feishu_bot",
        "endpoint_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
        "config": {"timeout": 5},
        "status": 1,
    })
    ep_bid = re.json()["notification_api_bid"]
    rm = client.post("/api/v1/message-definitions", json={
        "name": "simple-text",
        "type": "text",
        "schema": {"msg_type": "text", "content": {"text": "${text}"}},
        "status": 1,
    })
    msg_bid = rm.json()["message_definition_bid"]
    rd = client.post(f"/api/v1/message-definitions/{msg_bid}/dispatches", json={
        "endpoint_bid": ep_bid,
        "mapping": {},
        "enabled": True,
    })
    assert rd.status_code == 201
    return msg_bid


def test_notify_by_name(client, monkeypatch):
    msg_bid = setup_system_endpoint_and_message(client)

    class DummySender:
        def send(self, *, endpoint, payload):
            return {"status_code": 200, "body": {"ok": True, "payload": payload}}

    with patch("backend.app.services.notify.HttpSender", return_value=DummySender()):
        r = client.post("/api/v1/notify/", json={"message_name": "simple-text", "data": {"text": "hi"}}, headers={"X-API-Key": "test"})
        # default: PUBLIC_API_KEY is None, dependency allows
        assert r.status_code == 200, r.text
        res = r.json()["results"]
        assert len(res) == 1
        assert res[0]["status_code"] == 200

