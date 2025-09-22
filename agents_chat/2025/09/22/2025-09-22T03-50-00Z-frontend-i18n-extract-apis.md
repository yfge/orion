---
id: 2025-09-22T03-50-00Z-frontend-i18n-extract-apis
date: 2025-09-22T03:50:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/app/apis/page.tsx
  - frontend/app/apis/new/page.tsx
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "抽取 Notify APIs 模块（列表/新建）文案，统一使用 useI18n 与 messages"
---

## 变更内容

- 列表页：标题、搜索、空态文案与链接、表头、操作按钮、分页（上一页/下一页）；
- 新建页：标题、无系统提示与链接、字段标签（系统/名称/类型/适配器/HTTP 地址/认证/Schema 表单/高级 JSON）、配置校验按钮与提示、错误提示与按钮文案；
- 增补 `apis.*` 键，并复用 `common.*` 键（创建/取消/加载等）。

## 影响

- Notify APIs 模块完全支持中英文切换；后续可继续完善提示与字段的说明文本。

## 下一步

- 抽取 Messages/Records/Auth 模块文案，按相同模式推进并保留 agents_chat。
