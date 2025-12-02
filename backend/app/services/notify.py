from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from ..db.models import MessageDefinition, SendDetail, SendRecord
from ..repository import dispatches as disp_repo
from ..repository import endpoints as ep_repo
from ..repository import message_definitions as msg_repo
from .gateway import get_channel
from .sender.http_sender import HttpSender
from .sender.smtp_sender import SmtpSender
from .templating import render_value


def _dispatch_via_gateway(
    db: Session,
    *,
    ep: Any,
    message: MessageDefinition,
    base_payload: Any,
    mapping: dict[str, Any],
    data: dict[str, Any],
    remark: str | None,
) -> dict[str, Any]:
    """Dispatch notification via channel gateway (e.g., wechat_official_account)."""
    adapter_key = ep.adapter_key or ""
    channel_key = adapter_key.replace("channel.", "", 1)

    try:
        gateway = get_channel(channel_key)
    except KeyError:
        return {
            "endpoint_bid": ep.notification_api_bid,
            "error": f"channel '{channel_key}' not registered",
        }

    # Prepare SendRecord
    send_record = SendRecord(
        message_definition_bid=message.message_definition_bid,
        notification_api_bid=ep.notification_api_bid,
        status=0,
    )
    if remark:
        send_record.remark = remark
    db.add(send_record)
    db.flush()

    # Merge mapping, render context
    rendered_mapping = render_value(mapping, data)
    gateway_payload = base_payload
    if isinstance(gateway_payload, dict) and isinstance(rendered_mapping, dict):
        gateway_payload = {**gateway_payload, **rendered_mapping}

    # Merge endpoint config
    endpoint_config = ep.config or {}
    if isinstance(gateway_payload, dict):
        gateway_payload = {**endpoint_config, **gateway_payload}

    # Add template rendering context
    if isinstance(gateway_payload, dict):
        gateway_payload["context"] = data

    try:
        result = gateway.send(db, gateway_payload)

        # Update send record based on gateway result
        send_record.status = 1 if result.success else -1
        send_record.send_time = datetime.now(UTC)
        send_record.result = {
            "success": result.success,
            "message_bid": result.message_bid,
            "vendor_msg_id": result.vendor_msg_id,
            "state": result.state,
            "error": result.error,
        }

        # Create send detail
        detail = SendDetail(
            send_record_bid=send_record.send_record_bid,
            notification_api_bid=ep.notification_api_bid,
            attempt_no=1,
            request_payload=gateway_payload if isinstance(gateway_payload, dict) else {"raw": str(gateway_payload)},
            response_payload=send_record.result,
            status=1 if result.success else -1,
            sent_at=datetime.now(UTC),
            error=result.error,
        )
        db.add(detail)

        return {
            "endpoint_bid": ep.notification_api_bid,
            "channel": channel_key,
            "message_bid": result.message_bid,
            "vendor_msg_id": result.vendor_msg_id,
            "status": result.state,
            "success": result.success,
        }
    except Exception as e:
        # Record failure
        detail = SendDetail(
            send_record_bid=send_record.send_record_bid,
            notification_api_bid=ep.notification_api_bid,
            attempt_no=1,
            request_payload=gateway_payload if isinstance(gateway_payload, dict) else {"raw": str(gateway_payload)},
            response_payload=None,
            status=-1,
            sent_at=datetime.now(UTC),
            error=str(e),
        )
        db.add(detail)
        send_record.status = -1
        return {
            "endpoint_bid": ep.notification_api_bid,
            "channel": channel_key,
            "error": str(e),
        }


def notify_by_name(
    db: Session, *, message_name: str, data: dict[str, Any], remark: str | None = None
) -> list[dict[str, Any]]:
    msg = msg_repo.get_by_name(db, message_name)
    if not msg:
        raise ValueError("message not found")
    return _notify(db, message=msg, schema=msg.schema or {}, data=data, remark=remark)


def notify_by_bid(
    db: Session, *, message_bid: str, data: dict[str, Any], remark: str | None = None
) -> list[dict[str, Any]]:
    msg = msg_repo.get_by_bid(db, message_bid)
    if not msg:
        raise ValueError("message not found")
    return _notify(db, message=msg, schema=msg.schema or {}, data=data, remark=remark)


