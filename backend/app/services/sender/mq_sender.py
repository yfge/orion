from __future__ import annotations

from typing import Any

from .base import MessageSender


class MQSender(MessageSender):
    def send(self, *, endpoint: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        cfg = endpoint.get("config") or {}
        broker = cfg.get("broker_type")  # kafka/rabbit
        # Placeholder; actual implementation would use aiokafka/pika/etc.
        return {"status": "queued", "broker": broker}

