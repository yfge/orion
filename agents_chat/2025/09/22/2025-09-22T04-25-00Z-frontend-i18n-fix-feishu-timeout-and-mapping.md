---
id: 2025-09-22T04-25-00Z-frontend-i18n-fix-feishu-timeout-and-mapping
date: 2025-09-22T04:25:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/lib/schemas.ts
  - frontend/app/apis/new/page.tsx
  - frontend/app/systems/[bid]/endpoints/[endpointBid]/page.tsx
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "本地化补全：文本内容覆盖(可选)、Webhook URL、超时(秒) 等 Schema 标题"
---

## 背景

- 用户反馈：仍有未本地化或未随着语言切换的字段标题，包括“文本内容覆盖(可选)”“Webhook URL \*”“超时(秒)”。

## 变更

- schemas：
  - `endpointConfigSchemaFor(adapterKey, t)` 新增对 `timeout` 与 Feishu `Webhook URL` 的 i18n；已有 headers 相关标题继续复用；
  - `mappingSchemaFor(adapterKey, messageType, t)` 支持传入 t，并将 Feishu 文本映射标题本地化（`schemas.feishu.textOverride`）。
- 页面：
  - 编辑端点页将 `mappingSchemaFor` 调用改为传入 t；
  - 新建 API 页将 `endpointConfigSchemaFor` 传入 t，以呈现本地化 Schema 标题；
- 文案：
  - 新增 `schemas.common.timeout`、`schemas.http.webhookUrl`、`schemas.feishu.textOverride` 键（中英）。

## 结果

- “文本内容覆盖(可选)”“Webhook URL”“超时(秒)”在中英文间切换正确；必填星号由 RJSF/表单组件按 required 自动呈现。

## 后续

- 逐步为其余 Schema 字段（如 mailgun/sendgrid/smtp 的 from/to/subject 等）补全 i18n。
