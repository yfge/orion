---
id: 2025-09-22T05-00-00Z-frontend-i18n-extract-messages
date: 2025-09-22T05:00:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/app/messages/page.tsx
  - frontend/app/messages/new/page.tsx
  - frontend/app/messages/[bid]/page.tsx
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "抽取 Messages（消息定义）模块列表/新建/编辑页面文案，接入 useI18n 与验证按钮本地化"
---

## 变更内容

- 列表页：标题、搜索、表头、操作按钮、空态本地化；
- 新建/编辑页：标题、字段名、Schema JSON/预览、示例数据、校验按钮与结果、错误提示、保存/取消按钮；
- 增加 messages._ 键并复用 common._；

## 影响

- 消息定义模块完全支持中英切换，验证按钮与提示语也统一抽取。

## 后续

- 继续抽取 Records（发送记录）与 Auth（登录/注册）模块文案；
- 视需要扩展 schema 字段的 description/placeholder 的 i18n。
