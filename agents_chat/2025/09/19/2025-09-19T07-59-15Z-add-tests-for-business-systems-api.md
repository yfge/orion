---
id: 2025-09-19T00-00-00Z-tests-systems
date: 2025-09-19T07:59:15Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [tests, api, systems]
related_paths:
  - backend/tests/test_systems.py
  - backend/tests/conftest.py
summary: "新增业务系统 API 的单元测试：覆盖创建、查询、列表/搜索、更新与软删除。修正 conftest 导入 models 以创建表。"
---

内容
- 用例：
  - POST /api/v1/systems 创建
  - GET /api/v1/systems/{bid} 查询
  - GET /api/v1/systems 列表 + q 搜索
  - PATCH /api/v1/systems/{bid} 更新
  - DELETE /api/v1/systems/{bid} 软删除，并验证后续 404 与列表不再包含
- 基建：
  - conftest 确保导入 models 再 Base.metadata.create_all，以免 metadata 为空导致无表

运行
- `pip install -e backend[test] && pytest`
