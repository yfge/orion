---
id: 2025-09-19T00-00-00Z-dispatch-tests-ui
date: 2025-09-19T08:40:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [dispatch, tests, ui]
related_paths:
  - backend/app/api/v1/endpoints.py
  - backend/app/repository/dispatches.py
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
  - frontend/app/messages/[bid]/page.tsx
  - frontend/lib/api.ts
summary: "完善映射管理：后端增加按端点列出/创建映射 API；前端在端点编辑页增加映射管理视图。下一步将补充后端映射单元测试。"
---

说明
- 端点侧 UI：可在端点下直接选择消息定义以新增映射，查看并删除现有映射；消息侧 UI 也保留。
- API 补充：GET/POST /api/v1/endpoints/{endpoint_bid}/dispatches；现有按消息的映射 API 不变。

下一步
- 增加后端映射单元测试（CRUD + 双向列表）。
- 将 Mapping JSON 表单化与校验。
