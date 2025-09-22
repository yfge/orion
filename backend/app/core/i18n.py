from __future__ import annotations

import gettext
import os
from collections.abc import Iterable
from contextvars import ContextVar

from starlette.requests import Request

SUPPORTED_LOCALES: list[str] = ["zh-CN", "en-US"]
DEFAULT_LOCALE: str = "zh-CN"

_locale_ctx: ContextVar[str] = ContextVar("locale", default=DEFAULT_LOCALE)


def get_locale() -> str:
    return _locale_ctx.get()


def set_locale(locale: str) -> None:
    _locale_ctx.set(locale)


def _parse_accept_language(header: str) -> list[str]:
    # Very small parser: returns locales ordered by q weight
    parts: list[tuple[str, float]] = []
    for item in header.split(","):
        token = item.strip()
        if not token:
            continue
        if ";q=" in token:
            lang, q = token.split(";q=", 1)
            try:
                weight = float(q)
            except ValueError:
                weight = 1.0
        else:
            lang, weight = token, 1.0
        parts.append((lang.strip(), weight))
    parts.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in parts]


def _negotiate(candidates: Iterable[str]) -> str | None:
    # Match exact first, then language-only fallbacks (e.g., en -> en-US default)
    for cand in candidates:
        if cand in SUPPORTED_LOCALES:
            return cand
        # try language-only match
        lang = cand.split("-", 1)[0]
        for sup in SUPPORTED_LOCALES:
            if sup.split("-", 1)[0] == lang:
                return sup
    return None


def detect_locale(request: Request) -> str:
    # Priority: ?lang -> Cookie LANG -> Accept-Language -> default
    qp = request.query_params.get("lang")
    if qp:
        cand = _negotiate([qp])
        if cand:
            return cand

    cookie = request.cookies.get("LANG")
    if cookie:
        cand = _negotiate([cookie])
        if cand:
            return cand

    al = request.headers.get("Accept-Language")
    if al:
        cand = _negotiate(_parse_accept_language(al))
        if cand:
            return cand

    return DEFAULT_LOCALE


def _translations_for(locale: str) -> gettext.NullTranslations | gettext.GNUTranslations:
    localedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "locale")
    # Normalize locale like zh-CN -> zh_CN for filesystem if needed
    normalized = locale.replace("-", "_")
    try:
        return gettext.translation(
            "orion", localedir=localedir, languages=[normalized], fallback=True
        )
    except Exception:
        return gettext.NullTranslations()


def gettext_(message_id: str) -> str:
    t = _translations_for(get_locale())
    return t.gettext(message_id)


class I18nMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive=receive)
            loc = detect_locale(request)
            set_locale(loc)
            scope.setdefault("state", {})
            scope["state"]["locale"] = loc

            async def send_wrapper(message):
                if message.get("type") == "http.response.start":
                    headers = list(message.get("headers", []))
                    headers.append((b"content-language", loc.encode("ascii")))
                    message["headers"] = headers
                await send(message)

            await self.app(scope, receive, send_wrapper)
            return
        await self.app(scope, receive, send)
