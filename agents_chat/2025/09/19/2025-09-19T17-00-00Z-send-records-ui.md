---
id: 2025-09-19T17-00-00Z-orion-send-records
date: 2025-09-19T17:00:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, frontend, api, ui]
related_paths:
  - backend/app/api/v1/send_records.py
  - backend/app/repository/send_records.py
  - backend/app/schemas/send_records.py
  - frontend/app/records/
  - frontend/lib/api.ts
summary: "Add Send Records APIs and Console UI to list and inspect notification send history."
---

What
- Implemented backend list/detail APIs for send records and send details; joined names for readability.
- Added frontend Records pages: table with filters, and detail view with attempts.
- Minor fix: made datetime usage timezone-aware in notify service.

Why
- Operators need visibility into notification dispatch history for troubleshooting and auditing.

Outcome
- New routes: GET /api/v1/send-records, GET /api/v1/send-records/{bid}, GET /api/v1/send-records/{bid}/details.
- Sidebar link “发送记录” now navigates to a functional list and detail UI.
- All existing tests still pass.

TODOs
- Add retry action from record/detail page.
- Advanced filters (time range, business system).
- Pagination for details, export.
