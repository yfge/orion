---
id: 2025-09-21T07-05-00Z-fix-notify-datetime-import
date: 2025-09-21T07:05:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, bugfix]
related_paths:
  - backend/app/api/v1/notify.py
summary: "Fix NameError in notify public records (import datetime)"
---

Issue

- 后端报错 NameError: name 'datetime' is not defined，发生在 `/api/v1/notify/send-records` 查询参数使用 datetime 类型的注解处。

Fix

- 在 `backend/app/api/v1/notify.py` 顶部补充 `from datetime import datetime`。

Outcome

- 公开发送记录查询接口恢复正常。
