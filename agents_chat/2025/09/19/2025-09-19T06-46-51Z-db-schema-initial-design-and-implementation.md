---
id: 2025-09-19T06-46-51Z-db-schema-init
date: 2025-09-19T06:46:51Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [db, schema, mysql, alembic, sqlalchemy]
related_paths:
  - backend/app/db/models.py
  - backend/alembic/versions/0001_initial_schema.py
  - backend/alembic/env.py
summary: "按统一约定实现基础表结构（含 bid/软删除/状态/时间戳），完成 SQLAlchemy 模型与 Alembic 初始迁移。"
---

约定
- 所有表：自增 id 主键；`<table>_bid` 为 char(32) UUID（去短横线）唯一；`is_deleted` 软删除；`status` smallint；`created_at`/`updated_at`。

表设计
1) business_systems：业务系统（名称、地址、鉴权方式、app_id/app_secret）。
2) notification_apis：通知 API（归属业务系统、名称、地址、请求/响应 JSON schema）。
3) message_definitions：通知消息定义（名称、类型、schema）。
4) message_dispatches：消息与 API 的映射（schema 映射 JSON、可启用/禁用、唯一对）。
5) send_records：消息发送记录（消息/接口、状态、时间、结果、备注）。
6) send_details：单次发送的明细（每个接口的请求/响应、状态、错误、尝试序号）。
7) users：简单用户（username 唯一、email/phone、hashed_password）。

实现要点
- SQLAlchemy 模型：`backend/app/db/models.py`，提供 `gen_bid()` 生成 32 位 uuid4 hex；混入统一字段；关系与索引。
- Alembic 初始迁移：`backend/alembic/versions/0001_initial_schema.py`；包含所有表与索引/约束；通用列通过 `_common_columns()` 复用。
- Alembic env：导入 models，便于未来 autogenerate（`from backend.app.db import models as _models`）。

MySQL 兼容
- JSON 列用于 schema/mapping/结果等字段；`pool_pre_ping=True` 已启用。
- `updated_at` 模型层 `onupdate=func.now()`，DB 默认 `CURRENT_TIMESTAMP` 确保跨方言兼容（后续可针对 MySQL 增加 `ON UPDATE`）。

后续
- 根据业务细化 auth_method、类型枚举与更多索引。
- 增加模板与速率限制/幂等等扩展表。
