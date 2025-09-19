---
id: 2025-09-19T00-00-00Z-notify-api
date: 2025-09-19T08:50:20Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [notify, api, service, auth]
related_paths:
  - backend/app/api/v1/notify.py
  - backend/app/services/notify.py
  - backend/app/services/templating.py
  - backend/app/deps/api_key.py
  - backend/app/repository/message_definitions.py
  - backend/tests/test_notify.py
summary: "实现 /api/v1/notify：按消息名或 BID + data 调用，路由到映射端点进行发送；支持 X-API-Key 校验；添加模板渲染与单测（mock Sender）。"
---

内容
- API：POST /api/v1/notify
  - 入参：message_name 或 message_definition_bid + data
  - 输出：每个派发的 status_code/body
  - Auth：X-API-Key（ORION_PUBLIC_API_KEY 为空则放行，后续可改严格）
- Service：notify_by_name/notify_by_bid
  - 基于 MessageDefinition.schema 渲染（${var} 占位符），与 Dispatch.mapping 合并
  - 发送 HTTP（Feishu 特殊兜底为 text）
- 模板：递归替换 ${var}（支持 data 嵌套路径）
- 测试：mock HttpSender，验证返回结构
