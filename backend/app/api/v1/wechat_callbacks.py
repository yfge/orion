from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from ...adapters.wechat_official_account.callback import CallbackVerifier, parse_xml_message
from ...observability.metrics import record_wechat_callback
from ...repository import wechat_official_account as repo
from ...deps.db import get_db

router = APIRouter(prefix="/callbacks/wechat-oa", tags=["wechat"])

logger = logging.getLogger(__name__)


def _get_verifier() -> CallbackVerifier:
    return CallbackVerifier()


@router.get("")
async def verify(
    signature: str,
    timestamp: str,
    nonce: str,
    echostr: str,
    verifier: CallbackVerifier = Depends(_get_verifier),
) -> Response:
    if not verifier.verify_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        raise HTTPException(status_code=403, detail="invalid signature")
    return PlainTextResponse(content=echostr)


@router.post("")
async def receive(
    request: Request,
    signature: str,
    timestamp: str,
    nonce: str,
    msg_signature: str | None = None,
    encrypt_type: str | None = None,
    db: Session = Depends(get_db),
    verifier: CallbackVerifier = Depends(_get_verifier),
) -> Response:
    if not verifier.verify_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        logger.warning("wechat callback signature invalid", extra={
            "event": "wechat.callback.invalid_signature",
            "signature": signature,
            "timestamp": timestamp,
            "nonce": nonce,
        })
        raise HTTPException(status_code=403, detail="invalid signature")

    raw_body_bytes = await request.body()
    raw_body = raw_body_bytes.decode("utf-8")
    decrypted = verifier.decrypt_if_needed(
        encrypt_type=encrypt_type,
        body=raw_body,
        msg_signature=msg_signature,
    )
    payload = parse_xml_message(decrypted)
    event = verifier.to_event(payload=payload, raw_message=raw_body)

    message = None
    if event.vendor_msg_id:
        message = repo.get_message_by_vendor_msg_id(db, vendor_msg_id=event.vendor_msg_id)
    error_code = _to_int(payload.get("ErrorCode"))
    status_text = payload.get("Status") or payload.get("status")
    error_message = payload.get("ErrorMsg") or payload.get("errmsg")
    status_text_normalized = (status_text or "").lower() if status_text else ""
    status_label = "success"
    if error_code is not None or status_text_normalized not in {"", "success", "ok"}:
        status_label = "failure"
    repo.create_event(
        db,
        wechat_message_bid=message.wechat_message_bid if message else None,
        vendor_msg_id=event.vendor_msg_id,
        event_type=event.event_type,
        status_text=status_text,
        error_code=error_code,
        error_message=error_message,
        occurred_at=event.occurred_at,
        payload=payload,
        raw_message=raw_body,
    )
    db.commit()
    record_wechat_callback(event.event_type, status_label)
    logger.info(
        "wechat callback received",
        extra={
            "event": "wechat.callback.received",
            "event_type": event.event_type,
            "vendor_msg_id": event.vendor_msg_id,
            "message_bid": message.wechat_message_bid if message else None,
            "status": status_label,
            "error_code": error_code,
        },
    )
    return PlainTextResponse(content="success")


def _to_int(value: Any) -> int | None:
    if value in (None, "", []) or isinstance(value, (list, dict)):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
