from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
try:
    from prometheus_client import REGISTRY
except ImportError:  # pragma: no cover - optional dependency
    REGISTRY = None

from backend.app.adapters.wechat_official_account.errors import WechatAPIError, WechatErrorCategory
from backend.app.adapters.wechat_official_account.token_provider import WechatAccessTokenProvider
from backend.app.core.config import settings
from backend.app.db import models
from backend.app.observability import metrics as metrics_module
from backend.app.repository import wechat_official_account as repo
from backend.app.services.gateway.base import GatewaySendResult
from backend.app.services.gateway.wechat_official_account import WechatGatewayService


@pytest.fixture(autouse=True)
def _reset_env(monkeypatch):
    original_token = settings.WECHAT_OFFICIAL_ACCOUNT.token
    original_app_id = settings.WECHAT_OFFICIAL_ACCOUNT.app_id
    original_app_secret = settings.WECHAT_OFFICIAL_ACCOUNT.app_secret
    original_public_key = settings.PUBLIC_API_KEY

    settings.WECHAT_OFFICIAL_ACCOUNT.token = "test-token"
    settings.WECHAT_OFFICIAL_ACCOUNT.app_id = "test-app"
    settings.WECHAT_OFFICIAL_ACCOUNT.app_secret = "test-secret"
    settings.PUBLIC_API_KEY = None

    yield

    settings.WECHAT_OFFICIAL_ACCOUNT.token = original_token
    settings.WECHAT_OFFICIAL_ACCOUNT.app_id = original_app_id
    settings.WECHAT_OFFICIAL_ACCOUNT.app_secret = original_app_secret
    settings.PUBLIC_API_KEY = original_public_key


def test_token_provider_cache(monkeypatch, db_session):
    call_counter = {"count": 0}

    class DummyResponse:
        status_code = 200

        def json(self) -> dict[str, str | int]:
            return {"access_token": "token-xyz", "expires_in": 7200}

        @property
        def text(self) -> str:
            return "{}"

    class DummyClient:
        def __init__(self, *args, **kwargs):
            call_counter["count"] += 1

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get(self, endpoint: str, params: dict[str, str]):
            assert endpoint == "/cgi-bin/token"
            assert params["appid"] == "test-app"
            return DummyResponse()

    monkeypatch.setattr(
        "backend.app.adapters.wechat_official_account.token_provider.httpx.Client",
        DummyClient,
    )

    provider = WechatAccessTokenProvider(refresh_margin_seconds=300)
    token = provider.get_token(db_session)
    assert token == "token-xyz"
    assert call_counter["count"] == 1

    # Cache hit
    token = provider.get_token(db_session)
    assert token == "token-xyz"
    assert call_counter["count"] == 1

    # Force refresh triggers another HTTP call
    token = provider.get_token(db_session, force_refresh=True)
    assert token == "token-xyz"
    assert call_counter["count"] == 2

    record = repo.get_token_by_app_id(db_session, app_id="test-app")
    assert record is not None
    assert record.access_token == "token-xyz"



def test_token_provider_refreshes_expiring(monkeypatch, db_session):
    call_counter = {"count": 0}

    class RefreshingClient:
        def __init__(self, *args, **kwargs):
            call_counter["count"] += 1

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get(self, endpoint: str, params: dict[str, str]):
            class DummyResponse:
                status_code = 200

                def json(self) -> dict[str, str | int]:
                    return {"access_token": f"token-{call_counter['count']}", "expires_in": 7200}

                @property
                def text(self) -> str:
                    return "{}"

            return DummyResponse()

    monkeypatch.setattr(
        "backend.app.adapters.wechat_official_account.token_provider.httpx.Client",
        RefreshingClient,
    )

    provider = WechatAccessTokenProvider(refresh_margin_seconds=300)
    provider.get_token(db_session)
    assert call_counter["count"] == 1

    record = repo.get_token_by_app_id(db_session, app_id="test-app")
    assert record is not None
    record.expires_at = datetime.now(timezone.utc) + timedelta(seconds=200)
    db_session.commit()

    provider.get_token(db_session)
    assert call_counter["count"] == 2


