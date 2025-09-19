def test_register_login_and_list_users(client):
    # register
    payload = {"username": "alice", "password": "Secret@123", "email": "a@example.com"}
    r = client.post("/api/v1/auth/register", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["username"] == "alice"

    # login
    r = client.post("/api/v1/auth/login", json={"username": "alice", "password": "Secret@123"})
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    # list users (protected)
    r = client.get("/api/v1/users/", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    users = r.json()
    assert any(u["username"] == "alice" for u in users)

