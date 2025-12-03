from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ...core.config import settings
from ...deps.api_key import require_api_key
from ...deps.db import get_db
from ...repository import wechat_official_account as repo
from ...services.gateway import WechatGatewayService
from ...services.gateway.base import GatewaySendResult
from ...schemas.wechat_official_account import (
    WechatLinkInput,
    WechatNotificationDetail,
    WechatNotificationOut,
    WechatTemplateMessageRequest,
)

router = APIRouter(prefix="/notifications/wechat", tags=["notifications"], dependencies=[Depends(require_api_key)])


def _result_to_response(result: GatewaySendResult) -> WechatNotificationOut:
    return WechatNotificationOut(
        message_bid=result.message_bid,
        state=result.state or ("success" if result.success else "failed"),
        vendor_msg_id=result.vendor_msg_id,
        error=result.error,
        retry_scheduled=result.retry_scheduled,
    )


@router.post("/template", response_model=WechatNotificationOut, status_code=status.HTTP_201_CREATED)
def send_template_message(
    payload: WechatTemplateMessageRequest,
    db: Session = Depends(get_db),
):
    gateway = WechatGatewayService()
    gateway_payload: dict[str, Any] = {
        "template_id": payload.template_id,
        "to_user": payload.to_user,
        "data": {k: v.model_dump() for k, v in payload.data.items()},
        "context": payload.context,
        "link": payload.link.model_dump(by_alias=True) if payload.link else None,
        "language": payload.language,
        "idempotency_key": payload.idempotency_key,
        "app_id": payload.app_id,
        "app_secret": payload.app_secret,
    }
    if not gateway_payload["app_id"]:
        gateway_payload["app_id"] = settings.WECHAT_OFFICIAL_ACCOUNT.app_id
    if not gateway_payload.get("app_secret"):
        gateway_payload["app_secret"] = settings.WECHAT_OFFICIAL_ACCOUNT.app_secret
    if not gateway_payload["app_id"] or not gateway_payload.get("app_secret"):
        raise HTTPException(status_code=400, detail="app_id/app_secret not configured for WeChat")
    try:
        result = gateway.send(db, gateway_payload)
        db.commit()
    except Exception as exc:  # pragma: no cover - propagate with rollback
        db.rollback()
        raise
    return _result_to_response(result)


@router.get("/{message_bid}", response_model=WechatNotificationDetail)
def get_wechat_notification(message_bid: str, db: Session = Depends(get_db)) -> WechatNotificationDetail:
    record = repo.get_message_by_bid(db, message_bid=message_bid)
    if not record:
        raise HTTPException(status_code=404, detail="notification not found")
    link = None
    if record.link_type:
        try:
            link = WechatLinkInput.model_validate(
                {
                    "type": record.link_type,
                    "url": record.link_url,
                    "app_id": record.mini_program_app_id,
                    "path": record.mini_program_path,
                }
            )
        except ValidationError:
            link = None
    payload = record.data_payload or {}
    data = payload.get("data") if isinstance(payload, dict) else None
    context = payload.get("context") if isinstance(payload, dict) else None
    return WechatNotificationDetail(
        message_bid=record.wechat_message_bid,
        app_id=record.app_id,
        to_user=record.to_user,
        template_id=record.template_id,
        language=record.language,
        link=link,
        data=data,
        context=context,
        state=record.state,
        vendor_msg_id=record.vendor_msg_id,
        last_error_code=record.last_error_code,
        last_error_message=record.last_error_message,
        retry_count=record.retry_count,
        queued_at=record.queued_at,
        last_attempt_at=record.last_attempt_at,
        updated_at=record.updated_at,
    )


@router.post("/{message_bid}/retry", response_model=WechatNotificationOut)
def retry_wechat_notification(message_bid: str, db: Session = Depends(get_db)) -> WechatNotificationOut:
    gateway = WechatGatewayService()
    try:
        result = gateway.retry(db, message_bid)
        db.commit()
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception:
        db.rollback()
        raise
    return _result_to_response(result)
