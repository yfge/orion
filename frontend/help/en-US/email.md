% Email adapters (Mailgun/SendGrid/SMTP)

## Adapters

- Mailgun (HTTP): `adapter_key=http.mailgun`
  - Config: `url=https://api.mailgun.net/v3/<domain>/messages`, `api_key`
  - Optional: default `from`, default `to`
- SendGrid (HTTP): `adapter_key=http.sendgrid`
  - Config: `url=https://api.sendgrid.com/v3/mail/send`, `api_key`
  - Optional: default `from`, default `to`
- SMTP (direct): `transport=smtp, adapter_key=smtp.generic`
  - Config: `host`, optional `port` (25/465/587), `use_tls`/`use_ssl`, `username`/`password`, default `from`/`to`

## Send test and mapping

- “Send Test” auto‑builds subject/body (default subject “Orion Test”)
- Dispatch mapping supports: `from`, `to`, `subject`, `text`, `html`; prefer schema forms (RJSF)

SendGrid body (partial) example:

```json
{
  "from": { "email": "noreply@example.com" },
  "personalizations": [{ "to": [{ "email": "alice@example.com" }] }],
  "subject": "Hello",
  "content": [{ "type": "text/plain", "value": "Hi" }]
}
```

## Troubleshooting

- 401/403: invalid API key or permission; verify `api_key`, domain and IP whitelist
- 400 Bad Request: sender/recipient/domain unverified or invalid
- SMTP issues:
  - Ports and TLS/SSL: 465 = SSL, 587 = STARTTLS, 25 = plain (often blocked by clouds)
  - Auth failures: check `username/password` and whether app passwords/less secure apps are required
  - HTML: ensure valid HTML markup to avoid rejection
