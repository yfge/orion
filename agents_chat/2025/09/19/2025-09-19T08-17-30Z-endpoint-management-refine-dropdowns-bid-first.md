---
id: 2025-09-19T00-00-00Z-endpoints-refine
date: 2025-09-19T08:17:30Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [endpoints, frontend, api]
related_paths:
  - backend/app/api/v1/endpoints.py
  - backend/app/repository/endpoints.py
  - backend/app/api/v1/auth_profiles.py
  - backend/app/repository/auth_profiles.py
  - backend/app/schemas/{endpoints,auth_profiles}.py
  - backend/app/api/v1/router.py
  - frontend/lib/api.ts
  - frontend/app/systems/[bid]/endpoints/new/page.tsx
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
summary: "端点管理细化：后端输出统一以 BID 为关联；新增 AuthProfile CRUD；前端端点表单下拉选择（transport/adapter/auth_profile），更友好。"
---

变更
- 后端：
  - Endpoints API 输出包含 business_system_bid 与 auth_profile_bid；列表/详情均返回 BID 以便前端联动。
  - 新增 AuthProfile CRUD（/api/v1/auth-profiles）供端点选择绑定；Repository/Schema 同步。
- 前端：
  - 端点新建/编辑页使用下拉：transport（http/mq）、adapter（依类型可选 http.generic/http.feishu_bot 或 mq.kafka/mq.rabbit）、auth_profile（来自后端列表）。
  - API 封装增加 listAuthProfiles；端点表单提交携带 auth_profile_bid。

约定
- 关联一律通过 BID 进行输入输出；仅内部更新使用 id（数据库层面）。
- 后续可用 JSON Schema 驱动端点配置表单，进一步减少原始 JSON 编辑。
