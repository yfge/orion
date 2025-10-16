"""Notification gateway services."""

from .registry import get_channel, list_capabilities
from .wechat_official_account import WechatGatewayService

__all__ = [
    "WechatGatewayService",
    "get_channel",
    "list_capabilities",
]
