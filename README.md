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

- Auth: either header `X-API-Key` or HTTP Basic with `api:<key>`
  - Set `ORION_PUBLIC_API_KEY` in `.env` or compose env
  - Basic example: `Authorization: Basic` + base64(`api:<key>`)
- Endpoint: `POST /api/v1/notify`
- Body options:
  - By name: `{ "message_name": "simple-text", "data": { "text": "hi" } }`
  - By bid: `{ "message_definition_bid": "...", "data": { ... } }`
- Response: `{ "results": [ { "dispatch_bid", "endpoint_bid", "status_code", "body" } ] }`

- Generate a key (preview): `POST /api/v1/notify/keys/preview` returns a random key suggestion; set it to `ORION_PUBLIC_API_KEY` on the backend.

### Feishu quick test

1. Create endpoint: transport=http, adapter_key=http.feishu_bot, endpoint_url=<feishu_webhook>
2. Create message definition: schema `{ "msg_type": "text", "content": { "text": "${text}" } }`
3. Add dispatch (message -> endpoint)
4. Call `/api/v1/notify` with `{ "message_name": "...", "data": { "text": "hello" } }`
5. Or use endpoint edit page “Send test” UI

### Email channels (Mailgun, SendGrid, SMTP)

- Mailgun
  - Create endpoint: transport=http, adapter_key=http.mailgun
  - Config: `url=https://api.mailgun.net/v3/<domain>/messages`, `api_key=<key>`, optional `from`/`to`
  - Send test in endpoint page; subject auto="Orion Test", body uses input text
- SendGrid
  - Create endpoint: transport=http, adapter_key=http.sendgrid
  - Config: `url=https://api.sendgrid.com/v3/mail/send`, `api_key=<key>`, optional `from`/`to`
  - Send test constructs SendGrid JSON with from/to/subject/content
- SMTP
  - Create endpoint: transport=smtp, adapter_key=smtp.generic
  - Config: `host`, optional `port`, `use_tls`/`use_ssl`, optional `username`/`password`, default `from`/`to`
  - Send test sends a simple email with subject "Orion Test" and text from input; mapping also supports `subject`, `text`, `html`, `from`, `to`

## Frontend Setup

- `cd frontend && npm i` (or pnpm/yarn)
- Run: `npm run dev` and open http://localhost:3000
- Note: the browser uses same-origin `/api` calls; for local dev without Docker/Nginx, set up a dev proxy from `/api` → `http://127.0.0.1:8000` (e.g., Next.js rewrites) or prefer Docker Compose below which already proxies via Nginx.
- Navigate to Systems, Endpoints, Messages; create mappings in Messages or Endpoints pages

## Docker (one‑command bring‑up)

- Prereqs: Docker Desktop with Compose.
- Start (first time build recommended):
  - Build images: `docker compose build`
  - Run in background: `docker compose up -d`
  - Check status: `docker compose ps`
  - Tail logs: `docker compose logs -f --tail=200 backend` (or `frontend`/`mysql`/`nginx`)

### Endpoints

- Console (Nginx entry): http://localhost:8080
- API (proxied by Nginx): http://localhost:8080/api/
- Health: `/healthz` or `/api/v1/ping`

### Services (brief)

- `mysql`: MySQL 8 with `orion/orionpass`, DB `orion`, root `orionroot`; data persists via volume `mysql_data`.
- `backend`: FastAPI service. Runs `alembic upgrade head` then serves via Uvicorn.
  - Key envs: `ORION_DATABASE_URL=mysql+pymysql://orion:orionpass@mysql:3306/orion?charset=utf8mb4`, `ORION_PUBLIC_API_KEY`, etc.
- `frontend`: Next.js console. Browser requests hit same-origin `/api`, which Nginx proxies to backend.
- `nginx`: reverse proxies `/` to frontend and `/api/` to backend.

### Troubleshooting

- MySQL may take a moment on first start. If backend migrates too early, run `docker compose restart backend`.
- Compose warns about `version` field deprecation: it’s safe to ignore; we’ll clean this later.
- To override the frontend API base URL, edit `docker-compose.yml` and set `NEXT_PUBLIC_API_BASE_URL` in both `frontend.build.args` and `frontend.environment`.

## Local Dev: pre-commit hooks

- Install: `pip install pre-commit` and ensure Node.js is available (for commitlint).
- Install hooks: `pre-commit install` and `pre-commit install --hook-type commit-msg`.
- Validate locally: `pre-commit run -a`.
- Commits should not use `--no-verify`; CI enforces Conventional Commits and agents_chat coupling.

## Tests

- Install: `pip install -e backend[test]`
- Run in `backend/`: `pytest`

## Agents & Documentation

- All agent instruction files are symlinked to `AGENTS.md`.
- Collaboration logs under `agents_chat/` (Y/M/D/timestamp-topic.md). Commits that modify code must include an agents_chat entry in the same commit (CI-enforced). Use `skip agents-chat` in commit body to bypass when necessary.
- Architecture doc: `docs/architecture/overview.md`.

## License

TBD.
