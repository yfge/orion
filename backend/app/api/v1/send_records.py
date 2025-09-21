from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...deps.db import get_db
from ...repository import send_records as repo
from ...schemas.send_records import SendDetailList, SendRecordList, SendRecordOut

router = APIRouter(prefix="/send-records", tags=["send_records"])


@router.get("", response_model=SendRecordList)
def list_send_records(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    message_definition_bid: str | None = Query(default=None),
    notification_api_bid: str | None = Query(default=None),
    status: int | None = Query(default=None),
    start_time: datetime | None = Query(
        default=None, description="Filter by send_time >= start_time (ISO8601)"
    ),
    end_time: datetime | None = Query(
        default=None, description="Filter by send_time < end_time (ISO8601)"
    ),
):
    items, total = repo.list_send_records(
        db,
        limit=limit,
        offset=offset,
        message_definition_bid=message_definition_bid,
        notification_api_bid=notification_api_bid,
        status=status,
        start_time=start_time,
        end_time=end_time,
    )
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{bid}", response_model=SendRecordOut)
def get_send_record(bid: str, db: Session = Depends(get_db)):
    rec = repo.get_record_by_bid(db, bid=bid)
    if not rec:
        raise HTTPException(status_code=404, detail="Send record not found")
    return rec


@router.get("/{bid}/details", response_model=SendDetailList)
def list_send_details(
    bid: str,
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    items, total = repo.list_details_by_record(db, send_record_bid=bid, limit=limit, offset=offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}
