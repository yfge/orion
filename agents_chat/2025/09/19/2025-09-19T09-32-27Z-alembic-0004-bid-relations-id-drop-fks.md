---
id: 2025-09-19T00-00-00Z-alembic-0004
date: 2025-09-19T09:32:27Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [db, migration]
related_paths:
  - backend/alembic/versions/0004_bid_relations_and_drop_fks.py
summary: "新增 0004 迁移：将 *_id 外键关系迁移为 *_bid + 索引；自动回填并容错删除外键与旧列（幂等）。"
---

要点
- 为 notification_apis/message_dispatches/send_records/send_details 增加 *_bid 列并回填（如存在旧 *_id）。
- 删除旧列前自动在 information_schema 查找并删除对应 FK（兼容自动命名 ibfk_*）。
- 为 MySQL alter_column 增加 existing_type；添加列/索引与回填/删除均做存在性检查，幂等执行。
