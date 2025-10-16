from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any
import uuid

import httpx
from sqlalchemy.orm import Session

from ...core.config import settings
from ...repository import wechat_official_account as repo
from .errors import raise_for_errcode

logger = logging.getLogger(__name__)


class WechatAccessTokenProvider:
    """Fetches and caches WeChat Official Account access tokens."""

    def __init__(self, *, refresh_margin_seconds: int = 300) -> None:
        self._config = settings.WECHAT_OFFICIAL_ACCOUNT
        self._refresh_margin = refresh_margin_seconds

    def get_token(
        self,
        db: Session,
        *,
        app_id: str | None = None,
        app_secret: str | None = None,
        force_refresh: bool = False,
    ) -> str:
        conf = self._config
        app_id = app_id or conf.app_id
        app_secret = app_secret or conf.app_secret
        if not app_id or not app_secret:
            raise ValueError("app_id and app_secret are required to fetch access token")

        record = repo.get_token_by_app_id(db, app_id=app_id)
        now = datetime.now(timezone.utc)
        if record and not force_refresh:
            expires_at = record.expires_at
            if expires_at and expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            # consider valid if not close to expiration
            remaining = (expires_at - now).total_seconds() if expires_at else -1
            if remaining > self._refresh_margin:
                logger.debug("wechat token cache hit", extra={"app_id": app_id, "remaining": remaining})
                return record.access_token

        trace_id = uuid.uuid4().hex
        access_token, expires_in = self._request_token(app_id=app_id, app_secret=app_secret, trace_id=trace_id)
        ttl = min(expires_in, conf.api.token_ttl_seconds)
        expires_at = now + timedelta(seconds=ttl)
        repo.upsert_token(
            db,
            app_id=app_id,
            access_token=access_token,
            expires_at=expires_at,
            environment=settings.ENV,
            trace_id=trace_id,
        )
        logger.info(
            "wechat token refreshed",
            extra={"app_id": app_id, "trace_id": trace_id, "expires_at": expires_at.isoformat()},
        )
        return access_token

    def invalidate(self, db: Session, *, app_id: str) -> None:
        repo.mark_token_deleted(db, app_id=app_id)

    def _request_token(self, *, app_id: str, app_secret: str, trace_id: str) -> tuple[str, int]:
        api_conf = self._config.api
        params = {
            "grant_type": "client_credential",
            "appid": app_id,
            "secret": app_secret,
        }
        with httpx.Client(base_url=str(api_conf.base_url), timeout=5.0) as client:
            resp = client.get(api_conf.token_endpoint, params=params)
        try:
            data: dict[str, Any] = resp.json()
        except ValueError as exc:
            logger.error("invalid wechat token response", extra={"app_id": app_id, "trace_id": trace_id, "status_code": resp.status_code, "body": resp.text[:2000]}, exc_info=exc)
            raise ValueError("Failed to decode WeChat token response") from exc
        errcode = data.get("errcode", 0)
        errmsg = data.get("errmsg", "") or "ok"
        if resp.status_code != 200:
            raise_for_errcode(errcode or resp.status_code, errmsg or resp.text, response=data)
        if errcode:
            raise_for_errcode(errcode, errmsg, response=data)
        access_token = data.get("access_token")
        expires_in = int(data.get("expires_in") or api_conf.token_ttl_seconds)
        if not access_token:
            raise ValueError("WeChat token response missing access_token")
        logger.debug(
            "wechat token fetched",
            extra={"app_id": app_id, "trace_id": trace_id, "expires_in": expires_in},
        )
        return access_token, expires_in
