% Third-party integration

Use Notify API to decouple your business systems from channels.

Recommendations:

- Prefer Authorization: Bearer <token>
- Use async /notify/async for high volume and poll records by request_id
- Retries with backoff for 5xx; fix params/auth for 4xx

Security:

- Keep API keys on server-side only
- HTTPS only; restrict IPs; consider signatures/timestamps
- Rotate keys and revoke unused ones
