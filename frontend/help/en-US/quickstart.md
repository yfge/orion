% Quickstart

This page helps you get from install to sending a notification in ~10 minutes.

## 1. Run and Login

Docker Compose (recommended):

```bash
docker compose build && docker compose up -d
```

Open http://localhost:8080 and register/login.

## 2. Create an API Key

Create a key in “API Keys” and use it with Authorization: Bearer <token>.

## 3. Create end-to-end pipeline

1. Create Business System
2. Create Notify API (endpoint): Feishu/Mailgun/SendGrid/SMTP
3. Create Message Definition (schema)
4. Add Dispatch Mapping (message → endpoint)
5. Send Test in endpoint page

## 4. Call Notify

```bash
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify \
  -d '{"message_name":"simple-text","data":{"text":"hello"}}'
```

## 5. View Send Records

Filter by time/message/endpoint/status; inspect details for troubleshooting.
