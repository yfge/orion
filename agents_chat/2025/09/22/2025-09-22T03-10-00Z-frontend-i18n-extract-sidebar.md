---
id: 2025-09-22T03-10-00Z-frontend-i18n-extract-sidebar
date: 2025-09-22T03:10:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/components/sidebar.tsx
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "抽取 Sidebar 文案到 i18n messages，并接入 useI18n"
---

## 变更内容

- Sidebar 组件将原硬编码中文改为使用 `t('nav.*')` 渲染；
- 在 messages 中新增 nav.overview/nav.systems/nav.apis/nav.messages/nav.records/nav.users/nav.apiKeys/nav.help；

## 影响

- 侧边导航栏随语言切换自动本地化；不影响路由与交互。

## 下一步

- 抽取首页 Home 页面文案；随后逐页推进系统/消息/记录/认证等模块。
