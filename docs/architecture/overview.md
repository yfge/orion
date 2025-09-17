# Orion Architecture Overview

Vision
- Orion is a centralized notification gateway: accept requests from business systems and dispatch to external channels (Feishu, WeCom, WeChat, Email, SMS...).
- Goals: decoupling, reliability, observability, operability, and modular integrations via DI.

Key Components
- API Layer (FastAPI): request validation, auth (future), routing to use cases.
- Domain & Services: orchestration, template rendering, routing policies, idempotency.
- Adapters: per-channel senders hidden behind stable interfaces; vendor-agnostic core.
- Persistence: relational DB for notifications, events, templates; Redis/queues optional.
- Jobs: retry/backoff, scheduled scans for stuck/failed messages (Celery/RQ/APScheduler).

Backend Layers
- `api`: thin controllers, no vendor logic.
- `services`: business flows (create -> schedule -> send -> confirm -> record).
- `adapters`: Feishu/WeCom/WeChat/Email/SMS senders, replaceable via DI.
- `repository`: SQLAlchemy implementations behind ports.

State & Reliability
- States: pending -> sending -> success | failed -> retrying -> abandoned.
- Idempotency keys per request; exponential backoff; rate limiting; circuit breaker.
- Full audit trail: persist events and transitions.

Extensibility
- New channel: implement adapter interface + register via DI; no API changes required.
- New strategy: add routing/templating strategies in services; keep interfaces stable.

Observability (future)
- Structured logging, metrics (Prometheus), tracing (OpenTelemetry).

AI Collaboration
- All session logs saved under `agents_chat/` per `AGENTS.md`.
- Docs-first workflow: architecture -> module docs -> implementation.

Initial Scaffolding (done)
- FastAPI app with `/healthz` and `/api/v1/ping`.
- Alembic configured; DB URL sourced from settings.
- Backend packaging via `backend/pyproject.toml`; repo uses pre-commit for ruff/black/isort.
