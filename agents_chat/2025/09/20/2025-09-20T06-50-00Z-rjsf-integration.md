---
id: 2025-09-20T06-50-00Z-orion-rjsf-integration
date: 2025-09-20T06:50:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, json-schema, rjsf, ui]
related_paths:
  - frontend/components/jsonschema/RjsfForm.tsx
  - frontend/app/messages/new/page.tsx
  - frontend/app/messages/[bid]/page.tsx
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
  - frontend/package.json
  - frontend/pnpm-lock.yaml
summary: "Integrate @rjsf/core + ajv8 with ShadCN-styled widgets/templates and replace schema preview/config forms in messages and endpoints."
---

What
- Added `RjsfForm` wrapper using `@rjsf/core` + `@rjsf/validator-ajv8`, with ShadCN-styled widgets (Text/Number/Select/Checkbox) and templates (Object/Array).
- Replaced message definition preview forms to use RJSF.
- Endpoint edit page now renders adapter-based config via RJSF while retaining a JSON textarea (bidirectional sync).
- Updated `package.json` deps, committed pnpm lockfile changes.

Why
- Need robust JSON Schema rendering and built-in Ajv validation for complex forms while keeping UI consistent with ShadCN.

Outcome
- Operators can configure endpoints and preview message schemas with richer widgets and proper validation.
- Code paths prepared for uiSchema and additional widgets (date/datetime/url/email, x-enumNames, password, kv editors).

Notes
- Install deps in `frontend/` (may require `--legacy-peer-deps`).
- Optional: use dynamic import with `ssr: false` if SSR causes issues with RJSF.

Next
- Add uiSchema support, advanced widgets, and integrate backend `/schema/validate` errors to field-level messages.
