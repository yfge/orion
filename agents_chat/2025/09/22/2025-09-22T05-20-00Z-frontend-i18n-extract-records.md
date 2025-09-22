---
id: 2025-09-22T05-20-00Z-frontend-i18n-extract-records
date: 2025-09-22T05:20:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/app/records/page.tsx
  - frontend/app/records/[bid]/page.tsx
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "抽取 Records（发送记录）模块列表与详情页文案，覆盖过滤项、表头、状态、分页与详情字段"
---

## 变更内容

- 列表页：标题、过滤项（全部消息/端点/状态、筛选按钮）、表头（时间/消息/端点/状态/操作）、状态文案、详情按钮、空态、分页按钮本地化；
- 详情页：标题、返回按钮、字段标签（Record BID/时间/消息/端点/状态）、响应结果标题、尝试记录区块（表头/空态）、状态文案本地化；
- 新增 `records.*` 文案键并复用 `common.*` 状态与空态。

## 影响

- Records 模块完整支持中英切换，详情页面字段与表格头一致。

## 后续

- 可进一步本地化时间/数字格式展示（目前使用 `toLocaleString()`）。
