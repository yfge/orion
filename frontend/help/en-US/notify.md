% Notify API and auth

Endpoint: `POST /api/v1/notify`

Auth (prefer Bearer):

- Authorization: Bearer <token>
- X-API-Key: <token>
- Authorization: Basic api:<token>

Example:

```bash
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/notify \
  -d '{"message_name":"simple-text","data":{"text":"hello"}}'
```

See “Send Records” for result details and troubleshooting.
