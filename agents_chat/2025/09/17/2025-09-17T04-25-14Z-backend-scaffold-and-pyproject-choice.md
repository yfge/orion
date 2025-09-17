---
id: 2025-09-17T04-25-14Z-backend-scaffold
date: 2025-09-17T04:25:14Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, scaffolding, alembic, packaging, decision]
related_paths:
  - backend/app/
  - backend/alembic/
  - backend/pyproject.toml
  - backend/README.md
  - docs/architecture/overview.md
  - README.md
summary: "完成后端 FastAPI 脚手架与 Alembic；决定将 pyproject 移至 backend 目录并更新文档。"
---

结果概述
- 建立 FastAPI 基础：`/healthz` 与 `/api/v1/ping` 路由可用。
- 引入配置系统：`pydantic-settings`，环境前缀 `ORION_`，默认 `sqlite:///./orion.db`。
- 初始化数据库层：`SQLAlchemy Base`、`SessionLocal` 与 `session_scope`。
- 配置 Alembic：`backend/alembic.ini`、`env.py`（从 Settings 读取 DB URL）、`versions/` 占位。
- 打包与工具：将 Python 打包与依赖声明放在 `backend/pyproject.toml`；根仍通过 pre-commit 管控 ruff/black/isort。
- 文档：更新 `backend/README.md` 与 `docs/architecture/overview.md`；根 `README.md` 补充后端运行说明。

关键决策：pyproject 文件位置
- 可选方案对比：
  - 根目录集中（单一 `pyproject.toml`）
    - 优点：工具（ruff/black/isort）与依赖集中；安装命令简单。
    - 缺点：前后端边界不清晰；Python 依赖“污染”根，前端为主的开发者安装体验不佳。
  - 后端独立（`backend/pyproject.toml`）【采纳】
    - 优点：后端与前端清晰隔离；Python 依赖仅在 `backend` 生效；Monorepo 模块边界更干净。
    - 代价：工具配置需与 pre-commit 协调；安装命令改为 `pip install -e backend` 或在 `backend` 内执行。
- 结论：采用“后端独立”，将 `pyproject.toml` 迁移至 `backend/`，并同步更新文档与命令。

主要变更
- 新增：
  - `backend/app/main.py`、`backend/app/api/v1/router.py`、`backend/app/core/config.py`
  - `backend/app/db/base.py`、`backend/app/db/session.py`
  - `backend/alembic.ini`、`backend/alembic/env.py`、`backend/alembic/script.py.mako`、`backend/alembic/versions/.gitkeep`
  - `backend/pyproject.toml`（后端独立打包/依赖）
  - `.env.example`（示例环境变量）
  - `docs/architecture/overview.md`（架构总览）
- 更新：
  - `backend/README.md`（conda、安装与 Alembic 命令）
  - `README.md`（新增后端依赖与运行）

如何运行（本地）
- 激活环境：`conda activate py311`
- 安装依赖：
  - 在仓库根目录：`pip install -e backend`
  - 或进入后端目录：`cd backend && pip install -e .`
- 启动服务：`uvicorn backend.app.main:app --reload`
- 健康检查：GET `http://127.0.0.1:8000/healthz`
- Ping：GET `http://127.0.0.1:8000/api/v1/ping`

后续建议
- 定义领域模型与首个迁移（如 `Notification` 表与状态机字段）。
- 选择任务方案（APScheduler/Celery/RQ）并设计重试与退避策略。
- 设计适配器接口（Feishu/WeCom/Email/SMS）与依赖注入容器。
- 增加配置分层（dev/staging/prod）与日志/观测（结构化日志、OpenTelemetry）。
