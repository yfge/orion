import base64


def test_notify_basic_auth_allows_when_key_set(client, monkeypatch):
    # Configure expected public API key
    from backend.app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "PUBLIC_API_KEY", "secret-key")

    # Create minimal setup (reuse existing helper by calling endpoints to create data)
    # Create system, endpoint, message, dispatch (reuse from test_notify via API)
    rs = client.post("/api/v1/systems", json={"name": "sys-basic"})
    sys_bid = rs.json()["business_system_bid"]
    re = client.post(
        f"/api/v1/systems/{sys_bid}/endpoints",
        json={
            "name": "feishu",
            "transport": "http",
            "adapter_key": "http.feishu_bot",
            "endpoint_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
            "config": {},
            "status": 1,
        },
    )
    ep_bid = re.json()["notification_api_bid"]
    rm = client.post(
        "/api/v1/message-definitions",
        json={
            "name": "basic-text",
            "type": "text",
            "schema": {"msg_type": "text", "content": {"text": "${text}"}},
            "status": 1,
        },
    )
    msg_bid = rm.json()["message_definition_bid"]
    rd = client.post(
        f"/api/v1/message-definitions/{msg_bid}/dispatches",
        json={"endpoint_bid": ep_bid, "mapping": {}, "enabled": True},
    )
    assert rd.status_code == 201

    # Send with Basic auth (user=api, pass=secret-key)
    token = base64.b64encode(b"api:secret-key").decode()
    r = client.post(
        "/api/v1/notify/",
        json={"message_name": "basic-text", "data": {"text": "hi"}},
        headers={"Authorization": f"Basic {token}"},
    )
    # Only check that auth passed (not 401). Outbound may vary (200/502)
    assert r.status_code != 401


def test_notify_x_api_key_allows_when_key_set(client, monkeypatch):
    from backend.app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "PUBLIC_API_KEY", "k")
    # Quick call without creating dispatch (should fail 404 for message, but 401 must not happen)
    r = client.post(
        "/api/v1/notify/",
        json={"message_name": "no-exist", "data": {}},
        headers={"X-API-Key": "k"},
    )
    # Not authorized error must not occur
    assert r.status_code != 401


def test_notify_basic_auth_rejects_wrong_key(client, monkeypatch):
    from backend.app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "PUBLIC_API_KEY", "good")
    bad = base64.b64encode(b"api:bad").decode()
    r = client.post(
        "/api/v1/notify/",
        json={"message_name": "whatever", "data": {}},
        headers={"Authorization": f"Basic {bad}"},
    )
    assert r.status_code == 401


def test_notify_bearer_auth_allows_when_key_set(client, monkeypatch):
    from backend.app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "PUBLIC_API_KEY", "bear")
    # Create minimal setup to avoid 401
    rs = client.post("/api/v1/systems", json={"name": "sys-bearer"})
    sys_bid = rs.json()["business_system_bid"]
    re = client.post(
        f"/api/v1/systems/{sys_bid}/endpoints",
        json={
            "name": "feishu",
            "transport": "http",
            "adapter_key": "http.feishu_bot",
            "endpoint_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
            "config": {},
            "status": 1,
        },
    )
    ep_bid = re.json()["notification_api_bid"]
    rm = client.post(
        "/api/v1/message-definitions",
        json={
            "name": "bearer-text",
            "type": "text",
            "schema": {"msg_type": "text", "content": {"text": "${text}"}},
            "status": 1,
        },
    )
    msg_bid = rm.json()["message_definition_bid"]
    client.post(
        f"/api/v1/message-definitions/{msg_bid}/dispatches",
        json={"endpoint_bid": ep_bid, "mapping": {}, "enabled": True},
    )

    r = client.post(
        "/api/v1/notify/",
        json={"message_name": "bearer-text", "data": {"text": "hi"}},
        headers={"Authorization": "Bearer bear"},
    )
    assert r.status_code != 401


def test_notify_bearer_auth_rejects_wrong_key(client, monkeypatch):
    from backend.app.core import config as cfg

    monkeypatch.setattr(cfg.settings, "PUBLIC_API_KEY", "good")
    r = client.post(
        "/api/v1/notify/",
        json={"message_name": "whatever", "data": {}},
        headers={"Authorization": "Bearer bad"},
    )
    assert r.status_code == 401


def test_preview_key_endpoint(client):
    r = client.post("/api/v1/notify/keys/preview")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data.get("key"), str) and len(data["key"]) >= 16
