---
id: 2025-09-19T00-00-00Z-message-defs
date: 2025-09-19T08:31:17Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [messages, api, tests]
related_paths:
  - backend/app/api/v1/message_definitions.py
  - backend/app/repository/message_definitions.py
  - backend/app/schemas/message_definitions.py
  - backend/app/api/v1/router.py
  - backend/tests/test_message_definitions.py
summary: "实现消息定义（MessageDefinition）的 CRUD API 与单元测试；输出与关联统一使用 BID。"
---

内容
- API：/api/v1/message-definitions（POST/GET 列表/GET 详情/PATCH/DELETE）
- Repository：基于 BID 的创建、查询、列表（支持 q 搜索）、更新、软删除
- 模型：MessageDefCreate/Update/Out/List（含 name/type/schema/status）
- 测试：覆盖 CRUD 完整流程；与内存 SQLite + TestClient 集成

注意
- Pydantic 关于 `schema` 字段命名会有 warning（shadow BaseModel attr），不影响功能；可后续改名为 `definition_schema` 避免警告。
