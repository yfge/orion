---
id: 2025-09-22T07-05-00Z-frontend-i18n-api-keys-page
date: 2025-09-22T07:05:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/app/api-keys/page.tsx
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "本地化 API Keys 页面：标题、表单、提示、表头、状态、操作、搜索、分页与删除确认"
---

## 变更内容

- 页面接入 useI18n；替换所有硬编码中文：
  - 标题/新建区块/字段/占位/创建按钮/新密钥提示与说明；
  - 搜索占位与按钮；
  - 表头（名称/标识/状态/操作）、状态（启用/禁用）、操作按钮（启用/禁用/删除）与删除确认；
  - 空态与分页按钮；
  - 加载与错误回退信息复用 common.\* 键。
- 新增 `apiKeys.*` 文案键（中英）。

## 影响

- API Keys 页面完整支持中英文切换；文案统一可维护。
