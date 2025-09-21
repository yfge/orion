---
id: 2025-09-21T07-15-00Z-help-third-party
date: 2025-09-21T07:15:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [docs, help, third-party]
related_paths:
  - frontend/help/third-party.md
  - frontend/help/index.md
summary: "Add Third-party Integration guide (auth, sync/async notify, records query, best practices)"
---

User request

- 面向第三方的帮助文档，说明系统使用方式，包含异步通知与发送记录检索。

Changes

- `frontend/help/third-party.md`：新增“第三方集成指南”，涵盖：
  - 基础信息与鉴权（Bearer/X-API-Key/Basic）
  - 同步 `POST /api/v1/notify` 与异步 `POST /api/v1/notify/async`（含 request_id）
  - 公开发送记录查询接口 `/api/v1/notify/send-records*`
  - curl 示例、错误码与最佳实践、安全建议
- `frontend/help/index.md`：加入“第三方集成指南”的索引链接。

Outcome

- 第三方可按文档快速集成公开 API，包含异步闭环与回查流程。
