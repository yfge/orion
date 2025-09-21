---
id: 2025-09-21T05-25-00Z-alembic-fix-down-revision
date: 2025-09-21T05:25:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, alembic, migration]
related_paths:
  - backend/alembic/versions/0002_add_api_keys.py
  - backend/alembic/versions/0001_initial_schema.py
summary: "Fix 0002 migration down_revision to match 0001 revision id"
---

Issue

- 运行 Alembic 升级时，报找不到 `down_revision '0001_initial_schema'`。原因：`0001_initial_schema.py` 文件的 `revision` 其实是 `"0001"`，而 `0002_add_api_keys.py` 写成了 `down_revision = '0001_initial_schema'`。

Change

- 将 `backend/alembic/versions/0002_add_api_keys.py` 中的 `down_revision` 修正为 `"0001"`。

Outcome

- 迁移链路恢复正常：`0001` → `0002_add_api_keys`。

Notes

- 0001 的表结构与 ORM 有一定差异（历史原因），但本次新增表 `api_keys` 与现有模型兼容；Compose 环境按顺序迁移不会受影响。
