% API Keys: management and usage

## Basics

- Entry: sidebar “API Keys”
- Create: input name/description; a plaintext token is shown once
- Usage: prefer `Authorization: Bearer <token>`; `X-API-Key` and `Basic api:<token>` are compatible
- Enable/disable: toggle status; deleted keys cannot be used
- Isolation: each user sees and manages only keys they created (owner_user_bid)

## API examples

Create (requires user token from console login):

```bash
curl -X POST \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/api-keys \
  -d '{"name": "notify-public", "description": "public calls"}'
```

List: `GET /api/v1/api-keys?limit=50&offset=0&q=`

Disable:

```bash
curl -X PATCH \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:8080/api/v1/api-keys/$BID \
  -d '{"status": 0}'
```

## Relation to Notify

- Public Notify auth: first checks env `ORION_PUBLIC_API_KEY`, otherwise validates against enabled DB API Keys (sha256)
- Manage keys in the “API Keys” page for auditing and rotation
