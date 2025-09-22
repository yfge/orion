% Notify API usage and authentication

## Interface and auth

- Endpoint: `POST /api/v1/notify`
- Auth (choose one; prefer Bearer):
  - `Authorization: Bearer <token>` (recommended)
  - `X-API-Key: <token>` (compatible)
  - `Authorization: Basic <base64("api:<token>")>` (Mailgun‑style)

Create keys in Console “API Keys” (plaintext shown once), or generate random strings via `/api/v1/notify/keys/preview` and configure on backend.

## Request example

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

The response contains status/body for each dispatch. See Send Records to interpret results.

## Async notify

- Endpoint: `POST /api/v1/notify/async` (202)
- Same body as sync; optional `request_id` for later lookup
- Response: `{"accepted":true, "request_id":"...", "estimated_dispatches": N}`

## Send Records API

- List: `GET /api/v1/notify/send-records?...`
- One: `GET /api/v1/notify/send-records/{bid}`
- Details: `GET /api/v1/notify/send-records/{bid}/details?...`

Lookup by `request_id`:

```bash
curl -H "Authorization: Bearer $API_KEY" \
  "http://localhost:8080/api/v1/notify/send-records?request_id=$REQ&limit=20&offset=0"
```

## Error codes

- 401 Unauthorized: invalid/missing API Key
- 404 Not Found: resource not found (e.g. message name)
- 5xx: system or vendor error (retry/alert)
