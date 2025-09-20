---
id: 2025-09-20T16-30-00Z-alembic-env-import-fix
date: 2025-09-20T16:30:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [alembic, docker, backend]
related_paths:
  - backend/alembic/env.py
  - backend/alembic.ini
  - Docker/backend.Dockerfile
summary: "Make Alembic env.py import robust across dev and container (backend.app.* vs app.*); set ALEMBIC_CONFIG and uvicorn module path."
---

用户原始提示与要求
- 后端容器迁移后 uvicorn 启动报错 ModuleNotFoundError: No module named 'backend'。

变更内容
- env.py 调整 sys.path 并 try-import：优先尝试 `backend.app.*`，失败回退 `app.*`。
- alembic.ini `script_location = alembic`（匹配容器路径）。
- Dockerfile 设置 `ALEMBIC_CONFIG=alembic.ini`，并使用 `uvicorn app.main:app`。

结果
- 容器内迁移与启动均可用，兼容本地与容器两种运行方式。
