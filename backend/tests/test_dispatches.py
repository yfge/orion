def test_dispatch_crud(client):
    # create a business system
    rs = client.post("/api/v1/systems", json={"name": "sys-a", "base_url": "https://a.example.com"})
    assert rs.status_code == 201
    sys_bid = rs.json()["business_system_bid"]

    # create endpoint under system
    re = client.post(f"/api/v1/systems/{sys_bid}/endpoints", json={
        "name": "feishu-webhook",
        "transport": "http",
        "adapter_key": "http.feishu_bot",
        "endpoint_url": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
        "config": {"timeout": 5},
        "status": 1,
    })
    assert re.status_code == 201, re.text
    ep_bid = re.json()["notification_api_bid"]

    # create message definition
    rm = client.post("/api/v1/message-definitions", json={
        "name": "text-msg",
        "type": "text",
        "schema": {"msg_type": "text", "content": {"text": "${text}"}},
        "status": 1,
    })
    assert rm.status_code == 201
    msg_bid = rm.json()["message_definition_bid"]

    # create dispatch (message -> endpoint)
    rd = client.post(f"/api/v1/message-definitions/{msg_bid}/dispatches", json={
        "endpoint_bid": ep_bid,
        "mapping": {"text": "hello"},
        "enabled": True,
    })
    assert rd.status_code == 201, rd.text
    disp_bid = rd.json()["message_dispatch_bid"]

    # list by message
    rlist = client.get(f"/api/v1/message-definitions/{msg_bid}/dispatches")
    assert rlist.status_code == 200
    assert any(d["message_dispatch_bid"] == disp_bid for d in rlist.json()["items"])

    # list endpoints (global)
    rg = client.get("/api/v1/endpoints")
    assert rg.status_code == 200
    assert any(e["notification_api_bid"] == ep_bid for e in rg.json()["items"])

    # list by endpoint
    rle = client.get(f"/api/v1/endpoints/{ep_bid}/dispatches")
    assert rle.status_code == 200
    assert any(d["message_dispatch_bid"] == disp_bid for d in rle.json()["items"])

    # update dispatch
    ru = client.patch(f"/api/v1/dispatches/{disp_bid}", json={"enabled": False})
    assert ru.status_code == 200
    assert ru.json()["enabled"] is False

    # delete dispatch
    rdel = client.delete(f"/api/v1/dispatches/{disp_bid}")
    assert rdel.status_code == 204

    # ensure deleted
    rle2 = client.get(f"/api/v1/message-definitions/{msg_bid}/dispatches")
    assert rle2.status_code == 200
    assert not any(d["message_dispatch_bid"] == disp_bid for d in rle2.json()["items"])

