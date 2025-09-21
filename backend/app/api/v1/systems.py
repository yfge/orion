from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...deps.db import get_db
from ...repository import systems as repo
from ...schemas.systems import (
    BusinessSystemCreate,
    BusinessSystemList,
    BusinessSystemOut,
    BusinessSystemUpdate,
)

router = APIRouter(prefix="/systems", tags=["systems"])


@router.post("", response_model=BusinessSystemOut, status_code=status.HTTP_201_CREATED)
def create_system(payload: BusinessSystemCreate, db: Session = Depends(get_db)):
    obj = repo.create_system(
        db,
        name=payload.name,
        base_url=payload.base_url,
        auth_method=payload.auth_method,
        app_id=payload.app_id,
        app_secret=payload.app_secret,
        status=payload.status or 0,
    )
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=BusinessSystemList)
def list_systems(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    q: str | None = Query(default=None, description="Search by name"),
):
    items, total = repo.list_systems(db, limit=limit, offset=offset, q=q)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{bid}", response_model=BusinessSystemOut)
def get_system(bid: str, db: Session = Depends(get_db)):
    obj = repo.get_by_bid(db, bid)
    if not obj:
        raise HTTPException(status_code=404, detail="Business system not found")
    return obj


@router.patch("/{bid}", response_model=BusinessSystemOut)
def update_system(bid: str, payload: BusinessSystemUpdate, db: Session = Depends(get_db)):
    obj = repo.update_by_bid(
        db,
        bid,
        name=payload.name,
        base_url=payload.base_url,
        auth_method=payload.auth_method,
        app_id=payload.app_id,
        app_secret=payload.app_secret,
        status=payload.status,
    )
    if not obj:
        raise HTTPException(status_code=404, detail="Business system not found")
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{bid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_system(bid: str, db: Session = Depends(get_db)):
    ok = repo.soft_delete_by_bid(db, bid)
    if not ok:
        raise HTTPException(status_code=404, detail="Business system not found")
    db.commit()
    return None
