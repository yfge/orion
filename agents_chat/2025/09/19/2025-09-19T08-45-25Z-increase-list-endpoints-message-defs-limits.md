---
id: 2025-09-19T00-00-00Z-increase-limits
date: 2025-09-19T08:45:25Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [api, paging]
related_paths:
  - backend/app/api/v1/endpoints.py
  - backend/app/api/v1/message_definitions.py
summary: "将全局端点列表与消息定义列表的 limit 上限提升至 1000（原 200），以匹配前端默认的 500。"
---

说明
- 前端在部分页面默认使用 limit=500 拉取下拉选项（端点/消息定义），原后端上限 200 导致 422 校验失败。
- 调整：两个列表接口的 limit 上限由 200 提升至 1000。
