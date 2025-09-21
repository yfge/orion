from __future__ import annotations

import hashlib
import secrets

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..db.models import ApiKey


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def create_api_key(db: Session, *, name: str, description: str | None = None) -> tuple[ApiKey, str]:
    token = secrets.token_urlsafe(32)
    token_hash = _sha256_hex(token)
    prefix = token[:8]
    suffix = token[-6:]
    obj = ApiKey(
        name=name,
        token_hash=token_hash,
        prefix=prefix,
        suffix=suffix,
        description=description,
        status=1,
    )
    db.add(obj)
    db.flush()
    return obj, token


def list_api_keys(
    db: Session, *, limit: int = 50, offset: int = 0, q: str | None = None
) -> tuple[list[ApiKey], int]:
    query = db.query(ApiKey).filter(~ApiKey.is_deleted)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(ApiKey.name.ilike(like)))
    total = query.count()
    items = query.order_by(ApiKey.id.desc()).limit(limit).offset(offset).all()
    return items, total


def soft_delete_by_bid(db: Session, api_key_bid: str) -> bool:
    obj = db.query(ApiKey).filter(ApiKey.api_key_bid == api_key_bid, ~ApiKey.is_deleted).first()
    if not obj:
        return False
    obj.is_deleted = True
    obj.status = -1
    db.add(obj)
    db.flush()
    return True


def exists_by_token(db: Session, *, token: str) -> bool:
    token_hash = _sha256_hex(token)
    obj = (
        db.query(ApiKey)
        .filter(ApiKey.token_hash == token_hash, ~ApiKey.is_deleted, ApiKey.status == 1)
        .first()
    )
    return obj is not None


def update_by_bid(
    db: Session,
    api_key_bid: str,
    *,
    name: str | None = None,
    description: str | None = None,
    status: int | None = None,
) -> ApiKey | None:
    obj = db.query(ApiKey).filter(ApiKey.api_key_bid == api_key_bid, ~ApiKey.is_deleted).first()
    if not obj:
        return None
    if name is not None:
        obj.name = name
    if description is not None:
        obj.description = description
    if status is not None:
        obj.status = int(status)
    db.add(obj)
    db.flush()
    return obj
