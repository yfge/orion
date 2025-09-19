from typing import Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db.models import BusinessSystem, NotificationAPI, AuthProfile


def _get_system_id_by_bid(db: Session, bid: str) -> int | None:
    stmt = select(BusinessSystem.id).where(
        BusinessSystem.business_system_bid == bid,
        BusinessSystem.is_deleted == False,  # noqa: E712
    )
    row = db.execute(stmt).first()
    return int(row[0]) if row else None


def _get_auth_profile_id_by_bid(db: Session, bid: str | None) -> int | None:
    if not bid:
        return None
    stmt = select(AuthProfile.id).where(
        AuthProfile.auth_profile_bid == bid,
        AuthProfile.is_deleted == False,  # noqa: E712
    )
    row = db.execute(stmt).first()
    return int(row[0]) if row else None


def create_endpoint(
    db: Session,
    *,
    system_bid: str,
    name: str,
    transport: str | None,
    adapter_key: str | None,
    endpoint_url: str | None,
    config: dict | None,
    auth_profile_bid: str | None,
    status: int | None = 0,
) -> NotificationAPI:
    obj = NotificationAPI(
        business_system_bid=system_bid,
        name=name,
        endpoint_url=endpoint_url or "",
        request_schema=None,
        response_schema=None,
        transport=transport,
        adapter_key=adapter_key,
        config=config,
        auth_profile_bid=auth_profile_bid,
        status=status or 0,
    )
    db.add(obj)
    db.flush()
    return obj


def list_endpoints(db: Session, *, system_bid: str, limit: int = 50, offset: int = 0, q: str | None = None) -> Tuple[list[NotificationAPI], int]:
    system_id = _get_system_id_by_bid(db, system_bid)
    if system_id is None:
        return [], 0
    base = select(NotificationAPI).where(NotificationAPI.business_system_bid == system_bid, NotificationAPI.is_deleted == False)  # noqa: E712
    count_q = select(func.count()).select_from(NotificationAPI).where(NotificationAPI.business_system_bid == system_bid, NotificationAPI.is_deleted == False)  # noqa: E712
    if q:
        like = f"%{q}%"
        base = base.where(NotificationAPI.name.ilike(like))
        count_q = count_q.where(NotificationAPI.name.ilike(like))
    items = list(db.execute(base.order_by(NotificationAPI.id.desc()).limit(limit).offset(offset)).scalars())
    # Attach business_system_bid and auth_profile_bid for each item (avoid extra queries via simple lookups)
    for it in items:
        # already set in row
        pass
    total = db.execute(count_q).scalar_one()
    return items, int(total)


def get_by_bid(db: Session, bid: str) -> NotificationAPI | None:
    return db.execute(select(NotificationAPI).where(NotificationAPI.notification_api_bid == bid, NotificationAPI.is_deleted == False)).scalar_one_or_none()  # noqa: E712


def list_all_endpoints(db: Session, *, limit: int = 50, offset: int = 0, q: str | None = None) -> Tuple[list[NotificationAPI], int]:
    base = select(NotificationAPI).where(NotificationAPI.is_deleted == False)  # noqa: E712
    count_q = select(func.count()).select_from(NotificationAPI).where(NotificationAPI.is_deleted == False)  # noqa: E712
    if q:
        like = f"%{q}%"
        base = base.where(NotificationAPI.name.ilike(like))
        count_q = count_q.where(NotificationAPI.name.ilike(like))
    items = list(db.execute(base.order_by(NotificationAPI.id.desc()).limit(limit).offset(offset)).scalars())
    total = db.execute(count_q).scalar_one()
    return items, int(total)


def update_by_bid(
    db: Session,
    bid: str,
    *,
    name: str | None = None,
    transport: str | None = None,
    adapter_key: str | None = None,
    endpoint_url: str | None = None,
    config: dict | None = None,
    auth_profile_bid: str | None = None,
    status: int | None = None,
) -> NotificationAPI | None:
    obj = db.execute(select(NotificationAPI).where(NotificationAPI.notification_api_bid == bid, NotificationAPI.is_deleted == False)).scalar_one_or_none()  # noqa: E712
    if not obj:
        return None
    if name is not None:
        obj.name = name
    if transport is not None:
        obj.transport = transport
    if adapter_key is not None:
        obj.adapter_key = adapter_key
    if endpoint_url is not None:
        obj.endpoint_url = endpoint_url
    if config is not None:
        obj.config = config
    if auth_profile_bid is not None:
        obj.auth_profile_id = _get_auth_profile_id_by_bid(db, auth_profile_bid)
    if status is not None:
        obj.status = status
    db.flush()
    return obj


def soft_delete_by_bid(db: Session, bid: str) -> bool:
    obj = db.execute(select(NotificationAPI).where(NotificationAPI.notification_api_bid == bid, NotificationAPI.is_deleted == False)).scalar_one_or_none()  # noqa: E712
    if not obj:
        return False
    obj.is_deleted = True
    db.flush()
    return True
