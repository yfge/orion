---
id: 2025-09-19T00-00-00Z-frontend-messages
date: 2025-09-19T08:34:07Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, messages, crud]
related_paths:
  - frontend/app/messages/page.tsx
  - frontend/app/messages/new/page.tsx
  - frontend/app/messages/[bid]/page.tsx
  - frontend/lib/api.ts
summary: "实现消息定义管理前端：列表/搜索、新建、编辑与删除；类型下拉与 Schema JSON 编辑框。"
---

内容
- 列表 `/messages`：表格显示名称/类型/状态；搜索；跳转新建/编辑；删除确认
- 新建 `/messages/new`：名称、类型（下拉）、状态、Schema JSON 文本域
- 编辑 `/messages/[bid]`：加载并保存字段；支持删除
- API：lib/api.ts 增加 message-definitions 的 list/create/get/update/delete 封装

后续
- 以 JSON Schema 渲染 Schema 字段的编辑（更友好与校验）
- 与端点派发映射联动，提供从消息定义直接查看/配置关联端点
