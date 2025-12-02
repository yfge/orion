"""Integration tests for wechat channel via unified /notify endpoint."""
from __future__ import annotations

import uuid

import pytest

from backend.app.db import models
from backend.app.repository import dispatches as disp_repo
from backend.app.repository import endpoints as ep_repo
from backend.app.repository import message_definitions as msg_repo
from backend.app.services.gateway.base import GatewaySendResult
from backend.app.services.notify import notify_by_name


class MockWechatGateway:
    """Mock wechat gateway for testing."""

    def __init__(self, success: bool = True, vendor_msg_id: str = "wx-mock-123"):
        self.success = success
        self.vendor_msg_id = vendor_msg_id
        self.sent_payloads = []

    def send(self, db, payload):
        self.sent_payloads.append(payload)
        return GatewaySendResult(
            success=self.success,
            message_bid="wechat-msg-001",
            vendor_msg_id=self.vendor_msg_id if self.success else None,
            state="success" if self.success else "failed",
            error=None if self.success else "mock error",
        )

    def retry(self, db, message_bid):
        return self.send(db, {})


@pytest.fixture
def wechat_gateway_mock(monkeypatch):
    """Replace wechat gateway with mock."""
    mock_gateway = MockWechatGateway()

    def mock_get_channel(key: str):
        if key == "wechat_official_account":
            return mock_gateway
        raise KeyError(f"channel '{key}' not registered")

    monkeypatch.setattr("backend.app.services.notify.get_channel", mock_get_channel)
    return mock_gateway


@pytest.fixture
def wechat_message_setup(db_session):
    """Setup message definition, endpoint, and dispatch for wechat."""
    # Create unique suffix
    unique_suffix = uuid.uuid4().hex[:8]

    # Create business system
    system = models.BusinessSystem(name=f"Test System {unique_suffix}")
    db_session.add(system)
    db_session.flush()

    # Create message definition
    msg_def = models.MessageDefinition(
        name=f"wechat_order_notify_{unique_suffix}",
        schema={
            "template_id": "TM00000001",
            "to_user": "${openid}",
            "data": {
                "first": {"value": "订单通知"},
                "keyword1": {"value": "${order_no}"},
                "keyword2": {"value": "${amount}"},
                "remark": {"value": "感谢您的购买"},
            },
        },
    )
    db_session.add(msg_def)
    db_session.flush()

    # Create wechat endpoint with channel adapter
    endpoint = models.NotificationAPI(
        business_system_bid=system.business_system_bid,
        name="Wechat Official Account",
        endpoint_url="https://api.weixin.qq.com",
        transport="channel",
        adapter_key="channel.wechat_official_account",
        config={
            "app_id": "wx1234567890",
            "language": "zh_CN",
        },
    )
    db_session.add(endpoint)
    db_session.flush()

    # Create dispatch
    dispatch = models.MessageDispatch(
        message_definition_bid=msg_def.message_definition_bid,
        notification_api_bid=endpoint.notification_api_bid,
        enabled=True,
        mapping={
            "link": {
                "type": "url",
                "url": "https://example.com/order/${order_no}",
            }
        },
    )
    db_session.add(dispatch)
    db_session.commit()

    return {
        "message_name": msg_def.name,
        "message_bid": msg_def.message_definition_bid,
        "endpoint_bid": endpoint.notification_api_bid,
    }


def test_notify_wechat_via_gateway_success(db_session, wechat_gateway_mock, wechat_message_setup):
    """Test sending wechat notification via unified notify endpoint."""
    data = {
        "openid": "oABCD1234567890",
        "order_no": "ORD20251202001",
        "amount": "299.00",
    }

    results = notify_by_name(db_session, message_name=wechat_message_setup["message_name"], data=data)
    db_session.commit()

    assert len(results) == 1
    result = results[0]

    # Verify result structure
    assert result["success"] is True
    assert result["channel"] == "wechat_official_account"
    assert result["message_bid"] == "wechat-msg-001"
    assert result["vendor_msg_id"] == "wx-mock-123"
    assert result["status"] == "success"

    # Verify gateway received correct payload
    assert len(wechat_gateway_mock.sent_payloads) == 1
    payload = wechat_gateway_mock.sent_payloads[0]

    assert payload["template_id"] == "TM00000001"
    assert payload["to_user"] == "oABCD1234567890"
    assert payload["data"]["keyword1"]["value"] == "ORD20251202001"
    assert payload["data"]["keyword2"]["value"] == "299.00"
    assert payload["link"]["url"] == "https://example.com/order/ORD20251202001"
    assert payload["app_id"] == "wx1234567890"
    assert payload["language"] == "zh_CN"
    assert payload["context"] == data

    # Verify send_record created
    from backend.app.repository import send_records as rec_repo

    records, _ = rec_repo.list_send_records(
        db_session, notification_api_bid=wechat_message_setup["endpoint_bid"], limit=10, offset=0
    )
    assert len(records) == 1
    record = records[0]
    assert record.status == 1
    assert record.result["vendor_msg_id"] == "wx-mock-123"


