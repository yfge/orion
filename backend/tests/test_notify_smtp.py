from unittest.mock import patch
from sqlalchemy.orm import sessionmaker
from backend.app.db.models import SendRecord, SendDetail


def setup_smtp_endpoint_and_message(client):
    rs = client.post("/api/v1/systems", json={"name": "sys-smtp"})
    sys_bid = rs.json()["business_system_bid"]
    re = client.post(f"/api/v1/systems/{sys_bid}/endpoints", json={
        "name": "smtp-out",
        "transport": "smtp",
        "adapter_key": "smtp.generic",
        "endpoint_url": None,
        "config": {"host": "smtp.example.com", "port": 587, "use_tls": True, "from": "noreply@example.com", "to": "alice@example.com"},
        "status": 1,
    })
    ep_bid = re.json()["notification_api_bid"]
    rm = client.post("/api/v1/message-definitions", json={
        "name": "mail-text",
        "type": "email",
        "schema": {"subject": "Test ${text}", "text": "${text}"},
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


def test_notify_smtp(client, engine):
    msg_bid = setup_smtp_endpoint_and_message(client)

    class DummySmtp:
        def send(self, *, endpoint, payload):
            # assert minimal fields
            assert payload.get("subject", "").startswith("Test")
            assert payload.get("text") == "hi"
            return {"status_code": 250, "body": {"ok": True}}

    with patch("backend.app.services.notify.SmtpSender", return_value=DummySmtp()):
        # snapshot counts
        Session = sessionmaker(bind=engine, future=True)
        with Session() as s:
            before_sr = s.query(SendRecord).count()
            before_sd = s.query(SendDetail).count()
        r = client.post("/api/v1/notify/", json={"message_definition_bid": msg_bid, "data": {"text": "hi"}}, headers={"X-API-Key": "test"})
        assert r.status_code == 200
        res = r.json()["results"]
        assert len(res) == 1
        assert res[0]["status_code"] == 250
        with Session() as s:
            assert s.query(SendRecord).count() == before_sr + 1
            assert s.query(SendDetail).count() == before_sd + 1
