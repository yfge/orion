---
id: 2025-09-19T00-00-00Z-bid-models-repos
date: 2025-09-19T09:32:48Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [models, repos, notify]
related_paths:
  - backend/app/db/models.py
  - backend/app/repository/dispatches.py
  - backend/app/repository/endpoints.py
  - backend/app/services/notify.py
  - backend/app/api/v1/notify.py
summary: "模型与仓储改为 BID 关联；notify 成功后落库 SendRecord/SendDetail；路由与逻辑同步调整。"
---

内容
- 模型：notification_apis / message_dispatches / send_records / send_details 的外键列改为 *_bid；关系改为 viewonly+primaryjoin。
- 仓储：endpoints/dispatches 统一按 *_bid 查询与列表；全局端点列表输出 BID。
- 通知：成功发送后写入 SendRecord/SendDetail（*_bid）；API 层统一 commit。
