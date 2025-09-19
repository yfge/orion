from typing import Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db.models import AuthProfile


def create_profile(db: Session, *, name: str, type: str, config: dict | None, status: int | None = 0) -> AuthProfile:
    obj = AuthProfile(name=name, type=type, config=config, status=status or 0)
    db.add(obj)
    db.flush()
    return obj


def list_profiles(db: Session, *, limit: int = 50, offset: int = 0, q: str | None = None) -> Tuple[list[AuthProfile], int]:
    base = select(AuthProfile).where(AuthProfile.is_deleted == False)  # noqa: E712
    count_q = select(func.count()).select_from(AuthProfile).where(AuthProfile.is_deleted == False)  # noqa: E712
    if q:
        like = f"%{q}%"
        base = base.where(AuthProfile.name.ilike(like))
        count_q = count_q.where(AuthProfile.name.ilike(like))
    items = list(db.execute(base.order_by(AuthProfile.id.desc()).limit(limit).offset(offset)).scalars())
    total = db.execute(count_q).scalar_one()
    return items, int(total)


def get_by_bid(db: Session, bid: str) -> AuthProfile | None:
    return db.execute(select(AuthProfile).where(AuthProfile.auth_profile_bid == bid, AuthProfile.is_deleted == False)).scalar_one_or_none()  # noqa: E712


def update_by_bid(db: Session, bid: str, *, name: str | None = None, type: str | None = None, config: dict | None = None, status: int | None = None) -> AuthProfile | None:
    obj = get_by_bid(db, bid)
    if not obj:
        return None
    if name is not None:
        obj.name = name
    if type is not None:
        obj.type = type
    if config is not None:
        obj.config = config
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

