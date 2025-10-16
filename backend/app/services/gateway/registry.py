from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

from .base import ChannelGateway


@dataclass(frozen=True)
class ChannelRegistration:
    factory: Callable[[], ChannelGateway]
    capabilities: dict[str, bool]


_registry: Dict[str, ChannelRegistration] = {}


def register_channel(key: str, *, factory: Callable[[], ChannelGateway], capabilities: dict[str, bool]) -> None:
    _registry[key] = ChannelRegistration(factory=factory, capabilities=capabilities)


def get_channel(key: str) -> ChannelGateway:
    if key not in _registry:
        raise KeyError(f"channel '{key}' is not registered")
    registration = _registry[key]
    return registration.factory()


def list_capabilities() -> dict[str, dict[str, bool]]:
    return {key: reg.capabilities for key, reg in _registry.items()}
