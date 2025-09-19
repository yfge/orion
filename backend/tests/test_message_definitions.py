def test_message_definitions_crud(client):
    # create
    r = client.post("/api/v1/message-definitions", json={
        "name": "feishu-text",
        "type": "text",
        "schema": {"msg_type": "text", "content": {"text": "${text}"}},
        "status": 1,
    })
    assert r.status_code == 201, r.text
    obj = r.json()
    bid = obj["message_definition_bid"]

    # get
    r = client.get(f"/api/v1/message-definitions/{bid}")
    assert r.status_code == 200
    assert r.json()["name"] == "feishu-text"

    # list
    r = client.get("/api/v1/message-definitions?limit=20&offset=0&q=feishu")
    assert r.status_code == 200
    data = r.json()
    assert any(i["message_definition_bid"] == bid for i in data["items"])

    # update
    r = client.patch(f"/api/v1/message-definitions/{bid}", json={"name": "feishu-text-2", "status": 2})
    assert r.status_code == 200
    assert r.json()["name"] == "feishu-text-2"
    assert r.json()["status"] == 2

    # delete
    r = client.delete(f"/api/v1/message-definitions/{bid}")
    assert r.status_code == 204

    # 404 after delete
    r = client.get(f"/api/v1/message-definitions/{bid}")
    assert r.status_code == 404

