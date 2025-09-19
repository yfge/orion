---
id: 2025-09-19T00-00-00Z-config-cors-str
date: 2025-09-19T07:51:38Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [config, cors, pydantic]
related_paths:
  - backend/app/core/config.py
summary: "补充修复：CORS_ORIGINS 字段类型允许 str/None（来自环境变量的原始字符串），再由 validator 统一解析。"
---

动机
- 某些环境下 env 源会先以字符串传入；将字段类型放宽为 `list[str] | str | None` 以避免 settings 源的类型不匹配，再交由 validator 解析为 list。

变更
- backend/app/core/config.py：`CORS_ORIGINS` 注解从 `list[str]` → `list[str] | str | None`。
