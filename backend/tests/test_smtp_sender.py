from unittest.mock import patch

from backend.app.services.sender.smtp_sender import SmtpSender


class DummySMTP:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.started_tls = False
        self.logged_in = False
        self.sent = None

    def starttls(self):
        self.started_tls = True

    def login(self, user, pwd):
        self.logged_in = (user, pwd)

    def sendmail(self, from_addr, to_addrs, msg):
        self.sent = (from_addr, to_addrs, msg)
        return {}

    def quit(self):
        pass

    def close(self):
        pass


def test_smtp_sender_tls_and_login(monkeypatch):
    captured = {}

    def fake_smtp(host, port, timeout=None):
        s = DummySMTP(host, port, timeout)
        captured["smtp"] = s
        return s

    with patch("smtplib.SMTP", new=fake_smtp):
        sender = SmtpSender()
        endpoint = {
            "adapter_key": "smtp.generic",
            "config": {
                "host": "smtp.example.com",
                "port": 587,
                "use_tls": True,
                "username": "user",
                "password": "pass",
            },
        }
        payload = {
            "from": "noreply@example.com",
            "to": "u1@example.com,u2@example.com",
            "subject": "Hi",
            "text": "Hello",
            "html": "<b>Hello</b>",
        }
        res = sender.send(endpoint=endpoint, payload=payload)

    s = captured["smtp"]
    assert s.started_tls is True
    assert s.logged_in == ("user", "pass")
    assert res["status_code"] == 250
    assert s.sent[0] == "noreply@example.com"
    assert s.sent[1] == ["u1@example.com", "u2@example.com"]

