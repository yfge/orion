---
id: 2025-09-21T07-25-00Z-help-third-party-expanded
date: 2025-09-21T07:25:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [docs, help, third-party]
related_paths:
  - frontend/help/third-party.md
summary: "Expand third-party guide with concepts, generic HTTP example, Mailgun/SMTP cases, and best practices"
---

Context

- 用户要求：面向第三方的文档需要更细，讲清概念/定义/流程，并给出详细例子。

Changes

- 扩写第三方集成指南：
  - 概念：业务系统、端点、消息定义、映射、记录、API Key
  - 对接流程：平台配置 → 第三方调用 → 回查记录
  - 示例：通用 HTTP JSON、Mailgun（form）、SMTP（直连）
  - 同步/异步对比与 request_id 回查
  - 错误码、重试与安全最佳实践

Outcome

- 第三方可直接参照文档完成对接落地，覆盖绝大多数“表单/JSON/SMTP”模型。
