# Third‑party integration guide

This guide targets vendors/external systems. It explains Orion concepts, onboarding flow and examples.

## 1. Basics

- Base URL (local example): `http://localhost:8080`
- Production: use your domain over HTTPS
- Public APIs share the prefix: `/api/v1` (e.g. `/api/v1/notify`)

## 2. Authentication (API Key)

- Platform admin creates API Keys in Console “API Keys” and shares with you
- Prefer `Authorization: Bearer <token>`
- Compatible: `X-API-Key: <token>` or `Authorization: Basic <base64("api:<token>")>`

Security note: never expose keys in frontend or shared media; store them server‑side or in a secret manager.

---

## 3. Core concepts

- Business System: your domain/app scope (e.g. “Orders”, “Settlement”)
- Endpoint: channel config containing:
  - transport: http/smtp/etc
  - adapter_key: http.generic, http.mailgun, http.sendgrid, smtp.generic, etc
  - config: URL/auth/timeout/etc
- Message Definition: JSON Schema + `${var}` placeholders (e.g. Feishu text)
- Dispatch: bind Message Definition to one or more Endpoints; optional `mapping` overrides fields
- Send Record/Detail: overall record and per‑attempt/per‑channel details

---

## 4. Integration flow

1. Admin creates API Key
2. Platform config:
   - New Business System (optional)
   - New Endpoint (HTTP/SMTP…)
   - New Message Definition (JSON Schema with `${var}`)
   - Bind Dispatch (message → endpoint), set mapping if needed
3. You call public Notify (sync or async) with data; Orion dispatches to channels
4. Query Send Records via API or Console (filter by request_id)

## 5. Synchronous sending

- `POST /api/v1/notify`
- Body (choose one):
  - `{ "message_name": "<name>", "data": { ... } }`
  - `{ "message_definition_bid": "<bid>", "data": { ... } }`
- Success: `{"results": [{"dispatch_bid","endpoint_bid","status_code","body"}]}`

Example:

```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify \
  -d '{
    "message_name": "simple-text",
    "data": { "text": "hello from vendor" }
  }'
```

Use when volume is small and you need immediate channel results.

## 6. Async sending (high volume)

- `POST /api/v1/notify/async` (returns 202)
- Same body as sync; optional `request_id` for later lookup (stored as remark)
- Success: `{"accepted":true, "request_id":"...", "estimated_dispatches": 2}`

Example:

```bash
REQ=$(uuidgen | tr 'A-Z' 'a-z' | tr -d '-')
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify/async \
  -d "{\n  \"message_name\": \"simple-text\",\n  \"data\": { \"text\": \"async hello\" },\n  \"request_id\": \"$REQ\"\n}"
```

Note: current `request_id` is for lookup only (no idempotency). Ensure uniqueness on caller side or adopt an idempotency strategy.

## 7. Query send records (API Key)

- List: `GET /api/v1/notify/send-records?...`
- One: `GET /api/v1/notify/send-records/{bid}`
- Details: `GET /api/v1/notify/send-records/{bid}/details?...`

Lookup by request_id:

```bash
curl -H "Authorization: Bearer $API_KEY" \
  "http://localhost:8080/api/v1/notify/send-records?request_id=$REQ&limit=20&offset=0"
```

Record fields: `send_record_bid`, `message_definition_bid`, `notification_api_bid`, `message_name`, `endpoint_name`, `business_system_name`, `send_time`, `result`, `remark` (=request_id), `status`, `created_at`

Detail fields: `request_payload`, `response_payload`, `error`, `attempt_no`, `sent_at`, etc.

## 8. Error codes

- 401 Unauthorized: invalid/missing API Key
- 404 Not Found: resource not found (e.g. message name)
- 5xx: server or channel errors (retry/alert)

## 9. Best practices

- Auth: prefer Bearer; rotate keys regularly
- Async: use `/notify/async` under heavy load, and query by `request_id`
- Retry: backoff for 5xx; fix parameters/auth for 4xx
- Observability: use Send Records + Console to build alerts/dashboards

