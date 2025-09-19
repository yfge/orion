from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class MessageSender(ABC):
    @abstractmethod
    def send(self, *, endpoint: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        """Send a message to the given endpoint with a normalized payload."""

