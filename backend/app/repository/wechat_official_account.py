from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

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


def create_message_record(
    db: Session,
    *,
    message_bid: str,
    send_record_bid: str | None,
    app_id: str,
    to_user: str,
    template_id: str,
    language: str | None,
    link_type: str | None,
    link_url: str | None,
    mini_program_app_id: str | None,
    mini_program_path: str | None,
    data_payload: dict[str, Any] | None,
    raw_request: dict[str, Any] | None,
    idempotency_key: str | None,
    state: str,
) -> models.WechatOfficialAccountMessage:
    record = models.WechatOfficialAccountMessage(
        wechat_message_bid=message_bid,
        send_record_bid=send_record_bid,
        app_id=app_id,
        to_user=to_user,
        template_id=template_id,
        language=language,
        link_type=link_type,
        link_url=link_url,
        mini_program_app_id=mini_program_app_id,
        mini_program_path=mini_program_path,
        data_payload=data_payload,
        raw_request=raw_request,
        state=state,
        idempotency_key=idempotency_key,
    )
    db.add(record)
    db.flush()
    return record


def update_message_state(
    db: Session,
    record: models.WechatOfficialAccountMessage,
    *,
    state: str,
) -> None:
    record.state = state
    record.updated_at = datetime.now(timezone.utc)
    db.flush()


def mark_message_success(
    db: Session,
    record: models.WechatOfficialAccountMessage,
    *,
    vendor_msg_id: str,
    occurred_at: datetime | None = None,
) -> None:
    record.vendor_msg_id = vendor_msg_id
    record.state = "success"
    record.last_error_code = None
    record.last_error_message = None
    record.last_attempt_at = occurred_at or datetime.now(timezone.utc)
    record.updated_at = datetime.now(timezone.utc)
    db.flush()


def mark_message_failure(
    db: Session,
    record: models.WechatOfficialAccountMessage,
    *,
    error_code: int | None,
    error_message: str | None,
    retrying: bool,
    occurred_at: datetime | None = None,
) -> None:
    record.last_error_code = error_code
    record.last_error_message = error_message
    record.retry_count = (record.retry_count or 0) + 1
    record.state = "retrying" if retrying else "failed"
    record.last_attempt_at = occurred_at or datetime.now(timezone.utc)
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


def get_message_by_bid(
    db: Session,
    *,
    message_bid: str,
) -> models.WechatOfficialAccountMessage | None:
    return (
        db.query(models.WechatOfficialAccountMessage)
        .filter(
            models.WechatOfficialAccountMessage.wechat_message_bid == message_bid,
            models.WechatOfficialAccountMessage.is_deleted.is_(False),
        )
        .order_by(models.WechatOfficialAccountMessage.id.desc())
        .first()
    )
