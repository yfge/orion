def test_systems_crud_and_search(client):
    # create
    r = client.post("/api/v1/systems", json={
        "name": "app-foo",
        "base_url": "https://foo.example.com",
        "auth_method": "token",
        "app_id": "id1",
        "app_secret": "sec1",
        "status": 1,
    })
    assert r.status_code == 201, r.text
    sys1 = r.json()
    assert sys1["name"] == "app-foo"
    bid = sys1["business_system_bid"]

    # get
    r = client.get(f"/api/v1/systems/{bid}")
    assert r.status_code == 200
    got = r.json()
    assert got["name"] == "app-foo"

    # list
    r = client.get("/api/v1/systems?limit=50&offset=0")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] >= 1
    assert any(it["business_system_bid"] == bid for it in data["items"])

    # search
    r = client.get("/api/v1/systems?q=app-")
    assert r.status_code == 200
    data = r.json()
    assert any(it["business_system_bid"] == bid for it in data["items"])

    # update
    r = client.patch(f"/api/v1/systems/{bid}", json={"name": "app-foo-2", "status": 2})
    assert r.status_code == 200
    assert r.json()["name"] == "app-foo-2"
    assert r.json()["status"] == 2

    # delete (soft)
    r = client.delete(f"/api/v1/systems/{bid}")
    assert r.status_code == 204

    # get after delete -> 404
    r = client.get(f"/api/v1/systems/{bid}")
    assert r.status_code == 404

    # not listed anymore
    r = client.get("/api/v1/systems")
    assert r.status_code == 200
    assert not any(it["business_system_bid"] == bid for it in r.json()["items"])