def _notify(
    db: Session,
    *,
    message: MessageDefinition,
    schema: dict[str, Any],
    data: dict[str, Any],
    remark: str | None = None,
) -> list[dict[str, Any]]:
    # Render base payload from message schema
    base_payload = render_value(schema, data)
    # Fetch dispatches
    dispatches, _ = disp_repo.list_by_message(
        db, message_bid=message.message_definition_bid, limit=1000, offset=0
    )
    results: list[dict[str, Any]] = []
    http_sender = HttpSender()
    smtp_sender = SmtpSender()
    for d in dispatches:
        if not d.enabled:
            continue
        ep = ep_repo.get_by_bid(db, getattr(d, "endpoint_bid", None) or "")
        if not ep:
            continue

        # Check if this is a channel gateway (e.g., wechat)
        adapter_key = ep.adapter_key or ""
        if adapter_key.startswith("channel."):
            result = _dispatch_via_gateway(
                db, ep=ep, message=message, base_payload=base_payload,
                mapping=d.mapping or {}, data=data, remark=remark
            )
            results.append(result)
            continue
        # Prepare SendRecord
        send_record = SendRecord(
            message_definition_bid=message.message_definition_bid,
            notification_api_bid=ep.notification_api_bid,
            status=0,
        )
        if remark:
            send_record.remark = remark
        db.add(send_record)
        db.flush()
        endpoint_dict = {
            "adapter_key": ep.adapter_key
            or ("smtp.generic" if (ep.transport or "").lower() == "smtp" else "http.generic"),
            "endpoint_url": ep.endpoint_url,
            "config": (ep.config or {})
            | ({"url": ep.endpoint_url} if (ep.transport or "").lower() != "smtp" else {}),
            "auth_type": None,
            "auth_config": None,
        }
        # Merge mapping (after rendering), overrides base payload
        mapping = d.mapping or {}
        rendered_mapping = render_value(mapping, data)
        payload = base_payload
        if isinstance(payload, dict) and isinstance(rendered_mapping, dict):
            payload = {**payload, **rendered_mapping}

        if (ep.adapter_key or "").startswith("http.feishu") and not payload.get("msg_type"):
            # ensure Feishu format at minimum
            payload = {"msg_type": "text", "content": {"text": str(render_value("${text}", data))}}

        try:
            if (ep.transport or "").lower() == "smtp" or (ep.adapter_key or "").lower().startswith(
                "smtp."
            ):
                res = smtp_sender.send(endpoint=endpoint_dict, payload=payload)
            else:
                res = http_sender.send(endpoint=endpoint_dict, payload=payload)
            body = res.get("body")
            if isinstance(body, str):
                result_body: Any = {"raw": body}
            else:
                result_body = body
            # Update record and add detail
            send_record.status = 1
            send_record.send_time = datetime.now(UTC)
            send_record.result = result_body
            detail = SendDetail(
                send_record_bid=send_record.send_record_bid,
                notification_api_bid=ep.notification_api_bid,
                attempt_no=1,
                request_payload=payload if isinstance(payload, dict) else {"raw": str(payload)},
                response_payload=result_body,
                status=1,
                sent_at=datetime.now(UTC),
                error=None,
            )
            db.add(detail)
            results.append(
                {
                    "dispatch_bid": d.message_dispatch_bid,
                    "endpoint_bid": getattr(d, "endpoint_bid", None),
                    "status_code": int(res.get("status_code", 0)),
                    "body": res.get("body"),
                }
            )
        except Exception as e:  # pragma: no cover
            # failure detail
            detail = SendDetail(
                send_record_bid=send_record.send_record_bid,
                notification_api_bid=ep.notification_api_bid,
                attempt_no=1,
                request_payload=payload if isinstance(payload, dict) else {"raw": str(payload)},
                response_payload=None,
                status=-1,
                sent_at=datetime.now(UTC),
                error=str(e),
            )
            db.add(detail)
            send_record.status = -1
            results.append(
                {
                    "dispatch_bid": d.message_dispatch_bid,
                    "endpoint_bid": getattr(d, "endpoint_bid", None),
                    "error": str(e),
                }
            )

    return results
