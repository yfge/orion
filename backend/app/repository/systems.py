from typing import Tuple

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from ..db.models import BusinessSystem


def create_system(
    db: Session,
    *,
    name: str,
    base_url: str | None,
    auth_method: str | None,
    app_id: str | None,
    app_secret: str | None,
    status: int | None = 0,
) -> BusinessSystem:
    obj = BusinessSystem(
        name=name,
        base_url=base_url,
        auth_method=auth_method,
        app_id=app_id,
        app_secret=app_secret,
        status=status or 0,
    )
    db.add(obj)
    db.flush()
    return obj


def get_by_bid(db: Session, bid: str) -> BusinessSystem | None:
    stmt = select(BusinessSystem).where(
        BusinessSystem.business_system_bid == bid, BusinessSystem.is_deleted == False  # noqa: E712
    )
    return db.execute(stmt).scalar_one_or_none()


def list_systems(db: Session, *, limit: int = 50, offset: int = 0, q: str | None = None) -> Tuple[list[BusinessSystem], int]:
    base = select(BusinessSystem).where(BusinessSystem.is_deleted == False)  # noqa: E712
    count_q = select(func.count()).select_from(BusinessSystem).where(BusinessSystem.is_deleted == False)  # noqa: E712
    if q:
        like = f"%{q}%"
        base = base.where(BusinessSystem.name.ilike(like))
        count_q = count_q.where(BusinessSystem.name.ilike(like))
    items = list(db.execute(base.order_by(BusinessSystem.id.desc()).limit(limit).offset(offset)).scalars())
    total = db.execute(count_q).scalar_one()
    return items, int(total)


def update_by_bid(
    db: Session,
    bid: str,
    *,
    name: str | None = None,
    base_url: str | None = None,
    auth_method: str | None = None,
    app_id: str | None = None,
    app_secret: str | None = None,
    status: int | None = None,
) -> BusinessSystem | None:
    obj = get_by_bid(db, bid)
    if not obj:
        return None
    if name is not None:
        obj.name = name
    if base_url is not None:
        obj.base_url = base_url
    if auth_method is not None:
        obj.auth_method = auth_method
    if app_id is not None:
        obj.app_id = app_id
    if app_secret is not None:
        obj.app_secret = app_secret
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

