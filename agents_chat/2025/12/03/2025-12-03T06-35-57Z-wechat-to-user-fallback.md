---
id: 2025-12-03T06-35-57Z-wechat-to-user-fallback
date: 2025-12-03T06:35:57Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, wechat, mapping]
related_paths:
  - backend/app/services/gateway/wechat_official_account.py
summary: "微信网关支持 openid 别名，防止 to_user 缺失"
---

## User original prompt and requirements
- `/api/v1/notify/` 调用仍然报 `WechatSendPayload.__init__() missing to_user`，希望修复。

## Background and goals
- 前端/消息定义可能使用 `openid` 或 `touser` 字段名，网关之前过滤后丢失 `to_user`，导致构造 payload 失败。
- 目标：在网关层统一别名，缺省从 context.openid 补齐 to_user。

## Changes
- backend/app/services/gateway/wechat_official_account.py：
  - normalize 阶段接受 `openid` → `to_user`、`touser` → `to_user`，并保留现有别名映射。
  - 如果仍缺 to_user，尝试从 context.openid 补齐。

## Outcome and impact
- `/api/v1/notify/` 经过映射后，若数据里提供了 openid/touser/context.openid，将被正确转成 to_user，不再触发缺参错误。

## Next steps (TODO)
- 如模板 id 也存在别名/缺省场景，可按需增加类似兜底。

## Linked commits/PRs
- 尚未提交 commit
