---
id: 2025-09-17T04-45-30Z-mysql-support
date: 2025-09-17T04:45:30Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, mysql, sqlalchemy, config]
related_paths:
  - backend/pyproject.toml
  - backend/app/db/session.py
  - backend/README.md
  - .env.example
summary: "为后端增加 MySQL 支持（PyMySQL 驱动）并启用 pool_pre_ping，更新文档与 .env 示例。"
---

动机
- 需要支持 MySQL 作为后端数据库选项，并提高连接稳定性（避免 MySQL 空闲连接超时导致的 "server has gone away"）。

变更
- 依赖：在 `backend/pyproject.toml` 中加入 `pymysql>=1.0.3`。
- 连接：`create_engine(..., pool_pre_ping=True)` 以预检测失效连接，自动重连。
- 文档：在 `backend/README.md` 增加 MySQL 连接串示例和说明；`.env.example` 增加 MySQL 示例配置。

URL 示例
- `mysql+pymysql://user:password@localhost:3306/orion?charset=utf8mb4`

注意
- 仍可使用 SQLite（默认）或在未来加上 PostgreSQL；MySQL 场景建议开启 `utf8mb4`。
