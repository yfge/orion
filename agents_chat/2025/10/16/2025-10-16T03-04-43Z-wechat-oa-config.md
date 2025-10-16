---
id: 2025-10-16T03-04-43Z-wechat-oa-config
date: 2025-10-16T03:04:43Z
participants: [human, orion-assistant]
models: [gpt-5-codex]
tags: [backend, config]
related_paths:
  - backend/app/core/config.py
  - .env.example
  - docs/architecture/channels/wechat-official-account.md
  - docs/operations/wechat-official-account-credentials.md
summary: "引入公众号通道配置骨架与默认策略"
---

## User original prompt and requirements
- 用户要求按照 `tasks.md` 的 Step 2（配置与基础设施支持）完成改造并提交。

## Background and goals
- 需要在配置层定义微信公众号的凭证、API 域名、速率限制、重试与断路器参数，并让环境变量与文档对齐。

## Changes
- 在 `backend/app/core/config.py` 新增微信公众号配置模型，提供默认的 API 域名、token TTL、限流、重试与错误码分级，并暴露为 `Settings.WECHAT_OFFICIAL_ACCOUNT`。
- 更新 `.env.example`，补充所有可覆盖的环境变量示例，便于本地与 CI/CD 配置。
- 在 `docs/architecture/channels/wechat-official-account.md` 增加「配置与基础设施默认值」章节，固化默认参数。
- 在运维手册中新增环境变量对照表，指导凭证同步与 secrets 管理。

## Outcome and impact
- 后续实现可直接使用统一的配置对象，确保不同环境通过 env 覆盖即可落地。
- 文档、示例、配置三者保持一致，有助于安全团队配置 secrets 与限流策略。

## Next steps (TODO)
- 按 Task 3 扩展领域模型与存储结构，为 Access Token 与消息事件预留数据模型。
- 准备 Alembic 迁移草稿，记录渠道专属字段。

## Linked commits/PRs
- feat(config): add wechat official account defaults
