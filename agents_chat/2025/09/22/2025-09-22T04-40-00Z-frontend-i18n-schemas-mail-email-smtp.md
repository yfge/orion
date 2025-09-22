---
id: 2025-09-22T04-40-00Z-frontend-i18n-schemas-mail-email-smtp
date: 2025-09-22T04:40:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/lib/schemas.ts
  - frontend/messages/zh-CN.json
  - frontend/messages/en-US.json
summary: "完善 Mailgun/SendGrid/SMTP 相关 Schema 字段标题的多语言支持（from/to/subject/text/html/host/port/...）"
---

## 变更内容

- 在 `endpointConfigSchemaFor` 中为 mailgun/sendgrid/smtp 字段标题接入 i18n：
  - 邮件类：defaultFrom/defaultTo/bodyFormat/timeout 与 headers；
  - SMTP：host/port/useTLS/useSSL/username/password/from/to；
- 在 `mappingSchemaFor` 中为邮件映射字段（from/to/subject/text/html）接入 i18n；
- 新增/更新文案键：`schemas.http.bodyFormat`、`schemas.email.*`、`schemas.smtp.*`。

## 影响

- 新建/编辑端点页面的 Schema 表单字段标题会随语言切换（包含“文本内容覆盖(可选)”、“超时(秒)”、“SMTP 主机”等）。

## 后续

- 若需对描述（description）与占位符也进行本地化，可继续在 schema 中增加对应键并接入 t。
