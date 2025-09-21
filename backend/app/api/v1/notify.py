import secrets
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ...deps.api_key import require_api_key
from ...deps.db import get_db
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