class _SuccessClient:
    def send_template_message(self, db, message, force_refresh_token: bool = False):
        from backend.app.adapters.wechat_official_account.client import SendResult

        return SendResult(errcode=0, errmsg="ok", response={}, msg_id="wx-success-1")


class _FailClient:
    def send_template_message(self, db, message, force_refresh_token: bool = False):
        raise WechatAPIError(
            errcode=45009,
            errmsg="rate limit",
            category=WechatErrorCategory.RATE_LIMIT,
            response=None,
        )


def _metric_value(name: str, labels: dict[str, str]) -> float:
    if REGISTRY is None:
        return 0.0
    value = REGISTRY.get_sample_value(name, labels=labels)
    return float(value) if value is not None else 0.0


def _reset_wechat_tables(db_session):
    db_session.query(models.WechatOfficialAccountMessage).delete()
    db_session.query(models.WechatOfficialAccountToken).delete()
    db_session.query(models.WechatOfficialAccountEvent).delete()
    db_session.commit()


def test_gateway_send_success_records_message(db_session):
    _reset_wechat_tables(db_session)
    before = _metric_value(
        "orion_wechat_send_attempts_total",
        {"result": "success", "app_id": "test-app", "errcode": "0"},
    ) if metrics_module.PROMETHEUS_ENABLED else None
    service = WechatGatewayService(client=_SuccessClient())
    payload = {
        "template_id": "tmpl-success",
        "to_user": "openid-1",
        "data": {"first": {"value": "hello"}},
        "context": {"name": "Alice"},
    }
    result = service.send(db_session, payload)
    db_session.commit()

    assert result.success is True
    message = repo.get_message_by_bid(db_session, message_bid=result.message_bid)
    assert message is not None
    assert message.state == "success"
    assert message.vendor_msg_id == "wx-success-1"

    if metrics_module.PROMETHEUS_ENABLED:
        after = _metric_value(
            "orion_wechat_send_attempts_total",
            {"result": "success", "app_id": "test-app", "errcode": "0"},
        )
        assert after == before + 1


def test_gateway_send_failure_marks_retry(db_session):
    _reset_wechat_tables(db_session)
    before = _metric_value(
        "orion_wechat_send_attempts_total",
        {"result": "error", "app_id": "test-app", "errcode": "45009"},
    ) if metrics_module.PROMETHEUS_ENABLED else None
    service = WechatGatewayService(client=_FailClient())
    payload = {
        "template_id": "tmpl-fail",
        "to_user": "openid-x",
        "data": {"first": {"value": "fail"}},
        "context": {},
    }
    result = service.send(db_session, payload)
    db_session.commit()

    assert result.success is False
    message = repo.get_message_by_bid(db_session, message_bid=result.message_bid)
    assert message is not None
    assert message.state == "retrying"
    assert message.last_error_code == 45009
    assert message.retry_count == 1

    if metrics_module.PROMETHEUS_ENABLED:
        after = _metric_value(
            "orion_wechat_send_attempts_total",
            {"result": "error", "app_id": "test-app", "errcode": "45009"},
        )
        assert after == before + 1


def test_notifications_api_send(monkeypatch, client):
    class DummyGateway:
        def __init__(self):
            self.sent = []

        def send(self, db, payload):
            self.sent.append(payload)
            return GatewaySendResult(
                success=True,
                message_bid="api-msg-1",
                vendor_msg_id="wx-api-1",
                state="success",
            )

        def retry(self, db, message_bid):
            return GatewaySendResult(
                success=True,
                message_bid=message_bid,
                vendor_msg_id="wx-api-1",
                state="success",
            )

    gateway = DummyGateway()
    monkeypatch.setattr("backend.app.api.v1.notifications.WechatGatewayService", lambda: gateway)

    response = client.post(
        "/api/v1/notifications/wechat/template",
        json={
            "touser": "openid-42",
            "template_id": "tmpl-api",
            "data": {"keyword1": {"value": "hello"}},
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["message_bid"] == "api-msg-1"
    assert gateway.sent

    retry_resp = client.post("/api/v1/notifications/wechat/api-msg-1/retry")
    assert retry_resp.status_code == 200
    assert retry_resp.json()["message_bid"] == "api-msg-1"