def test_notify_wechat_via_gateway_failure(db_session, monkeypatch, wechat_message_setup):
    """Test handling wechat notification failure."""
    mock_gateway = MockWechatGateway(success=False)

    def mock_get_channel(key: str):
        if key == "wechat_official_account":
            return mock_gateway
        raise KeyError(f"channel '{key}' not registered")

    monkeypatch.setattr("backend.app.services.notify.get_channel", mock_get_channel)

    data = {
        "openid": "oABCD1234567890",
        "order_no": "ORD20251202002",
        "amount": "199.00",
    }

    results = notify_by_name(db_session, message_name=wechat_message_setup["message_name"], data=data)
    db_session.commit()

    assert len(results) == 1
    result = results[0]

    # Verify failure recorded
    assert result["success"] is False
    assert result["channel"] == "wechat_official_account"
    assert result["status"] == "failed"

    # Verify send_record marked as failed
    from backend.app.repository import send_records as rec_repo

    records, _ = rec_repo.list_send_records(
        db_session, notification_api_bid=wechat_message_setup["endpoint_bid"], limit=10, offset=0
    )
    assert len(records) == 1
    record = records[0]
    assert record.status == -1
    assert record.result["error"] == "mock error"


def test_notify_wechat_channel_not_registered(db_session, monkeypatch, wechat_message_setup):
    """Test handling when wechat channel is not registered."""

    def mock_get_channel_missing(key: str):
        raise KeyError(f"channel '{key}' not registered")

    monkeypatch.setattr("backend.app.services.notify.get_channel", mock_get_channel_missing)

    data = {
        "openid": "oABCD1234567890",
        "order_no": "ORD20251202003",
        "amount": "99.00",
    }

    results = notify_by_name(db_session, message_name=wechat_message_setup["message_name"], data=data)
    db_session.commit()

    assert len(results) == 1
    result = results[0]

    # Should return error about missing channel
    assert "error" in result
    assert "not registered" in result["error"]


def test_notify_mixed_channels(db_session, wechat_gateway_mock, wechat_message_setup):
    """Test notification with both wechat and http endpoints."""
    # Add a regular HTTP endpoint to the same message
    msg = msg_repo.get_by_name(db_session, wechat_message_setup["message_name"])
    # Get business_system_bid from existing endpoint
    existing_ep = ep_repo.get_by_bid(db_session, wechat_message_setup["endpoint_bid"])
    system_bid = existing_ep.business_system_bid

    http_endpoint = models.NotificationAPI(
        business_system_bid=system_bid,
        name="HTTP Webhook",
        endpoint_url="https://example.com/webhook",
        transport="http",
        adapter_key="http.generic",
    )
    db_session.add(http_endpoint)
    db_session.flush()

    http_dispatch = models.MessageDispatch(
        message_definition_bid=msg.message_definition_bid,
        notification_api_bid=http_endpoint.notification_api_bid,
        enabled=True,
    )
    db_session.add(http_dispatch)
    db_session.commit()

    # Mock HTTP sender
    class MockHttpSender:
        def send(self, endpoint, payload):
            return {"status_code": 200, "body": {"ok": True}}

    monkeypatch_http = pytest.MonkeyPatch()
    monkeypatch_http.setattr("backend.app.services.notify.HttpSender", MockHttpSender)

    data = {
        "openid": "oABCD1234567890",
        "order_no": "ORD20251202004",
        "amount": "399.00",
    }

    results = notify_by_name(db_session, message_name=wechat_message_setup["message_name"], data=data)
    db_session.commit()

    # Should have 2 results: 1 wechat + 1 http
    assert len(results) == 2

    # Find wechat result
    wechat_result = next((r for r in results if r.get("channel") == "wechat_official_account"), None)
    assert wechat_result is not None
    assert wechat_result["success"] is True

    # Find http result
    http_result = next((r for r in results if "status_code" in r), None)
    assert http_result is not None
    assert http_result["status_code"] == 200

    monkeypatch_http.undo()
