---
id: 2025-09-20T08-20-00Z-dashboard-live-data
date: 2025-09-20T08:20:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, backend, api]
related_paths:
  - frontend/app/page.tsx
  - frontend/lib/api.ts
  - backend/app/api/v1/send_records.py
  - backend/app/repository/send_records.py
summary: "Replace dashboard mock data with live stats via API; add date filters for send records."
---

User original prompt and requirements
- 「先完善目前的看板主页面，现在都是mock数据」

Background and goals
- Populate dashboard with real-time data: system count, endpoint count, today success/failure counts, and recent sends.

Changes
- Backend: `send-records` API accepts `start_time` and `end_time` (ISO8601) to filter by `send_time`.
- Frontend: Home page fetches counts and today stats; renders recent sends table.
- API SDK: `listSendRecords` supports `start_time`/`end_time` params.

Outcome and impact
- Dashboard now shows live data instead of mocks.

Next steps (TODO)
- Add channel health (success rate per endpoint, last 24h).
- Add global time range selector for the dashboard.
