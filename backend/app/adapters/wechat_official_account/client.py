from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any
import uuid

import httpx
from sqlalchemy.orm import Session

from ...core.config import settings
from ...domain.notifications import WechatOfficialAccountMessage
from .errors import raise_for_errcode
from .token_provider import WechatAccessTokenProvider

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class SendResult:
    errcode: int
    errmsg: str
    response: dict[str, Any]
    msg_id: str | None = None

    @property
    def success(self) -> bool:
        return self.errcode == 0


class WechatOfficialAccountClient:
    """HTTP client for WeChat Official Account messaging APIs."""

    def __init__(
        self,
        token_provider: WechatAccessTokenProvider | None = None,
    ) -> None:
        self._token_provider = token_provider or WechatAccessTokenProvider()
        self._config = settings.WECHAT_OFFICIAL_ACCOUNT

    def send_template_message(
        self,
        db: Session,
        message: WechatOfficialAccountMessage,
        *,
        force_refresh_token: bool = False,
        app_secret: str | None = None,
    ) -> SendResult:
        app_id = message.app_id or self._config.app_id
        if not app_id:
            raise ValueError("app_id is required on message or global configuration")
        access_token = self._token_provider.get_token(
            db,
            app_id=app_id,
            app_secret=app_secret,
            force_refresh=force_refresh_token,
        )
        payload = self._build_template_payload(message)
        data = self._post(
            endpoint=self._config.api.template_send_endpoint,
            payload=payload,
            token=access_token,
            app_id=app_id,
        )
        msg_id = data.get("msgid") or data.get("msg_id")
        return SendResult(errcode=data.get("errcode", 0), errmsg=data.get("errmsg", "ok"), response=data, msg_id=msg_id)

    def send_custom_message(
        self,
        db: Session,
        *,
        payload: dict[str, Any],
        app_id: str | None = None,
        app_secret: str | None = None,
        force_refresh_token: bool = False,
    ) -> SendResult:
        app_id = app_id or self._config.app_id
        if not app_id:
            raise ValueError("app_id is required for custom message sending")
        access_token = self._token_provider.get_token(
            db,
            app_id=app_id,
            app_secret=app_secret,
            force_refresh=force_refresh_token,
        )
        data = self._post(
            endpoint=self._config.api.custom_send_endpoint,
            payload=payload,
            token=access_token,
            app_id=app_id,
        )
        return SendResult(errcode=data.get("errcode", 0), errmsg=data.get("errmsg", "ok"), response=data, msg_id=data.get("msgid"))

    def _build_template_payload(self, message: WechatOfficialAccountMessage) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for key, field in message.data.items():
            entry: dict[str, Any] = {"value": field.value}
            if field.color:
                entry["color"] = field.color
            data[key] = entry

        payload: dict[str, Any] = {
            "touser": message.to_user,
            "template_id": message.template_id,
            "data": data,
        }
        if message.link:
            if message.link.link_type == "url" and message.link.url:
                payload["url"] = message.link.url
            elif message.link.link_type == "mini_program":
                mini: dict[str, Any] = {}
                if message.link.mini_program_app_id:
                    mini["appid"] = message.link.mini_program_app_id
                if message.link.mini_program_path:
                    mini["pagepath"] = message.link.mini_program_path
                if mini:
                    payload["miniprogram"] = mini
        if message.language:
            payload["lang"] = message.language
        if message.idempotency_key:
            payload["client_msg_id"] = message.idempotency_key
        return payload

    def _post(
        self,
        *,
        endpoint: str,
        payload: dict[str, Any],
        token: str,
        app_id: str,
    ) -> dict[str, Any]:
        params = {"access_token": token}
        trace_id = uuid.uuid4().hex
        with httpx.Client(base_url=str(self._config.api.base_url), timeout=5.0) as client:
            resp = client.post(endpoint, params=params, json=payload)
        try:
            data: dict[str, Any] = resp.json()
        except ValueError as exc:
            logger.error(
                "invalid wechat response",
                extra={"app_id": app_id, "trace_id": trace_id, "endpoint": endpoint, "status_code": resp.status_code},
                exc_info=exc,
            )
            raise ValueError("Failed to decode WeChat response") from exc

        errcode = data.get("errcode", 0)
        errmsg = data.get("errmsg", "") or resp.text
        logger.debug(
            "wechat api call",
            extra={
                "app_id": app_id,
                "trace_id": trace_id,
                "endpoint": endpoint,
                "status_code": resp.status_code,
                "errcode": errcode,
            },
        )
        if resp.status_code != 200 or errcode:
            raise_for_errcode(errcode or resp.status_code, errmsg, response=data)
        return data
