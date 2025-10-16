from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal


class WechatNotificationState(str, Enum):
    PENDING = "pending"
    SENDING = "sending"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    ABANDONED = "abandoned"


@dataclass(slots=True)
class WechatTemplateField:
    value: str
    color: str | None = None


@dataclass(slots=True)
class WechatLink:
    link_type: Literal["url", "mini_program"]
    url: str | None = None
    mini_program_app_id: str | None = None
    mini_program_path: str | None = None


@dataclass(slots=True)
class WechatAccessTokenSnapshot:
    app_id: str
    access_token: str
    expires_at: datetime
    fetched_at: datetime
    environment: str | None = None
    trace_id: str | None = None


@dataclass(slots=True)
class WechatOfficialAccountMessage:
    message_id: str
    send_record_bid: str | None
    app_id: str
    to_user: str
    template_id: str
    data: dict[str, WechatTemplateField] = field(default_factory=dict)
    link: WechatLink | None = None
    language: str | None = None
    state: WechatNotificationState = WechatNotificationState.PENDING
    vendor_msg_id: str | None = None
    vendor_status_code: int | None = None
    vendor_error_message: str | None = None
    retry_count: int = 0
    queued_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_attempt_at: datetime | None = None
    idempotency_key: str | None = None
    raw_request: dict[str, Any] | None = None


@dataclass(slots=True)
class WechatCallbackEvent:
    event_type: str
    message_id: str | None
    vendor_msg_id: str | None
    occurred_at: datetime
    payload: dict[str, Any]
    raw_message: str | None = None


@dataclass(slots=True)
class WechatDomainEvent:
    message_id: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class MessageQueued(WechatDomainEvent):
    reason: str | None = None


@dataclass(slots=True)
class VendorAccepted(WechatDomainEvent):
    vendor_msg_id: str
    raw_response: dict[str, Any] | None = None


@dataclass(slots=True)
class VendorFailed(WechatDomainEvent):
    error_code: int
    error_message: str
    raw_response: dict[str, Any] | None = None


@dataclass(slots=True)
class RetryScheduled(WechatDomainEvent):
    attempt: int
    next_attempt_at: datetime
    reason: str


@dataclass(slots=True)
class DeliveryConfirmed(WechatDomainEvent):
    vendor_msg_id: str
    event: str
    raw_event: dict[str, Any]


@dataclass(slots=True)
class DeliveryFailed(WechatDomainEvent):
    vendor_msg_id: str
    event: str
    error_code: int | None = None
    error_message: str | None = None
    raw_event: dict[str, Any] = field(default_factory=dict)
