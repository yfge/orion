---
id: 2025-09-22T06-30-00Z-frontend-help-i18n-fix-title
date: 2025-09-22T06:30:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend, docs]
related_paths:
  - frontend/app/help/page.tsx
  - frontend/app/help/[slug]/page.tsx
summary: "修复帮助中心标题/副标题未按语言切换：messages 路径查找兼容 frontend/ 与根目录"
---

## 问题

- 在某些执行上下文下（cwd 为 frontend 或仓库根），帮助中心服务端读取 messages 的路径不一致，导致 t() 读取失败，回退到中文默认。

## 变更

- loadMessages 增加双路径查找：先查 ./messages/<loc>.json，不存在则查 ./frontend/messages/<loc>.json。

## 结果

- 标题“帮助中心 / Help Center”与副标题随语言正确切换。
