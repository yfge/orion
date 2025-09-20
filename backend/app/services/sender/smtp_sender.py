from __future__ import annotations

from typing import Any
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from .base import MessageSender


class SmtpSender(MessageSender):
    def send(self, *, endpoint: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        cfg = endpoint.get("config") or {}
        host: str = cfg.get("host") or "localhost"
        port: int = int(cfg.get("port") or (465 if cfg.get("use_ssl") else 587 if cfg.get("use_tls") else 25))
        username: str | None = cfg.get("username")
        password: str | None = cfg.get("password")
        use_tls: bool = bool(cfg.get("use_tls") or False)
        use_ssl: bool = bool(cfg.get("use_ssl") or False)

        from_addr: str = (payload.get("from") or cfg.get("from") or "noreply@example.com")
        to_value = payload.get("to") or cfg.get("to") or ""
        if isinstance(to_value, str):
            to_addrs = [addr.strip() for addr in to_value.split(",") if addr.strip()]
        else:
            to_addrs = list(to_value or [])
        if not to_addrs:
            raise ValueError("SMTP requires at least one recipient in 'to'")

        subject: str = payload.get("subject") or ""
        text_body: str | None = payload.get("text")
        html_body: str | None = payload.get("html")

        # Build MIME message
        if html_body and text_body:
            msg = MIMEMultipart("alternative")
            msg.attach(MIMEText(text_body, "plain", "utf-8"))
            msg.attach(MIMEText(html_body, "html", "utf-8"))
        elif html_body:
            msg = MIMEMultipart("alternative")
            msg.attach(MIMEText(html_body, "html", "utf-8"))
        else:
            msg = MIMEText(text_body or "", _subtype="plain", _charset="utf-8")

        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = ", ".join(to_addrs)

        # Connect and send
        if use_ssl:
            smtp = smtplib.SMTP_SSL(host=host, port=port, timeout=int(cfg.get("timeout", 10)))
        else:
            smtp = smtplib.SMTP(host=host, port=port, timeout=int(cfg.get("timeout", 10)))
        try:
            if use_tls and not use_ssl:
                smtp.starttls()
            if username:
                smtp.login(username, password or "")
            failed = smtp.sendmail(from_addr, to_addrs, msg.as_string())
        finally:
            try:
                smtp.quit()
            except Exception:
                try:
                    smtp.close()
                except Exception:
                    pass

        status_code = 250 if not failed else 400
        return {"status_code": status_code, "body": {"failed": failed}}

