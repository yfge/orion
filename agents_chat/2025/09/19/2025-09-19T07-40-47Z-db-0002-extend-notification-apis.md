---
id: 2025-09-19T00-00-00Z-db-0002
date: 2025-09-19T07:40:47Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [db, migration, extensibility]
related_paths:
  - backend/alembic/versions/0002_extend_notification_apis.py
  - backend/app/db/models.py
summary: "扩展 notification_apis：新增 transport/adapter_key/config/auth_profile_id 字段，为 HTTP/MQ 等多形态端点与认证配置覆盖打基础。"
---

说明
- transport：端点传输类型（http/mq 等）
- adapter_key：适配器标识（http.generic/mq.kafka 等）
- config(JSON)：按适配器自定义配置（method/path/headers/timeout/策略 或 MQ 的 topic/exchange 等）
- auth_profile_id：可选认证配置引用（后续迁移添加外键）
