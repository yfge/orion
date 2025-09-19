---
id: 2025-09-19T00-00-00Z-notify-wiring
date: 2025-09-19T08:59:38Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [notify, config]
related_paths:
  - backend/app/core/config.py
  - backend/app/api/v1/router.py
summary: "补充 notify 接口的配置与路由接线：新增 ORION_PUBLIC_API_KEY 与 v1 路由挂载。"
---

说明
- 在 Settings 中增加 `PUBLIC_API_KEY` 以便通过 X-API-Key 校验调用方。
- v1 路由中挂载 notify 子路由，确保 API 可用。
