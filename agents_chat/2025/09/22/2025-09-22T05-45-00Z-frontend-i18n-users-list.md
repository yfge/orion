---
id: 2025-09-22T05-45-00Z-frontend-i18n-users-list
date: 2025-09-22T05:45:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/app/users/page.tsx
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "用户列表页面本地化：标题、搜索、刷新/注册/退出、统计、表头与复制按钮"
---

## 变更内容

- 用户列表页接入 useI18n；本地化：标题、搜索占位、刷新按钮（含加载态）、“注册新用户”“退出登录”、总数统计前后缀、表头和复制按钮；
- 错误默认文案改为 `common.failedLoad`。

## 影响

- 用户管理页完整支持中英文切换；与其他模块文案风格一致。
