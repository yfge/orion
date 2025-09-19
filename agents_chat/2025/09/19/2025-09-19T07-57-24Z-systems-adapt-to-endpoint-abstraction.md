---
id: 2025-09-19T00-00-00Z-systems-endpoint-abstraction
date: 2025-09-19T07:57:24Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, frontend, endpoints, systems]
related_paths:
  - backend/app/api/v1/endpoints.py
  - backend/app/repository/endpoints.py
  - backend/app/schemas/endpoints.py
  - backend/app/api/v1/router.py
  - frontend/lib/api.ts
  - frontend/app/systems/[bid]/page.tsx
  - frontend/app/systems/[bid]/endpoints/new/page.tsx
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
summary: "调整业务系统管理以适配“端点”抽象：后端新增 endpoints API，前端在系统下管理端点（列表/新建/编辑/删除）。"
---

后端
- 新增 API：
  - POST /api/v1/systems/{system_bid}/endpoints
  - GET  /api/v1/systems/{system_bid}/endpoints
  - GET  /api/v1/endpoints/{endpoint_bid}
  - PATCH/DELETE /api/v1/endpoints/{endpoint_bid}
- 仓储：按 business_system_bid 进行创建、列表与软删除；支持按 endpoint_bid 查询与更新
- 模型（Pydantic）：EndpointCreate/Update/Out/List，包含 transport/adapter_key/config/auth_profile_bid

前端
- 系统编辑页 `/systems/[bid]` 展示端点列表并提供“新建端点”入口
- 新建页 `/systems/[bid]/endpoints/new`：基础字段 + JSON 配置输入
- 编辑页 `/systems/[bid]/endpoints/[endpointBid]`：读取与保存端点配置
- lib/api.ts：封装端点相关 API 调用

说明
- 端点配置暂以 JSON 方式输入，后续可用 JSON Schema 渲染更友好的动态表单；auth_profile 关联将在下一步补齐。
