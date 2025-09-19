---
id: 2025-09-19T00-00-00Z-backend-tests
date: 2025-09-19T07:53:15Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [tests, pytest, fastapi]
related_paths:
  - backend/pyproject.toml
  - backend/tests/conftest.py
  - backend/tests/test_health.py
  - backend/tests/test_auth.py
summary: "配置后端测试框架（pytest）并提供基础用例：健康检查、注册/登录/用户列表。"
---

内容
- backend/pyproject.toml：添加可选依赖组 test（pytest）与 pytest 配置（testpaths、addopts）
- 测试基建：
  - conftest：创建 in-memory SQLite（StaticPool 共享连接），建表；覆盖 FastAPI 的 get_db 依赖；提供 app/client fixtures
  - 用例：test_health（/healthz），test_auth（注册→登录→用户列表）

运行
- 安装测试依赖：`pip install -e backend[test]`
- 运行：`pytest`（或 `pytest -q`）
