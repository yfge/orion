from __future__ import annotations

from typing import Any
from datetime import datetime

from sqlalchemy.orm import Session

from ..repository import message_definitions as msg_repo
from ..repository import dispatches as disp_repo
from ..repository import endpoints as ep_repo
from .templating import render_value
from .sender.http_sender import HttpSender


def notify_by_name(db: Session, *, message_name: str, data: dict[str, Any]) -> list[dict[str, Any]]:
    msg = msg_repo.get_by_name(db, message_name)
    if not msg:
        raise ValueError("message not found")
    return _notify(db, message_bid=msg.message_definition_bid, schema=msg.schema or {}, data=data)


def notify_by_bid(db: Session, *, message_bid: str, data: dict[str, Any]) -> list[dict[str, Any]]:
    msg = msg_repo.get_by_bid(db, message_bid)
    if not msg:
        raise ValueError("message not found")
    return _notify(db, message_bid=message_bid, schema=msg.schema or {}, data=data)


def _notify(db: Session, *, message_bid: str, schema: dict[str, Any], data: dict[str, Any]) -> list[dict[str, Any]]:
    # Render base payload from message schema
    base_payload = render_value(schema, data)
    # Fetch dispatches
    dispatches, _ = disp_repo.list_by_message(db, message_bid=message_bid, limit=1000, offset=0)
    results: list[dict[str, Any]] = []
    http_sender = HttpSender()
    for d in dispatches:
        if not d.enabled:
            continue
        ep = ep_repo.get_by_bid(db, getattr(d, "endpoint_bid", None) or "")
        if not ep:
            continue
        endpoint_dict = {
            "adapter_key": ep.adapter_key or "http.generic",
            "endpoint_url": ep.endpoint_url,
            "config": (ep.config or {}) | {"url": ep.endpoint_url},
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
            res = http_sender.send(endpoint=endpoint_dict, payload=payload)
            results.append({
                "dispatch_bid": d.message_dispatch_bid,
                "endpoint_bid": getattr(d, "endpoint_bid", None),
                "status_code": int(res.get("status_code", 0)),
                "body": res.get("body"),
            })
        except Exception as e:  # pragma: no cover
            results.append({
                "dispatch_bid": d.message_dispatch_bid,
                "endpoint_bid": getattr(d, "endpoint_bid", None),
                "error": str(e),
            })

    return results

