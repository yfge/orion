from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...deps.db import get_db
from ...repository import auth_profiles as repo
from ...schemas.auth_profiles import AuthProfileCreate, AuthProfileList, AuthProfileOut, AuthProfileUpdate


router = APIRouter(prefix="/auth-profiles", tags=["auth_profiles"])


@router.post("/", response_model=AuthProfileOut, status_code=status.HTTP_201_CREATED)
def create_profile(payload: AuthProfileCreate, db: Session = Depends(get_db)):
    obj = repo.create_profile(db, name=payload.name, type=payload.type, config=payload.config, status=payload.status or 0)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=AuthProfileList)
def list_profiles(db: Session = Depends(get_db), limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0), q: str | None = Query(default=None)):
    items, total = repo.list_profiles(db, limit=limit, offset=offset, q=q)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{bid}", response_model=AuthProfileOut)
def get_profile(bid: str, db: Session = Depends(get_db)):
    obj = repo.get_by_bid(db, bid)
    if not obj:
        raise HTTPException(status_code=404, detail="Auth profile not found")
    return obj


@router.patch("/{bid}", response_model=AuthProfileOut)
def update_profile(bid: str, payload: AuthProfileUpdate, db: Session = Depends(get_db)):
    obj = repo.update_by_bid(db, bid, name=payload.name, type=payload.type, config=payload.config, status=payload.status)
    if not obj:
        raise HTTPException(status_code=404, detail="Auth profile not found")
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{bid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(bid: str, db: Session = Depends(get_db)):
    ok = repo.soft_delete_by_bid(db, bid)
    if not ok:
        raise HTTPException(status_code=404, detail="Auth profile not found")
    db.commit()
    return None

