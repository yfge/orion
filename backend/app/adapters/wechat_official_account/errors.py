from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from ...core.config import settings


class WechatErrorCategory(str, Enum):
    UNKNOWN = "unknown"
    RETRYABLE = "retryable"
    NON_RETRYABLE = "non_retryable"
    AUTH = "auth"
    RATE_LIMIT = "rate_limit"


_SPECIAL_CATEGORIES: dict[int, WechatErrorCategory] = {
    -1: WechatErrorCategory.RETRYABLE,
    40001: WechatErrorCategory.AUTH,
    40014: WechatErrorCategory.AUTH,
    40164: WechatErrorCategory.AUTH,
    40125: WechatErrorCategory.AUTH,
    43004: WechatErrorCategory.NON_RETRYABLE,
    47003: WechatErrorCategory.NON_RETRYABLE,
    45009: WechatErrorCategory.RATE_LIMIT,
    45011: WechatErrorCategory.RATE_LIMIT,
    45047: WechatErrorCategory.RATE_LIMIT,
    45056: WechatErrorCategory.RATE_LIMIT,
}


@dataclass(eq=False)
class WechatAPIError(RuntimeError):
    errcode: int
    errmsg: str
    category: WechatErrorCategory
    response: dict[str, Any] | None = None

    def __post_init__(self) -> None:  # pragma: no cover - defensive
        super().__init__(f"WechatAPIError(errcode={self.errcode}, category={self.category}, errmsg={self.errmsg})")

    @property
    def retryable(self) -> bool:
        return self.category in {WechatErrorCategory.RETRYABLE, WechatErrorCategory.RATE_LIMIT}


def classify_errcode(errcode: int) -> WechatErrorCategory:
    cfg = settings.WECHAT_OFFICIAL_ACCOUNT
    if errcode in _SPECIAL_CATEGORIES:
        return _SPECIAL_CATEGORIES[errcode]
    if errcode in cfg.retryable_error_codes:
        return WechatErrorCategory.RETRYABLE
    if errcode in cfg.non_retryable_error_codes:
        return WechatErrorCategory.NON_RETRYABLE
    if errcode == 0:
        return WechatErrorCategory.UNKNOWN
    return WechatErrorCategory.UNKNOWN


def raise_for_errcode(errcode: int, errmsg: str, *, response: dict[str, Any] | None = None) -> None:
    if errcode == 0:
        return
    category = classify_errcode(errcode)
    raise WechatAPIError(errcode=errcode, errmsg=errmsg, category=category, response=response)
