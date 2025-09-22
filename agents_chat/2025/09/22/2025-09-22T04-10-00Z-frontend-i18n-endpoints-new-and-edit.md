---
id: 2025-09-22T04-10-00Z-frontend-i18n-endpoints-new-and-edit
date: 2025-09-22T04:10:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/app/systems/[bid]/endpoints/new/page.tsx
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
  - frontend/lib/schemas.ts
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "端点（新建/编辑）页面本地化；新增 schema 中“请求头(键值)”等标题的 i18n 支持"
---

## 背景与目标

- 用户反馈：新建端点中“请求头(键值)”尚未本地化；编辑端点页面未改造。

## 本次变更

- 新建端点（/systems/[bid]/endpoints/new）：
  - 接入 useI18n；本地化页面标题、字段（名称/类型/适配器/HTTP 地址/认证等）、Schema 表单/高级 JSON、校验按钮与消息、按钮（创建/取消）。
  - 通过 `endpointConfigSchemaFor(adapterKey, t)` 传入 t，使 Schema 中“请求头(键值)”等标题可本地化。
- 编辑端点（/systems/[bid]/endpoints/[endpointBid]）：
  - 接入 useI18n；本地化标题、删除确认、字段、Schema 表单、提示（Mailgun/SendGrid/SMTP）、派发映射区块（标题、字段、按钮、表头、空态）、测试发送区块、保存/取消按钮与加载/错误提示。
  - RJSF 也改为 `endpointConfigSchemaFor(adapterKey, t)` 以呈现本地化 Schema 标题。
- 公共 Schema 标题 i18n：
  - `frontend/lib/schemas.ts` 为 `endpointConfigSchemaFor` 增加可选 t，动态设置 headers 相关标题（headers/headersOptional/extraHeadersOptional）。
  - 新增 messages：`schemas.http.headers*` 与 `endpoints.*` 分组键。

## 结果与影响

- 新建/编辑端点页面完全支持中英切换；
- “请求头(键值)”等 Schema 标题也随语言变化；
- 不改变数据结构与接口行为。

## 下一步

- 继续抽取 messages/records/auth 模块的页面文案；
- 长期将 RJSF 所用 schema 的更多 label/description 全量 i18n 化。
