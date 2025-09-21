---
id: 2025-09-21T06-55-00Z-notify-async-and-public-records
date: 2025-09-21T06:55:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, api, notify, records]
related_paths:
  - backend/app/api/v1/notify.py
  - backend/app/services/notify.py
  - backend/app/repository/send_records.py
summary: "Add async Notify API and public Send Records APIs with API key auth; support request_id filtering"
---

User request and goals

- 增加异步的 notify 接口（接受后即返回），并提供发送记录查询接口。两者都需要 API Key 鉴权。

Changes

- 新增异步通知接口：`POST /api/v1/notify/async`（202 Accepted）
  - 使用 FastAPI `BackgroundTasks` 执行实际发送，避免客户端阻塞。
  - 支持 `request_id`（可选），会写入 `SendRecord.remark`，用于回查。
  - 返回字段：`accepted`、`request_id`、`estimated_dispatches`（估算派发数量）。
- 公开发送记录查询（均需 API Key）：
  - `GET /api/v1/notify/send-records`：支持按 `message_definition_bid`、`notification_api_bid`、`status`、`start_time`、`end_time`、`request_id` 过滤。
  - `GET /api/v1/notify/send-records/{bid}`：获取单条记录详情。
  - `GET /api/v1/notify/send-records/{bid}/details`：获取记录的发送明细。
- 内部实现：
  - `services/notify._notify` 支持 remark；`notify_by_name/notify_by_bid` 传递 remark。
  - `repository/send_records.list_send_records` 新增 `remark` 过滤；查询结果附带关联系统/端点/消息名称以便展示。

Auth & compatibility

- 所有新增接口均依赖现有 `require_api_key`（支持 X-API-Key / Bearer / Basic api:<key>）。
- 同步通知 `POST /api/v1/notify/` 未变；新增接口为异步选项，兼容旧用法。

Outcome

- 客户端可选择异步下发并通过 `request_id` 查询记录闭环；查询接口可供外部系统集成自助回查。

Next steps

- 如需大规模异步与重试、限速：建议引入任务队列（如 Celery/RQ）替换 BackgroundTasks，并完善重试/幂等。
