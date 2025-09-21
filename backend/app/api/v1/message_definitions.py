from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...deps.db import get_db
from ...repository import message_definitions as repo
from ...schemas.message_definitions import (
    MessageDefCreate,
    MessageDefList,
    MessageDefOut,
    MessageDefUpdate,
)

router = APIRouter(prefix="/message-definitions", tags=["message_definitions"])


@router.post("", response_model=MessageDefOut, status_code=status.HTTP_201_CREATED)
def create_message_def(payload: MessageDefCreate, db: Session = Depends(get_db)):
    obj = repo.create_message_def(
        db, name=payload.name, type=payload.type, schema=payload.schema, status=payload.status or 0
    )
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=MessageDefList)
def list_message_defs(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    q: str | None = Query(default=None),
):
    items, total = repo.list_message_defs(db, limit=limit, offset=offset, q=q)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{bid}", response_model=MessageDefOut)
def get_message_def(bid: str, db: Session = Depends(get_db)):
    obj = repo.get_by_bid(db, bid)
    if not obj:
        raise HTTPException(status_code=404, detail="Message definition not found")
    return obj


@router.patch("/{bid}", response_model=MessageDefOut)
def update_message_def(bid: str, payload: MessageDefUpdate, db: Session = Depends(get_db)):
    obj = repo.update_by_bid(
        db, bid, name=payload.name, type=payload.type, schema=payload.schema, status=payload.status
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Message definition not found")
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{bid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message_def(bid: str, db: Session = Depends(get_db)):
    ok = repo.soft_delete_by_bid(db, bid)
    if not ok:
        raise HTTPException(status_code=404, detail="Message definition not found")
    db.commit()
    return None
