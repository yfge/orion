from typing import Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db.models import MessageDefinition


def create_message_def(db: Session, *, name: str, type: str | None, schema: dict | None, status: int | None = 0) -> MessageDefinition:
    obj = MessageDefinition(name=name, type=type, schema=schema, status=status or 0)
    db.add(obj)
    db.flush()
    return obj


def list_message_defs(db: Session, *, limit: int = 50, offset: int = 0, q: str | None = None) -> Tuple[list[MessageDefinition], int]:
    base = select(MessageDefinition).where(MessageDefinition.is_deleted == False)  # noqa: E712
    count_q = select(func.count()).select_from(MessageDefinition).where(MessageDefinition.is_deleted == False)  # noqa: E712
    if q:
        like = f"%{q}%"
        base = base.where(MessageDefinition.name.ilike(like))
        count_q = count_q.where(MessageDefinition.name.ilike(like))
    items = list(db.execute(base.order_by(MessageDefinition.id.desc()).limit(limit).offset(offset)).scalars())
    total = db.execute(count_q).scalar_one()
    return items, int(total)


def get_by_bid(db: Session, bid: str) -> MessageDefinition | None:
    return db.execute(select(MessageDefinition).where(MessageDefinition.message_definition_bid == bid, MessageDefinition.is_deleted == False)).scalar_one_or_none()  # noqa: E712


def get_by_name(db: Session, name: str) -> MessageDefinition | None:
    return db.execute(select(MessageDefinition).where(MessageDefinition.name == name, MessageDefinition.is_deleted == False)).scalar_one_or_none()  # noqa: E712


def update_by_bid(db: Session, bid: str, *, name: str | None = None, type: str | None = None, schema: dict | None = None, status: int | None = None) -> MessageDefinition | None:
    obj = get_by_bid(db, bid)
    if not obj:
        return None
    if name is not None:
        obj.name = name
    if type is not None:
        obj.type = type
    if schema is not None:
        obj.schema = schema
    if status is not None:
        obj.status = status
    db.flush()
    return obj


def soft_delete_by_bid(db: Session, bid: str) -> bool:
    obj = get_by_bid(db, bid)
    if not obj:
        return False
    obj.is_deleted = True
    db.flush()
    return True
