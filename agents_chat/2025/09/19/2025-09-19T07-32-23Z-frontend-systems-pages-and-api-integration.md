---
id: 2025-09-19T00-00-00Z-frontend-systems
date: 2025-09-19T07:32:23Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, systems, crud]
related_paths:
  - frontend/app/systems/page.tsx
  - frontend/app/systems/new/page.tsx
  - frontend/app/systems/[bid]/page.tsx
  - frontend/lib/api.ts
  - frontend/components/ui/textarea.tsx
summary: "实现业务系统管理前端：列表/搜索、新建、编辑与删除；封装前端 API 并对接后端 /api/v1/systems。"
---

内容
- 页面：
  - 列表 `/systems`：表格、搜索、跳转新建/编辑、删除确认
  - 新建 `/systems/new`：表单字段（名称、地址、鉴权方式、app_id/secret、状态）
  - 编辑 `/systems/[bid]`：读取详情、提交更新、支持删除
- 封装：`lib/api.ts` 增加 list/create/get/update/delete 系统的 API 方法，沿用 token 与基地址逻辑
- 组件：新增 `Textarea`（当前页面未使用，后续用于 schema 配置等）

调试
- 设置 `frontend/.env.local` 的 `NEXT_PUBLIC_API_BASE_URL`
- 确保后端已启用 CORS 并运行
- 流程：新建系统 → 列表可见 → 编辑保存/删除
