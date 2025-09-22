---
id: 2025-09-22T03-20-00Z-frontend-i18n-extract-home
date: 2025-09-22T03:20:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/app/page.tsx
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "抽取首页 Home 页面文案到 i18n messages，接入 useI18n 渲染"
---

## 变更内容

- Home 页面所有用户可见文本改为从 `t()` 取值：标题、副标题、统计卡片、最近发送表格、健康区块；
- 新增/补充消息键：`home.*` 与 `common.success/failed/pending/noData`；

## 影响

- 首页随语言切换即时本地化；字符串集中管理，便于翻译与审查。

## 下一步

- 继续抽取系统/消息/记录/认证页面文案；
- 视需要将日期/数字格式化抽象成工具函数并采用本地化格式。
