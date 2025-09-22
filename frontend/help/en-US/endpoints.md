% Endpoints & Dispatches

## Concepts

- Endpoints: configure third‑party channels (HTTP/MQ/SMTP), described by `transport + adapter_key + config`
- Message Definitions: message structure via JSON Schema with `${var}` placeholders
- Dispatches: bind messages to one or more endpoints; optional `mapping` overrides fields
- Send Records: results and details for auditing/troubleshooting

## How to operate

1. Create Endpoint: Console → “Notify APIs” → “New”; choose adapter and fill config; HTTP/SMTP provide schema forms
2. Create Message Definition: Console → “Message Definitions” → “New”; input JSON Schema (supports `${var}`)
3. Create Dispatch mapping:
   - A: in Message Definition detail (choose endpoint, fill `mapping`)
   - B: in Endpoint edit (choose message, fill `mapping`)
   - Email mapping supports form fields: `from/to/subject/text/html`
4. Send Test: in Endpoint edit, “Send Test” to verify channel connectivity

## API snippets

- List endpoints (for a system): `GET /api/v1/systems/{system_bid}/endpoints?limit=50&offset=0&q=`
- Create endpoint: `POST /api/v1/systems/{system_bid}/endpoints`
- Get endpoint: `GET /api/v1/endpoints/{endpoint_bid}`
- Send test: `POST /api/v1/endpoints/{endpoint_bid}/send-test` (body: `{ "text": "hi" }`)
- Create dispatch for a message: `POST /api/v1/message-definitions/{message_bid}/dispatches`

## Tips

- Prefer schema forms (RJSF) to avoid JSON typos
- For errors, first check “Send Records” details (request + third‑party response)
