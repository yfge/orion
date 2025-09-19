---
id: 2025-09-19T00-00-00Z-fix-cors-origins-parse
date: 2025-09-19T07:46:07Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [config, cors, pydantic]
related_paths:
  - backend/app/core/config.py
  - .env.example
summary: "修复 ORION_CORS_ORIGINS 解析：支持 '*'、逗号分隔、JSON 数组；避免 Pydantic ValidationError。"
---

问题
- 设置 ORION_CORS_ORIGINS='*' 时，Pydantic 会报 ValidationError（字段期望 list[str]）。

修复
- 在 Settings 中为 CORS_ORIGINS 增加 field_validator(before)：
  - 若值为 '*' → 解析为 ['*']
  - 尝试按 JSON 数组解析；失败则按逗号分隔解析
  - 支持 list/tuple 直接传入
- 更新 .env.example 注释，明确三种可接受格式。

影响
- 现在可灵活通过 .env 配置 CORS 源，避免启动时校验错误。
