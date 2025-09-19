from __future__ import annotations

from datetime import datetime
from typing import Any, List

from pydantic import BaseModel, Field


class SendRecordOut(BaseModel):
    send_record_bid: str = Field(..., description="BID of the send record")
    message_definition_bid: str
    notification_api_bid: str
    message_name: str | None = None
    endpoint_name: str | None = None
    business_system_name: str | None = None
    send_time: datetime | None = None
    result: Any | None = None
    remark: str | None = None
    status: int
    created_at: datetime

    class Config:
        from_attributes = True


class SendRecordList(BaseModel):
    items: List[SendRecordOut]
    total: int
    limit: int
    offset: int


class SendDetailOut(BaseModel):
    send_detail_bid: str
    send_record_bid: str
    notification_api_bid: str
    endpoint_name: str | None = None
    attempt_no: int
    request_payload: Any | None = None
    response_payload: Any | None = None
    sent_at: datetime | None = None
    error: str | None = None
    status: int
    created_at: datetime

    class Config:
        from_attributes = True


class SendDetailList(BaseModel):
    items: List[SendDetailOut]
    total: int
    limit: int
    offset: int

