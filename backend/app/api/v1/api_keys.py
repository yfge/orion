from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...deps.db import get_db
from ...repository import api_keys as repo
from ...schemas.api_keys import (
    ApiKeyCreate,
    ApiKeyCreateResponse,
    ApiKeyList,
    ApiKeyOut,
    ApiKeyUpdate,
)
from .users import get_current_user_bid

router = APIRouter(prefix="/api-keys", tags=["api-keys"])


@router.post("", response_model=ApiKeyCreateResponse, status_code=status.HTTP_201_CREATED)
def create_api_key(
    payload: ApiKeyCreate,
    db: Session = Depends(get_db),
    user_bid: str = Depends(get_current_user_bid),
):
    obj, token = repo.create_api_key(
        db, owner_user_bid=user_bid, name=payload.name, description=payload.description
    )
    db.commit()
    return {
        "api_key_bid": obj.api_key_bid,
        "name": obj.name,
        "token": token,
        "prefix": obj.prefix,
        "suffix": obj.suffix,
    }


@router.get("", response_model=ApiKeyList)
def list_api_keys(
    db: Session = Depends(get_db),
    user_bid: str = Depends(get_current_user_bid),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    q: str | None = Query(default=None),
):
    items, total = repo.list_api_keys(db, owner_user_bid=user_bid, limit=limit, offset=offset, q=q)
    shaped = [
        {
            "api_key_bid": it.api_key_bid,
            "name": it.name,
            "prefix": it.prefix,
            "suffix": it.suffix,
            "status": it.status,
            "created_at": it.created_at,
        }
        for it in items
    ]
    return {"items": shaped, "total": total, "limit": limit, "offset": offset}


@router.delete("/{api_key_bid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_api_key(
    api_key_bid: str, db: Session = Depends(get_db), user_bid: str = Depends(get_current_user_bid)
):
    ok = repo.soft_delete_by_bid(db, owner_user_bid=user_bid, api_key_bid=api_key_bid)
    if not ok:
        raise HTTPException(status_code=404, detail="API key not found")
    db.commit()
    return None


@router.patch("/{api_key_bid}", response_model=ApiKeyOut)
def update_api_key(
    api_key_bid: str,
    payload: ApiKeyUpdate,
    db: Session = Depends(get_db),
    user_bid: str = Depends(get_current_user_bid),
):
    obj = repo.update_by_bid(
        db,
        api_key_bid,
        owner_user_bid=user_bid,
        name=payload.name,
        description=payload.description,
        status=payload.status,
    )
    if not obj:
        raise HTTPException(status_code=404, detail="API key not found")
    db.commit()
    db.refresh(obj)
    return {
        "api_key_bid": obj.api_key_bid,
        "name": obj.name,
        "prefix": obj.prefix,
        "suffix": obj.suffix,
        "status": obj.status,
        "created_at": obj.created_at,
    }
