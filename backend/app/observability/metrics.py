from __future__ import annotations

from typing import Any

try:
    from prometheus_client import Counter, Histogram
    PROMETHEUS_ENABLED = True
except Exception:  # pragma: no cover - fallback if prometheus_client unavailable
    PROMETHEUS_ENABLED = False
    class _NoopMetric:  # type: ignore[too-many-instance-attributes]
        def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
            return None

        def labels(self, *args: Any, **kwargs: Any) -> "_NoopMetric":  # noqa: D401
            return self

        def inc(self, *_: Any, **__: Any) -> None:  # noqa: D401
            return None

        def observe(self, *_: Any, **__: Any) -> None:  # noqa: D401
            return None

    Counter = Histogram = _NoopMetric  # type: ignore[misc]
    PROMETHEUS_ENABLED = False


_WECHAT_SEND_ATTEMPTS = Counter(
    "orion_wechat_send_attempts_total",
    "Total number of WeChat Official Account send attempts",
    labelnames=("result", "app_id", "errcode"),
)

_WECHAT_SEND_LATENCY = Histogram(
    "orion_wechat_send_latency_seconds",
    "WeChat Official Account send latency",
    labelnames=("app_id",),
    buckets=(0.1, 0.2, 0.5, 1, 2, 3, 5, 8),
)

_WECHAT_CALLBACK_EVENTS = Counter(
    "orion_wechat_callback_events_total",
    "Count of WeChat callback events by type/status",
    labelnames=("event_type", "status"),
)


def record_wechat_send(result: str, app_id: str | None, duration_seconds: float, *, errcode: int | None = None) -> None:
    app_id = app_id or "unknown"
    err_label = str(errcode) if errcode is not None else "0"
    _WECHAT_SEND_ATTEMPTS.labels(result=result, app_id=app_id, errcode=err_label).inc()
    _WECHAT_SEND_LATENCY.labels(app_id=app_id).observe(duration_seconds)


def record_wechat_callback(event_type: str, status: str) -> None:
    _WECHAT_CALLBACK_EVENTS.labels(event_type=event_type, status=status).inc()


__all__ = [
    "record_wechat_send",
    "record_wechat_callback",
    "PROMETHEUS_ENABLED",
]
