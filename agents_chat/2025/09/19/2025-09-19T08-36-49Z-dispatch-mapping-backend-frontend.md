---
id: 2025-09-19T00-00-00Z-dispatch-mapping
date: 2025-09-19T08:36:49Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [dispatch, mapping, endpoints, messages]
related_paths:
  - backend/app/api/v1/endpoints.py
  - backend/app/repository/{endpoints,dispatches}.py
  - backend/app/schemas/{dispatches,endpoints}.py
  - frontend/lib/api.ts
  - frontend/app/messages/[bid]/page.tsx
summary: "实现消息定义与端点之间的派发映射管理：后端支持按消息列出/创建/更新/删除映射；前端在消息编辑页新增端点选择与映射管理。"
---

后端
- 新增 Dispatch API：
  - POST /api/v1/message-definitions/{message_bid}/dispatches（创建）
  - GET /api/v1/message-definitions/{message_bid}/dispatches（列表）
  - GET/PATCH/DELETE /api/v1/dispatches/{dispatch_bid}
- Endpoints API：
  - GET /api/v1/endpoints（全局列表，便于前端下拉）
- Repository：dispatches.py 基于 BID 进行创建、列表（联表返回 endpoint_name、business_system_bid）、更新与软删除

前端
- lib/api.ts：新增 listAllEndpoints、listDispatches、createDispatch、updateDispatch、deleteDispatch
- 消息编辑页：
  - 新增派发映射管理区：下拉选端点、启用开关、Mapping JSON 文本域；展示映射列表与删除操作

说明
- 关联统一使用 BID；仅内部仓储映射到 id。
- 后续可将 Mapping JSON 也用 JSON Schema 表单化，并在端点与消息 schema 之间提供可视化映射工具。
