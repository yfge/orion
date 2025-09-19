# Orion Notification Gateway

[简体中文文档](README.zh-CN.md)

Orion is a unified notification gateway: it accepts notify requests from business systems, orchestrates routing, and delivers messages to multiple external channels (Feishu/Lark, WeCom, WeChat, email, SMS, MQ, etc.).

This repo demonstrates an ai-coding & vibe-coding workflow — documentation-first, agent-friendly, fully auditable via agents_chat.

## Status & Key Features
- Message Definitions: define message schema (JSON with ${var} templating).
- Endpoints: HTTP/MQ endpoints with adapter_key and config (e.g., http.feishu_bot).
- Dispatch Mapping: map a message to many endpoints (BID-first relations).
- Notify API: POST /api/v1/notify with message_name or message_definition_bid + data.
- Feishu E2E: endpoint edit page offers “send test” to a Feishu bot webhook.
- Auth profiles: CRUD ready; attach to endpoints (future auth providers wiring).
- Frontend console: manage systems, endpoints, messages, and mappings.

## Tech Stack
- Backend: Python 3.11, FastAPI, SQLAlchemy, Alembic, PyJWT/Passlib (optional), httpx
- Frontend: Next.js 14 (app dir) + Tailwind
- DB: SQLite (dev) / MySQL (supported); Redis/MQ optional later

## Structure
- `backend/`: FastAPI app, APIs, services, repositories, models, tests
- `frontend/`: Next.js console (systems, endpoints, messages, dispatches)
- `agents_chat/`: AI collaboration logs (see below)

## Backend Setup
- Conda recommended: `conda activate py311`
- Install: from repo root `pip install -e backend` (or `cd backend && pip install -e .`)
- Run server: `uvicorn backend.app.main:app --reload`
- DB (MySQL example): set in `.env`
  - `ORION_DATABASE_URL=mysql+pymysql://root:Pa88word@127.0.0.1:13306/orion?charset=utf8mb4`
  - Migrate: `scripts/migrate.sh upgrade head`
- CORS: configure `ORION_CORS_ORIGINS=*` or JSON array; defaults allow localhost:3000/3001
- API Docs: Swagger `/docs`, ReDoc `/redoc`

### Notify API (Public)
- Auth: header `X-API-Key` (set `ORION_PUBLIC_API_KEY` in `.env`)
- Endpoint: `POST /api/v1/notify`
- Body options:
  - By name: `{ "message_name": "simple-text", "data": { "text": "hi" } }`
  - By bid: `{ "message_definition_bid": "...", "data": { ... } }`
- Response: `{ "results": [ { "dispatch_bid", "endpoint_bid", "status_code", "body" } ] }`

### Feishu quick test
1) Create endpoint: transport=http, adapter_key=http.feishu_bot, endpoint_url=<feishu_webhook>
2) Create message definition: schema `{ "msg_type": "text", "content": { "text": "${text}" } }`
3) Add dispatch (message -> endpoint)
4) Call `/api/v1/notify` with `{ "message_name": "...", "data": { "text": "hello" } }`
5) Or use endpoint edit page “Send test” UI

## Frontend Setup
- `cd frontend && npm i` (or pnpm/yarn)
- Set base URL: `frontend/.env.local` → `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`
- Run: `npm run dev` and open http://localhost:3000
- Navigate to Systems, Endpoints, Messages; create mappings in Messages or Endpoints pages

## Tests
- Install: `pip install -e backend[test]`
- Run in `backend/`: `pytest`

## Agents & Documentation
- All agent instruction files are symlinked to `AGENTS.md`.
- Collaboration logs under `agents_chat/` (Y/M/D/timestamp-topic.md).
- Architecture doc: `docs/architecture/overview.md`.

## License
TBD.
