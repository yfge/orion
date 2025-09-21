---
id: 2025-09-21T00-00-00Z-frontend-smtp-schema
date: 2025-09-21T00:00:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [frontend, email, smtp, sendgrid]
related_paths:
  - frontend/lib/schemas.ts
  - frontend/app/apis/new/page.tsx
summary: "Add SMTP/SendGrid config schemas and enable creating SMTP endpoints in UI"
---

User original prompt and requirements
- Prompt (CN): “继续处理邮件的问题，回查一下之前的进度” —— 需要回顾邮件（Mailgun/SendGrid/SMTP）支持的现状，并继续推进尚缺的部分。

Background and goals
- 后端已实现 HttpSender + SmtpSender，含 Mailgun/SendGrid 便捷鉴权与 /endpoints/{id}/send-test；相关单测已覆盖且通过。
- 前端仍缺少：SMTP 端点创建表单的配置 Schema；SendGrid 配置 Schema；“新建通知 API”页面目前仅支持 http/mq，不支持 smtp。

Changes
- frontend/lib/schemas.ts
  - 新增 http.sendgrid 配置 Schema（url、api_key、from、to、headers、timeout）。
  - 新增 smtp.* 配置 Schema（host、port、use_tls、use_ssl、username、password、from、to、timeout）。
  - 映射 Schema：为 http.sendgrid 与 smtp.* 提供通用邮件字段（from、to、subject、text、html）。
- frontend/app/apis/new/page.tsx
  - 在“类型”下拉新增 smtp；选择 smtp 时默认适配器为 smtp.generic。
  - 适配器列表：为 http 增加 http.sendgrid；为 smtp 提供 smtp.generic。
  - 仅在 http 类型显示地址输入框；smtp 使用配置表单（host/port/...）。

Outcome and impact
- 现在可在前端直接创建 SMTP 端点，并便捷配置 SendGrid/Mailgun/SMTP 所需字段，减少手动 JSON 配置负担。
- 与后端 send-test/notify 兼容；不改变现有 http 行为。

Next steps (TODO)
- 在端点编辑页面补充 Schema 表单（若尚未存在编辑页）。
- 可进一步为 SendGrid 提供更贴近其 JSON 结构的映射辅助（personalizations/from/content）。
- 增加“发送测试”按钮至端点详情页，调用 /endpoints/{id}/send-test。

Linked commits/PRs
- 本次变更：前端 Schema 与新建页面的增量修改（未生成单独提交记录示例）。

