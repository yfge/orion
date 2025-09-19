---
id: 2025-09-19T06-53-08Z-migrate-script
date: 2025-09-19T06:53:08Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [script, alembic, env]
related_paths:
  - scripts/migrate.sh
  - backend/alembic.ini
summary: "新增迁移脚本 scripts/migrate.sh：加载 .env/环境中的 ORION_DATABASE_URL 并调用 Alembic。"
---

要点
- 脚本默认从环境变量读取 `ORION_DATABASE_URL`；若未设置且存在 `.env`，会自动 source `.env`。
- 使用 `backend/alembic.ini` 作为 Alembic 配置文件。
- 提供常用子命令：`upgrade|downgrade|current|history|stamp|revision`。
- 未安装 Alembic 时给出操作提示（`conda activate py311 && pip install -e backend`）。

用法示例
- `scripts/migrate.sh upgrade head`
- `scripts/migrate.sh revision -m "init schema"`
