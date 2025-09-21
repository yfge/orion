---
id: 2025-09-21T05-55-00Z-migrate-script-fix
date: 2025-09-21T05:55:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [tooling, alembic, scripts]
related_paths:
  - scripts/migrate.sh
  - backend/alembic.ini
summary: "Fix migrate.sh to run Alembic from backend dir so script_location resolves to backend/alembic"
---

Issue

- `scripts/migrate.sh upgrade head` 报错 `Path doesn't exist: './alembic'`，因为 alembic 的 `script_location=alembic` 是相对路径，脚本在仓库根执行时解析到错误目录。

Change

- 脚本进入 `backend/` 再执行 `alembic -c alembic.ini ...`，保持 `script_location=alembic` 的相对路径一致。

Outcome

- 现在在仓库根直接运行 `scripts/migrate.sh upgrade head` 可正常升级到 head。
