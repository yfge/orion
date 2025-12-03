from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


class WechatTemplateFieldInput(BaseModel):
    value: str
    color: str | None = Field(default=None, description="Hex color like #173177")


class WechatLinkInput(BaseModel):
    type: Literal["url", "mini_program"] = Field(default="url")
    url: HttpUrl | None = Field(default=None, description="External link for H5 跳转")
    app_id: str | None = Field(default=None, alias="appid", description="Mini program appid when type=mini_program")
    path: str | None = Field(default=None, alias="pagepath", description="Mini program page path when type=mini_program")

    model_config = {"populate_by_name": True}


class WechatTemplateMessageRequest(BaseModel):
    to_user: str = Field(..., alias="touser", min_length=1, description="Target user OpenID")
    template_id: str = Field(..., min_length=1)
    data: dict[str, WechatTemplateFieldInput]
    context: dict[str, Any] = Field(default_factory=dict, description="Template render context")
    link: WechatLinkInput | None = None
    language: str | None = Field(default=None, max_length=10)
    idempotency_key: str | None = Field(default=None, alias="client_msg_id")
    app_id: str | None = Field(default=None, alias="appid", description="Override AppID when多账号场景")
    app_secret: str | None = Field(default=None, alias="appsecret", description="AppSecret override when multi-account")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "touser": "openid-123",
                "template_id": "TM12345",
                "data": {
                    "first": {"value": "Hello"},
                    "remark": {"value": "Thanks", "color": "#173177"},
                },
                "context": {"name": "Alice"},
                "link": {"type": "url", "url": "https://example.com"},
                "client_msg_id": "req-123",
            }
        },
    }


class WechatCustomMessageRequest(BaseModel):
    to_user: str = Field(..., alias="touser", min_length=1)
    msg_type: str = Field(..., alias="msgtype")
    payload: dict[str, Any] = Field(..., description="Raw客服消息体")
    app_id: str | None = Field(default=None, alias="appid")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "touser": "openid-123",
                "msgtype": "text",
                "payload": {"text": {"content": "Hi there"}},
            }
        },
    }


class WechatNotificationOut(BaseModel):
    message_bid: str = Field(..., description="Internal message identifier")
    state: str
    vendor_msg_id: str | None = None
    error: str | None = None
    retry_scheduled: bool = False


class WechatNotificationDetail(BaseModel):
    message_bid: str
    app_id: str
    to_user: str
    template_id: str
    language: str | None = None
    link: WechatLinkInput | None = None
    data: dict[str, Any] | None = None
    context: dict[str, Any] | None = None
    state: str
    vendor_msg_id: str | None = None
    last_error_code: int | None = None
    last_error_message: str | None = None
    retry_count: int
    queued_at: datetime
    last_attempt_at: datetime | None = None
    updated_at: datetime


class WechatNotificationList(BaseModel):
    items: list[WechatNotificationDetail]
    total: int
    limit: int
    offset: int
