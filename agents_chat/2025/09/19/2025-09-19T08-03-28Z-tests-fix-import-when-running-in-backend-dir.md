---
id: 2025-09-19T00-00-00Z-tests-import-fix
date: 2025-09-19T08:03:28Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [tests, import]
related_paths:
  - backend/tests/conftest.py
summary: "修复在 backend 目录下直接运行 pytest 的导入问题：在 conftest 中将仓库根路径加入 sys.path。"
---

问题
- 在 backend 目录下执行 `pytest` 时，`from backend.app.main import create_app` 报 `ModuleNotFoundError: No module named 'backend'`。

修复
- 在 `backend/tests/conftest.py` 顶部，将仓库根目录加入 `sys.path`，以便 `import backend.*` 能正常解析，无需额外设置 PYTHONPATH。

影响
- 现在可以在仓库根或 backend 目录执行 `pytest`，导入路径均可用。
