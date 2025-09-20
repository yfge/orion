---
id: 2025-09-20T16-20-00Z-docker-backend-uvicorn-module
date: 2025-09-20T16:20:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [docker, backend]
related_paths:
  - Docker/backend.Dockerfile
  - backend/alembic.ini
summary: "Fix backend container start: use app.main:app for uvicorn, correct Alembic script_location to avoid path errors."
---

用户原始提示与要求
- 容器日志显示 Alembic 运行后，uvicorn 启动阶段报错退出。

背景与目标
- Docker 容器内工作目录为 `/app/backend`，而项目安装为 `orion-backend`（packages: `app*`）。
- 直接用 `uvicorn backend.app.main:app` 会因导入路径不匹配导致启动失败。

变更内容
- `backend/alembic.ini`：`script_location = alembic`，匹配容器内路径。
- `Docker/backend.Dockerfile`：
  - 设置 `ALEMBIC_CONFIG=alembic.ini`，`alembic upgrade head` 正常执行。
  - `uvicorn app.main:app`（使用安装包中的 `app` 模块名）代替 `backend.app.main:app`。

结果与影响
- 后端容器可正常运行 Alembic 迁移并启动 API 服务。

后续
- 可选：设置 `PYTHONPATH=/app`，以兼容 `backend.app.*` 导入路径；当前采用 `app.main:app` 已可用。
