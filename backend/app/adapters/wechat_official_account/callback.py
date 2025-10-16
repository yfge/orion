from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import Any
from xml.etree import ElementTree

from ...core.config import settings
from ...domain.notifications import WechatCallbackEvent

logger = logging.getLogger(__name__)


class CallbackVerifier:
    """Validates and parses WeChat Official Account callback messages."""

    def __init__(self, *, token: str | None = None) -> None:
        cfg = settings.WECHAT_OFFICIAL_ACCOUNT
        self._token = token or cfg.token
        if not self._token:
            raise ValueError("wechat callback token is not configured")

    def verify_signature(self, *, signature: str, timestamp: str, nonce: str) -> bool:
        expected = _compute_signature(self._token, timestamp, nonce)
        valid = expected == signature
        logger.debug(
            "wechat callback signature check",
            extra={"expected": expected, "received": signature, "timestamp": timestamp, "nonce": nonce, "valid": valid},
        )
        return valid

    def decrypt_if_needed(self, *, encrypt_type: str | None, body: str, msg_signature: str | None = None) -> str:
        if encrypt_type and encrypt_type.lower() == "aes":
            raise NotImplementedError("AES encrypted callbacks are not yet supported")
        return body

    def to_event(self, *, payload: dict[str, Any], raw_message: str) -> WechatCallbackEvent:
        event_type = (payload.get("Event") or payload.get("MsgType") or "unknown").lower()
        vendor_msg_id = payload.get("MsgID") or payload.get("MsgId") or payload.get("MsgID")
        message_id = vendor_msg_id
        status_text = payload.get("Status") or payload.get("status")
        error_code = None
        if payload.get("ErrorCode"):
            try:
                error_code = int(payload["ErrorCode"])
            except (TypeError, ValueError):
                error_code = None
        error_message = payload.get("ErrorMsg") or payload.get("errmsg")
        try:
            occur_ts = int(payload.get("CreateTime") or 0)
        except (TypeError, ValueError):
            occur_ts = 0
        occurred_at = (
            datetime.fromtimestamp(occur_ts, timezone.utc)
            if occur_ts
            else datetime.now(timezone.utc)
        )
        return WechatCallbackEvent(
            event_type=event_type,
            message_id=message_id,
            vendor_msg_id=vendor_msg_id,
            occurred_at=occurred_at,
            payload=payload,
            raw_message=raw_message,
        )


def _compute_signature(token: str, timestamp: str, nonce: str) -> str:
    values = sorted([token, timestamp, nonce])
    sha = hashlib.sha1()
    sha.update("".join(values).encode("utf-8"))
    return sha.hexdigest()


def parse_xml_message(body: str) -> dict[str, Any]:
    try:
        root = ElementTree.fromstring(body)
    except ElementTree.ParseError as exc:  # pragma: no cover - defensive
        logger.error("failed to parse wechat callback xml", exc_info=exc)
        raise ValueError("Invalid WeChat callback XML") from exc
    data: dict[str, Any] = {}
    for child in root:
        data[child.tag] = child.text or ""
    return data
