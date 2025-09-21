import secrets
import uuid
from datetime import datetime
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ...db.session import session_scope
from ...deps.api_key import require_api_key
from ...deps.db import get_db
from ...repository import dispatches as disp_repo
from ...repository import send_records as rec_repo
from ...schemas.send_records import SendDetailList, SendRecordList, SendRecordOut
from ...services.notify import notify_by_bid, notify_by_name


class NotifyRequest(BaseModel):
    message_name: str | None = Field(default=None)
    message_definition_bid: str | None = Field(default=None)
    data: dict[str, Any]


class NotifyResponse(BaseModel):
    results: list[dict[str, Any]]


router = APIRouter(prefix="/notify", tags=["notify"])


@router.post("/", response_model=NotifyResponse, dependencies=[Depends(require_api_key)])
def notify(payload: NotifyRequest, db: Session = Depends(get_db)):
    try:
        if payload.message_definition_bid:
            results = notify_by_bid(
                db, message_bid=payload.message_definition_bid, data=payload.data
            )
        elif payload.message_name:
            results = notify_by_name(db, message_name=payload.message_name, data=payload.data)
        else:
            raise HTTPException(
                status_code=400, detail="message_name or message_definition_bid is required"
            )
        db.commit()
        return {"results": results}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None


class KeyPreviewResponse(BaseModel):
    key: str


@router.post("/keys/preview", response_model=KeyPreviewResponse)
def preview_key() -> KeyPreviewResponse:
    # Return a random URL-safe token for admins to configure as ORION_PUBLIC_API_KEY
    return KeyPreviewResponse(key=secrets.token_urlsafe(32))


class AsyncNotifyRequest(NotifyRequest):
    request_id: str | None = Field(
        default=None,
        description="Optional client-generated request id, echoed in send record remark",
    )


class AsyncNotifyAccepted(BaseModel):
    accepted: bool = True
    request_id: str | None = None
    estimated_dispatches: int | None = None


def _do_notify_background(
    message_name: str | None, message_bid: str | None, data: dict[str, Any], remark: str | None
) -> None:
    with session_scope() as db:
        if message_bid:
            notify_by_bid(db, message_bid=message_bid, data=data, remark=remark)
        elif message_name:
            notify_by_name(db, message_name=message_name, data=data, remark=remark)
        else:
            raise ValueError("message_name or message_definition_bid required")


@router.post(
    "/async",
    response_model=AsyncNotifyAccepted,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(require_api_key)],
)
def notify_async(payload: AsyncNotifyRequest, bg: BackgroundTasks, db: Session = Depends(get_db)):
    est = None
    try:
        msg_bid = payload.message_definition_bid
        if not msg_bid and payload.message_name:
            from ...repository import message_definitions as msg_repo

            m = msg_repo.get_by_name(db, payload.message_name)
            if m:
                msg_bid = m.message_definition_bid
        if msg_bid:
            items, _ = disp_repo.list_by_message(db, message_bid=msg_bid, limit=1000, offset=0)
            est = sum(1 for it in items if getattr(it, "enabled", True))
    except Exception:
        est = None
    req_id = payload.request_id or uuid.uuid4().hex
    bg.add_task(
        _do_notify_background,
        payload.message_name,
        payload.message_definition_bid,
        payload.data,
        req_id,
    )
    return AsyncNotifyAccepted(accepted=True, request_id=req_id, estimated_dispatches=est)


@router.get("/send-records", response_model=SendRecordList, dependencies=[Depends(require_api_key)])
def list_send_records_public(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    message_definition_bid: str | None = Query(default=None),
    notification_api_bid: str | None = Query(default=None),
    status: int | None = Query(default=None),
    start_time: datetime | None = Query(default=None),
    end_time: datetime | None = Query(default=None),
    request_id: str | None = Query(default=None),
):
    items, total = rec_repo.list_send_records(
        db,
        limit=limit,
        offset=offset,
        message_definition_bid=message_definition_bid,
        notification_api_bid=notification_api_bid,
        status=status,
        start_time=start_time,
        end_time=end_time,
        remark=request_id,
    )
    shaped = [
        SendRecordOut.model_validate(
            {
                "send_record_bid": it.send_record_bid,
                "message_definition_bid": it.message_definition_bid,
                "notification_api_bid": it.notification_api_bid,
                "message_name": getattr(it, "message_name", None),
                "endpoint_name": getattr(it, "endpoint_name", None),
                "business_system_name": getattr(it, "business_system_name", None),
                "send_time": it.send_time,
                "result": it.result,
                "remark": it.remark,
                "status": it.status,
                "created_at": it.created_at,
            }
        )
        for it in items
    ]
    return {"items": shaped, "total": total, "limit": limit, "offset": offset}


@router.get(
    "/send-records/{bid}", response_model=SendRecordOut, dependencies=[Depends(require_api_key)]
)
def get_send_record_public(bid: str, db: Session = Depends(get_db)):
    rec = rec_repo.get_record_by_bid(db, bid=bid)
    if not rec:
        raise HTTPException(status_code=404, detail="Send record not found")
    return SendRecordOut.model_validate(
        {
            "send_record_bid": rec.send_record_bid,
            "message_definition_bid": rec.message_definition_bid,
            "notification_api_bid": rec.notification_api_bid,
            "message_name": getattr(rec, "message_name", None),
            "endpoint_name": getattr(rec, "endpoint_name", None),
            "business_system_name": getattr(rec, "business_system_name", None),
            "send_time": rec.send_time,
            "result": rec.result,
            "remark": rec.remark,
            "status": rec.status,
            "created_at": rec.created_at,
        }
    )


@router.get(
    "/send-records/{bid}/details",
    response_model=SendDetailList,
    dependencies=[Depends(require_api_key)],
)
def list_send_details_public(
    bid: str,
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    items, total = rec_repo.list_details_by_record(
        db, send_record_bid=bid, limit=limit, offset=offset
    )
    shaped = [
        {
            "send_detail_bid": it.send_detail_bid,
            "send_record_bid": it.send_record_bid,
            "notification_api_bid": it.notification_api_bid,
            "endpoint_name": getattr(it, "endpoint_name", None),
            "attempt_no": it.attempt_no,
            "request_payload": it.request_payload,
            "response_payload": it.response_payload,
            "sent_at": it.sent_at,
            "error": it.error,
            "status": it.status,
            "created_at": it.created_at,
        }
        for it in items
    ]
    return {"items": shaped, "total": total, "limit": limit, "offset": offset}
