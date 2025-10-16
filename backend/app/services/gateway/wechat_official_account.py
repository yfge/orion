from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from time import perf_counter
from typing import Any

from sqlalchemy.orm import Session

from ...db import models
from ...adapters.wechat_official_account import WechatAPIError, WechatOfficialAccountClient
from ...core.config import settings
from ...domain.notifications import (
    WechatLink,
    WechatNotificationState,
    WechatOfficialAccountMessage,
    WechatTemplateField,
)
from ...observability.metrics import record_wechat_send
from ...repository import wechat_official_account as repo
from ...services.templating import render_value
from .base import ChannelGateway, GatewaySendResult
from .registry import register_channel

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class WechatSendPayload:
    template_id: str
    to_user: str
    data: dict[str, Any]
    context: dict[str, Any]
    link: dict[str, Any] | None = None
    language: str | None = None
    idempotency_key: str | None = None
    app_id: str | None = None
    message_type: str = "template"
    custom_payload: dict[str, Any] | None = None


class WechatGatewayService(ChannelGateway):
    key = "wechat_official_account"

    def __init__(self, client: WechatOfficialAccountClient | None = None) -> None:
        self._client = client or WechatOfficialAccountClient()
        self._config = settings.WECHAT_OFFICIAL_ACCOUNT

    def send(self, db: Session, payload: dict[str, Any]) -> GatewaySendResult:
        request = WechatSendPayload(**payload)
        if request.message_type == "custom":
            return self._send_custom_message(db, request)
        return self._send_template_message(db, request)

    def retry(self, db: Session, message_bid: str) -> GatewaySendResult:
        record = repo.get_message_by_bid(db, message_bid=message_bid)
        if not record:
            raise ValueError(f"message {message_bid} not found")
        payload = WechatSendPayload(
            template_id=record.template_id,
            to_user=record.to_user,
            data=(record.data_payload or {}).get("data", {}),
            context=(record.data_payload or {}).get("context", {}),
            link=(record.data_payload or {}).get("link"),
            language=record.language,
            idempotency_key=record.idempotency_key,
            app_id=record.app_id,
        )
        return self._send_template_message(db, payload, existing_record=record)

    def _send_template_message(
        self,
        db: Session,
        request: WechatSendPayload,
        *,
        existing_record: models.WechatOfficialAccountMessage | None = None,
    ) -> GatewaySendResult:
        message = self._build_domain_message(request, existing_record=existing_record)
        record = existing_record
        if not record:
            record = repo.create_message_record(
                db,
                message_bid=message.message_id,
                send_record_bid=message.send_record_bid,
                app_id=message.app_id,
                to_user=message.to_user,
                template_id=message.template_id,
                language=message.language,
                link_type=message.link.link_type if message.link else None,
                link_url=message.link.url if message.link else None,
                mini_program_app_id=message.link.mini_program_app_id if message.link else None,
                mini_program_path=message.link.mini_program_path if message.link else None,
                data_payload=self._serialize_payload(request),
                raw_request=self._serialize_raw_request(request),
                idempotency_key=message.idempotency_key,
                state=message.state.value,
            )
        repo.update_message_state(db, record, state=WechatNotificationState.SENDING.value)

        app_id = message.app_id
        vendor_msg_id: str | None = None
        started = perf_counter()
        try:
            result = self._client.send_template_message(db, message)
        except WechatAPIError as exc:
            elapsed = perf_counter() - started
            record_wechat_send("error", app_id, elapsed, errcode=exc.errcode)
            repo.mark_message_failure(
                db,
                record,
                error_code=exc.errcode,
                error_message=exc.errmsg,
                retrying=exc.retryable,
            )
            retry_scheduled = False
            if exc.retryable:
                retry_scheduled = self._schedule_retry(db, record.wechat_message_bid)
            logger.warning(
                "wechat template send failed",
                extra={
                    "event": "wechat.template.send.failure",
                    "message_bid": record.wechat_message_bid,
                    "vendor_msg_id": vendor_msg_id,
                    "app_id": app_id,
                    "errcode": exc.errcode,
                    "errmsg": exc.errmsg,
                    "retry_scheduled": retry_scheduled,
                    "latency_ms": round(elapsed * 1000, 2),
                },
            )
            return GatewaySendResult(
                success=False,
                message_bid=record.wechat_message_bid,
                state=record.state,
                error=exc.errmsg,
                retry_scheduled=retry_scheduled,
            )
        except Exception:
            elapsed = perf_counter() - started
            record_wechat_send("exception", app_id, elapsed)
            logger.exception(
                "wechat template send exception",
                extra={
                    "event": "wechat.template.send.exception",
                    "message_bid": record.wechat_message_bid,
                    "app_id": app_id,
                    "latency_ms": round(elapsed * 1000, 2),
                },
            )
            raise

        elapsed = perf_counter() - started
        record_wechat_send("success", app_id, elapsed, errcode=0)
        vendor_msg_id = result.msg_id or ""
        repo.mark_message_success(db, record, vendor_msg_id=vendor_msg_id)
        logger.info(
            "wechat template send success",
            extra={
                "event": "wechat.template.send.success",
                "message_bid": record.wechat_message_bid,
                "vendor_msg_id": vendor_msg_id,
                "app_id": app_id,
                "latency_ms": round(elapsed * 1000, 2),
            },
        )
        return GatewaySendResult(
            success=True,
            message_bid=record.wechat_message_bid,
            vendor_msg_id=vendor_msg_id,
            state=WechatNotificationState.SUCCESS.value,
        )

    def _send_custom_message(self, db: Session, request: WechatSendPayload) -> GatewaySendResult:
        if not request.custom_payload:
            raise ValueError("custom_payload is required for custom message type")
        app_id = request.app_id or self._config.app_id
        if not app_id:
            raise ValueError("app_id is required")
        started = perf_counter()
        try:
            result = self._client.send_custom_message(
                db,
                payload=request.custom_payload,
                app_id=app_id,
            )
        except WechatAPIError as exc:
            elapsed = perf_counter() - started
            record_wechat_send("error", app_id, elapsed, errcode=exc.errcode)
            retry_scheduled = exc.retryable and self._schedule_retry(db, None)
            logger.warning(
                "wechat custom message failed",
                extra={
                    "event": "wechat.custom.send.failure",
                    "app_id": app_id,
                    "errcode": exc.errcode,
                    "errmsg": exc.errmsg,
                    "retry_scheduled": retry_scheduled,
                    "latency_ms": round(elapsed * 1000, 2),
                },
            )
            return GatewaySendResult(
                success=False,
                message_bid="",
                error=exc.errmsg,
                retry_scheduled=retry_scheduled,
            )
        except Exception:
            elapsed = perf_counter() - started
            record_wechat_send("exception", app_id, elapsed)
            logger.exception(
                "wechat custom message exception",
                extra={
                    "event": "wechat.custom.send.exception",
                    "app_id": app_id,
                    "latency_ms": round(elapsed * 1000, 2),
                },
            )
            raise

        elapsed = perf_counter() - started
        result_state = "success" if result.success else "failed"
        record_wechat_send("success" if result.success else "error", app_id, elapsed, errcode=0 if result.success else None)
        logger.info(
            "wechat custom message sent",
            extra={
                "event": "wechat.custom.send.success" if result.success else "wechat.custom.send.accepted",
                "app_id": app_id,
                "vendor_msg_id": result.msg_id,
                "latency_ms": round(elapsed * 1000, 2),
            },
        )
        return GatewaySendResult(success=result.success, message_bid="", vendor_msg_id=result.msg_id, state=result_state)

    def _build_domain_message(
        self,
        request: WechatSendPayload,
        *,
        existing_record: models.WechatOfficialAccountMessage | None = None,
    ) -> WechatOfficialAccountMessage:
        data_fields: dict[str, WechatTemplateField] = {}
        ctx = request.context or {}
        for key, raw in (request.data or {}).items():
            if isinstance(raw, dict):
                value_template = raw.get("value", "")
                color = raw.get("color")
            else:
                value_template = raw
                color = None
            rendered = render_value(value_template, ctx)
            data_fields[key] = WechatTemplateField(value=str(rendered), color=str(color) if color else None)
        link = None
        if request.link:
            link_type = (request.link.get("type") or "url").lower()
            if link_type not in {"url", "mini_program"}:
                link_type = "url"
            link = WechatLink(
                link_type=link_type,
                url=request.link.get("url"),
                mini_program_app_id=request.link.get("app_id") or request.link.get("appid"),
                mini_program_path=request.link.get("pagepath") or request.link.get("path"),
            )
        message_id = existing_record.wechat_message_bid if existing_record else uuid.uuid4().hex
        send_record_bid = existing_record.send_record_bid if existing_record else uuid.uuid4().hex
        app_id = request.app_id or self._config.app_id
        if not app_id:
            raise ValueError("app_id is required")
        return WechatOfficialAccountMessage(
            message_id=message_id,
            send_record_bid=send_record_bid,
            app_id=app_id,
            to_user=request.to_user,
            template_id=request.template_id,
            data=data_fields,
            link=link,
            language=request.language,
            state=WechatNotificationState.PENDING,
            idempotency_key=request.idempotency_key,
            raw_request=self._serialize_raw_request(request),
        )

    def _serialize_payload(self, request: WechatSendPayload) -> dict[str, Any]:
        return {
            "data": request.data,
            "context": request.context,
            "link": request.link,
        }

    def _serialize_raw_request(self, request: WechatSendPayload) -> dict[str, Any]:
        return {
            "template_id": request.template_id,
            "to_user": request.to_user,
            "language": request.language,
            "idempotency_key": request.idempotency_key,
            "app_id": request.app_id,
            "message_type": request.message_type,
            "custom_payload": request.custom_payload,
        }

    def _schedule_retry(self, db: Session, message_bid: str | None) -> bool:  # pragma: no cover - scheduler to be implemented
        logger.info(
            "schedule retry placeholder",
            extra={"message_bid": message_bid},
        )
        return False


register_channel(
    WechatGatewayService.key,
    factory=WechatGatewayService,
    capabilities={
        "template": True,
        "custom_message": True,
        "retry": True,
        "recall": False,
    },
)