## 10. Security

---

## Appendix: E2E examples

### A: Generic HTTP JSON API

Endpoint (adapter_key = http.generic):

```json
{
  "method": "POST",
  "url": "https://api.vendor.example.com/v1/notify",
  "timeout": 10,
  "headers": { "Authorization": "Bearer VENDOR_API_TOKEN" }
}
```

Message Definition:

```json
{
  "title": "Generic JSON",
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "content": { "type": "string" },
    "user_id": { "type": "string" }
  },
  "required": ["title", "content"]
}
```

Dispatch mapping:

```json
{ "title": "${text}", "content": "Notify: ${text}", "user_id": "${uid}" }
```

Call: see sections 5/6.

### B: Mailgun (HTTP form)

Endpoint (adapter_key = http.mailgun):

```json
{
  "url": "https://api.mailgun.net/v3/YOUR_DOMAIN/messages",
  "api_key": "MAILGUN_KEY",
  "body_format": "form",
  "from": "noreply@your.com",
  "to": "user@dest.com"
}
```

Mapping:

```json
{ "subject": "${subject}", "text": "${text}", "html": "<b>${text}</b>" }
```

### C: SMTP (direct)

Endpoint (transport=smtp, adapter_key=smtp.generic):

```json
{
  "host": "smtp.your.com",
  "port": 587,
  "use_tls": true,
  "username": "mailer",
  "password": "secret",
  "from": "noreply@your.com",
  "to": "user@dest.com"
}
```

Mapping:

```json
{ "subject": "${subject}", "text": "${text}", "html": "<p>${text}</p>" }
```

### D: WeChat Official Account (Template Message)

1. Endpoint config (adapter_key = channel.wechat_official_account)

Create an endpoint in “Notify API → New”:

- `transport=channel`
- `adapter_key=channel.wechat_official_account`

Config example:

```json
{
  "app_id": "wx1234567890",
  "app_secret": "your-app-secret",
  "language": "zh_CN",
  "timeout": 5
}
```

- `app_id/app_secret`: Service Account credentials from WeChat platform, used to fetch access_token
- `language`: template language, usually `zh_CN`

2. Message Definition (template)

In “Message Definitions”, create a template-style payload:

```json
{
  "template_id": "TM00000001",
  "to_user": "${openid}",
  "data": {
    "first": { "value": "Course booking result" },
    "time": { "value": "${time}" },
    "shifu_title": { "value": "${shifu_title}" },
    "student_name": { "value": "${student_name}" },
    "teacher_name": { "value": "${teacher_name}" }
  },
  "link": {
    "type": "url",
    "url": "${link_url}"
  }
}
```

Conventions:

- `to_user` may use `${openid}`; business passes `data.openid` when calling `/notify`
- `data.*.value` supports `${var}` placeholders
- `link.url` may reference variables such as `${order_no}`

3. Dispatch mapping (optional)

For simple cases, you usually do not need extra mapping; the message template itself handles `${var}`. If you want to centralize link construction in mapping:

```json
{
  "link": {
    "type": "url",
    "url": "https://example.com/order/${order_no}"
  }
}
```

4. Notify call example

```bash
curl -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify/ \
  -d '{
    "message_name": "course-booking-result",
    "data": {
      "link_url": "https://example.com/order/ORD20251202001",
      "time": "2025-11-29 10:00:00~12:00:00",
      "shifu_title": "TIT Garden",
      "student_name": "Coco",
      "teacher_name": "Melody",
      "openid": "oABCD1234567890"
    }
  }'
```

Orion will:

- Render the template payload from message definition using `data`
- Merge endpoint config (app_id/app_secret) and mapping
- Call WeChat template API via the channel gateway and record send_records/send_details

Security notes:

- Keep API keys server‑side; call via backend only
- Enforce HTTPS; restrict IPs; consider signatures/timestamps
- Disable unused keys promptly
