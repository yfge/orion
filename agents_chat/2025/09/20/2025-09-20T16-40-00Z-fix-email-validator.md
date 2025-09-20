---
id: 2025-09-20T16-40-00Z-fix-email-validator
date: 2025-09-20T16:40:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, deps]
related_paths:
  - backend/pyproject.toml
summary: "Add pydantic[email] extra to resolve EmailStr import error in container."
---

用户原始提示与要求
- 后端容器启动报错：ImportError: email-validator is not installed。

变更内容
- 在 `backend/pyproject.toml` 依赖中加入 `pydantic[email]`，安装 email-validator 可选依赖。

结果
- 使用 EmailStr（auth schema）时不再报错；容器可正常导入并启动。
