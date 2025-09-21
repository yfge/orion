---
id: 2025-09-21T05-45-00Z-alembic-revision-normalize
date: 2025-09-21T05:45:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, alembic]
related_paths:
  - backend/alembic/versions/0005_api_keys.py
summary: "Normalize migration revision id to numeric '0005' to match existing 0001–0004"
---

Change

- 将 `0005_api_keys.py` 的 `Revision ID` 与 `revision` 变量统一改为 `"0005"`，`down_revision` 保持 `"0004"`，与既有 0001–0004 的命名规范一致。

Outcome

- 迁移编号自洽：0001 → 0002 → 0003 → 0004 → 0005。
