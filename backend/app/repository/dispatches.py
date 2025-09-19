from typing import Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db.models import MessageDefinition, NotificationAPI, MessageDispatch, BusinessSystem


def _get_message_id_by_bid(db: Session, bid: str) -> int | None:
    row = db.execute(select(MessageDefinition.id).where(MessageDefinition.message_definition_bid == bid, MessageDefinition.is_deleted == False)).first()  # noqa: E712
    return int(row[0]) if row else None


def _get_endpoint_id_by_bid(db: Session, bid: str) -> int | None:
    row = db.execute(select(NotificationAPI.id).where(NotificationAPI.notification_api_bid == bid, NotificationAPI.is_deleted == False)).first()  # noqa: E712
    return int(row[0]) if row else None


def create_dispatch(db: Session, *, message_bid: str, endpoint_bid: str, mapping: dict | None, enabled: bool = True) -> MessageDispatch:
    mid = _get_message_id_by_bid(db, message_bid)
    if mid is None:
        raise ValueError("message definition not found")
    eid = _get_endpoint_id_by_bid(db, endpoint_bid)
    if eid is None:
        raise ValueError("endpoint not found")
    obj = MessageDispatch(message_definition_id=mid, notification_api_id=eid, mapping=mapping, enabled=enabled)
    db.add(obj)
    db.flush()
    return obj


def list_by_message(db: Session, *, message_bid: str, limit: int = 50, offset: int = 0) -> Tuple[list[MessageDispatch], int]:
    mid = _get_message_id_by_bid(db, message_bid)
    if mid is None:
        return [], 0
    base = (
        select(MessageDispatch, NotificationAPI.name, NotificationAPI.notification_api_bid, BusinessSystem.business_system_bid)
        .join(NotificationAPI, MessageDispatch.notification_api_id == NotificationAPI.id)
        .join(BusinessSystem, NotificationAPI.business_system_id == BusinessSystem.id)
        .where(MessageDispatch.message_definition_id == mid, MessageDispatch.is_deleted == False)
    )
    items_rows = db.execute(base.order_by(MessageDispatch.id.desc()).limit(limit).offset(offset)).all()
    items = []
    for md, ep_name, ep_bid, bs_bid in items_rows:
        md.endpoint_name = ep_name  # type: ignore[attr-defined]
        md.endpoint_bid = ep_bid  # type: ignore[attr-defined]
        md.business_system_bid = bs_bid  # type: ignore[attr-defined]
        md.message_definition_bid = message_bid  # type: ignore[attr-defined]
        items.append(md)
    total = db.execute(select(func.count()).select_from(MessageDispatch).where(MessageDispatch.message_definition_id == mid, MessageDispatch.is_deleted == False)).scalar_one()  # noqa: E712
    return items, int(total)


def get_by_bid(db: Session, bid: str) -> MessageDispatch | None:
    row = db.execute(
        select(MessageDispatch, NotificationAPI.notification_api_bid, NotificationAPI.name, BusinessSystem.business_system_bid, MessageDefinition.message_definition_bid)
        .join(NotificationAPI, MessageDispatch.notification_api_id == NotificationAPI.id)
        .join(BusinessSystem, NotificationAPI.business_system_id == BusinessSystem.id)
        .join(MessageDefinition, MessageDispatch.message_definition_id == MessageDefinition.id)
        .where(MessageDispatch.message_dispatch_bid == bid, MessageDispatch.is_deleted == False)
    ).first()
    if not row:
        return None
    md, ep_bid, ep_name, bs_bid, msg_bid = row
    md.endpoint_bid = ep_bid  # type: ignore[attr-defined]
    md.endpoint_name = ep_name  # type: ignore[attr-defined]
    md.business_system_bid = bs_bid  # type: ignore[attr-defined]
    md.message_definition_bid = msg_bid  # type: ignore[attr-defined]
    return md


def update_by_bid(db: Session, bid: str, *, endpoint_bid: str | None = None, mapping: dict | None = None, enabled: bool | None = None) -> MessageDispatch | None:
    obj = db.execute(select(MessageDispatch).where(MessageDispatch.message_dispatch_bid == bid, MessageDispatch.is_deleted == False)).scalar_one_or_none()  # noqa: E712
    if not obj:
        return None
    if endpoint_bid is not None:
        eid = _get_endpoint_id_by_bid(db, endpoint_bid)
        if eid is None:
            raise ValueError("endpoint not found")
        obj.notification_api_id = eid
    if mapping is not None:
        obj.mapping = mapping
    if enabled is not None:
        obj.enabled = enabled
    db.flush()
    return obj


def soft_delete_by_bid(db: Session, bid: str) -> bool:
    obj = db.execute(select(MessageDispatch).where(MessageDispatch.message_dispatch_bid == bid, MessageDispatch.is_deleted == False)).scalar_one_or_none()  # noqa: E712
    if not obj:
        return False
    obj.is_deleted = True
    db.flush()
    return True

