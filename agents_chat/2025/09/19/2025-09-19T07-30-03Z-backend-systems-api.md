---
id: 2025-09-19T00-00-00Z-backend-systems-api
date: 2025-09-19T07:30:03Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, api, systems]
related_paths:
  - backend/app/api/v1/systems.py
  - backend/app/repository/systems.py
  - backend/app/schemas/systems.py
  - backend/app/api/v1/router.py
summary: "新增业务系统管理 API：创建、查询、列表（分页/搜索）、更新、软删除；落库遵循统一约定。"
---

端点
- POST /api/v1/systems：创建业务系统
- GET /api/v1/systems：分页列表（limit/offset）+ 按名称 q 搜索
- GET /api/v1/systems/{bid}：按 BID 查询
- PATCH /api/v1/systems/{bid}：更新（局部）
- DELETE /api/v1/systems/{bid}：软删除（is_deleted=true）

实现
- schemas：BusinessSystemCreate/Update/Out/List
- repository：CRUD 与分页、ilike 搜索、软删除
- router 集成：在 v1/router 中挂载 systems 路由

说明
- 名称未强制唯一，如需可后续增加唯一约束或业务校验。
- Out 模型包含 app_secret（管理控制台场景）；生产可改为掩码或脱敏字段。
