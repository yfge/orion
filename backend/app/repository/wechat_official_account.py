from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..db import models


def get_token_by_app_id(db: Session, *, app_id: str) -> models.WechatOfficialAccountToken | None:
    return (
        db.query(models.WechatOfficialAccountToken)
        .filter(
            models.WechatOfficialAccountToken.app_id == app_id,
            models.WechatOfficialAccountToken.is_deleted.is_(False),
        )
        .order_by(models.WechatOfficialAccountToken.id.desc())
        .first()
    )


def upsert_token(
    db: Session,
    *,
    app_id: str,
    access_token: str,
    expires_at: datetime,
    environment: str | None,
    trace_id: str | None,
) -> models.WechatOfficialAccountToken:
    record = get_token_by_app_id(db, app_id=app_id)
    now = datetime.now(timezone.utc)
    if record:
        record.access_token = access_token
        record.expires_at = expires_at
        record.fetched_at = now
        record.environment = environment
        record.trace_id = trace_id
    else:
        record = models.WechatOfficialAccountToken(
            app_id=app_id,
            access_token=access_token,
            expires_at=expires_at,
            fetched_at=now,
            environment=environment,
            trace_id=trace_id,
        )
        db.add(record)
    db.flush()
    return record


def mark_token_deleted(db: Session, *, app_id: str) -> None:
    record = get_token_by_app_id(db, app_id=app_id)
    if not record:
        return
    record.is_deleted = True
    record.updated_at = datetime.now(timezone.utc)
    db.flush()


def get_message_by_vendor_msg_id(
    db: Session,
    *,
    vendor_msg_id: str,
) -> models.WechatOfficialAccountMessage | None:
    return (
        db.query(models.WechatOfficialAccountMessage)
        .filter(
            models.WechatOfficialAccountMessage.vendor_msg_id == vendor_msg_id,
            models.WechatOfficialAccountMessage.is_deleted.is_(False),
        )
        .order_by(models.WechatOfficialAccountMessage.id.desc())
        .first()
    )


def create_event(
    db: Session,
    *,
    wechat_message_bid: str | None,
    vendor_msg_id: str | None,
    event_type: str,
    status_text: str | None,
    error_code: int | None,
    error_message: str | None,
    occurred_at: datetime,
    payload: dict | None,
    raw_message: str | None,
) -> models.WechatOfficialAccountEvent:
    record = models.WechatOfficialAccountEvent(
        wechat_message_bid=wechat_message_bid,
        vendor_msg_id=vendor_msg_id,
        event_type=event_type,
        status_text=status_text,
        error_code=error_code,
        error_message=error_message,
        occurred_at=occurred_at,
        payload=payload,
        raw_message=raw_message,
    )
    db.add(record)
    db.flush()
    return record
