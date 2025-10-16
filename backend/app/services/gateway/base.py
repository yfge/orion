from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session


@dataclass(slots=True)
class GatewaySendResult:
    success: bool
    message_bid: str
    vendor_msg_id: str | None = None
    state: str | None = None
    error: str | None = None
    retry_scheduled: bool = False


class ChannelGateway(ABC):
    key: str

    @abstractmethod
    def send(self, db: Session, payload: dict[str, Any]) -> GatewaySendResult:
        """Send a message for the channel."""

    @abstractmethod
    def retry(self, db: Session, message_bid: str) -> GatewaySendResult:
        """Retry a previously failed message."""

    def recall(self, db: Session, message_bid: str) -> GatewaySendResult:  # pragma: no cover - optional
        raise NotImplementedError
