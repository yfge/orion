# Quickstart

This page gets you from install to sending a notification in ~10 minutes.

## 1) Start and log in

Option A (recommended): Docker Compose

1. Install Docker Desktop (with Compose)
2. At repo root:

```bash
docker compose build && docker compose up -d
```

3. Open http://localhost:8080, register a user and log in (Users → Register New User)

Option B: Local dev

Backend:

```bash
pip install -e backend
scripts/migrate.sh upgrade head
uvicorn backend.app.main:app --reload
```

Frontend (choose one way to reach backend):

- Dev proxy: set `DEV_API_PROXY=http://127.0.0.1:8000` in `frontend/.env.local`, then `npm i && npm run dev`
- Direct: set `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000` in `frontend/.env.local`, then `npm i && npm run dev`

## 2) Create an API Key

- Go to “API Keys”, create a Key; a plaintext token shows only once
- For public Notify calls, prefer `Authorization: Bearer <token>`

## 3) Build the end‑to‑end path

1. Business System → New
2. Notify API → New (Endpoint). Examples:
   - Feishu bot: `adapter_key=http.feishu_bot`, `endpoint_url=<feishu webhook>`
   - Mailgun: `adapter_key=http.mailgun`, configure URL + api_key
   - SendGrid: `adapter_key=http.sendgrid`, configure URL + api_key
   - SMTP: `transport=smtp, adapter_key=smtp.generic`, configure host/port/TLS/SSL
3. Message Definition → New, example schema:

```json
{
  "msg_type": "text",
  "content": { "text": "${text}" }
}
```

4. Dispatch Mapping: in Message Definition detail or Endpoint edit, bind message → endpoint; email adapters accept `from/to/subject/text/html` overrides
5. Send Test: on endpoint page, input test text to verify connectivity

## 4) Call Notify (from business side)

Bearer example:

```bash
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify \
  -d '{
    "message_name": "simple-text",
    "data": { "text": "hello from orion" }
  }'
```

The response lists each dispatch status and body; see “Notify API usage and authentication” for details.

## 5) View Send Records

Use the “Send Records” page to filter by time/message/endpoint/status; click a record for request/response details.

## FAQ

- 401 Unauthorized: log into console (frontend carries user token); for public Notify, use API Key (Bearer)
- 307 Redirect: routes are normalized; if 307 → 401 appears, refresh frontend or clear cache
- Email failures: check `from/to`, domain verification, SMTP account; consult response in Send Records
