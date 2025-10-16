---
id: 2025-10-16T03-48-40Z-wechat-oa-gateway
date: 2025-10-16T03:48:40Z
participants: [human, orion-assistant]
models: [gpt-5-codex]
tags: [backend, services]
related_paths:
  - backend/app/services/gateway/wechat_official_account.py
  - backend/app/services/gateway/base.py
  - backend/app/services/gateway/registry.py
  - backend/app/services/gateway/README.md
  - backend/app/repository/wechat_official_account.py
  - backend/alembic/versions/0007_wechat_message_send_record_nullable.py
  - docs/architecture/channels/wechat-official-account.md
summary: "实现公众号网关服务，串联领域模型与适配器"
---

## User original prompt and requirements
- 用户要求按 Task 5 完成服务编排，注册公众号渠道，支持消息构建、发送、重试占位，并保持最小粒度提交。

## Background and goals
- 在完成配置、域模型、适配器后，需要一个网关服务将 API 传入的业务数据转换为领域消息，调用适配器发送，并更新数据库状态。

## Changes
- 构建 `backend/app/services/gateway/` 包：包含网关基类、通道注册表、公众号实现及 README 概览。
- 公众号网关实现支持模板消息发送、渲染模板字段与跳转链接、记录消息实体、调用适配器，以及失败时的重试占位逻辑。
- 仓储层补充创建/更新消息记录、成功失败标记以及按 BID 查询函数；向 Alembic 添加迁移使 `send_record_bid` 可为空以支持外部生成。
- 架构文档新增“服务编排与业务流程”章节，描述端到端流程。

## Outcome and impact
- 网关层具备初始骨架，可在后续 API/任务中调用，实现消息入库、状态跟踪与适配器联动。
- 数据表及仓储扩展确保消息状态、错误信息、重试计数可审计，为后续重试/补发功能提供基础。

## Next steps (TODO)
- 将网关服务接入现有 API 流程，生成 send_record/send_detail，并衔接任务队列调度。
- 实现 `_schedule_retry` 真正的调度逻辑，并在回调处理中更新消息状态。

## Linked commits/PRs
- feat(gateway): scaffold wechat oa service orchestration
