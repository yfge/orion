---
id: 2025-09-19T06-57-09Z-fix-duplicate-status
date: 2025-09-19T06:57:09Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [db, migration, fix]
related_paths:
  - backend/app/db/models.py
  - backend/alembic/versions/0001_initial_schema.py
summary: "修复迁移失败（DuplicateColumnError: status）。原因是通用字段已包含 status，send_records/send_details 又各自定义了一次。"
---

问题
- 迁移执行到 `send_records` 报错：DuplicateColumnError: column 'status' already present。
- 原因：
  - 通用列 `_common_columns()` 已包含 `status`。
  - `send_records` 与 `send_details` 又显式定义了 `status`，导致重复。

修复
- 移除 `send_records` 与 `send_details` 中的显式 `status` 列定义（迁移与 ORM 模型均已修正）。

结果
- 重新执行 `scripts/migrate.sh upgrade head` 可正常创建所有表。
