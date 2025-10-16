"""WeChat Official Account adapter package."""

from .client import SendResult, WechatOfficialAccountClient
from .errors import WechatAPIError, WechatErrorCategory
from .token_provider import WechatAccessTokenProvider

__all__ = [
    "SendResult",
    "WechatOfficialAccountClient",
    "WechatAPIError",
    "WechatErrorCategory",
    "WechatAccessTokenProvider",
]
