---
id: 2025-09-21T04-55-00Z-notify-bearer-auth
date: 2025-09-21T04:55:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [backend, notify, auth]
related_paths:
  - backend/app/deps/api_key.py
  - backend/tests/test_notify_basic_auth.py
summary: "Add Bearer <key> support for Notify auth alongside X-API-Key and Basic"
---

User original prompt and requirements

- 提问：“是不是用类似 openai 的 Bearer 更标准？”——需要支持 `Authorization: Bearer <key>`。

Changes

- deps/api_key: 新增 `_check_bearer_auth()`，在 `require_api_key()` 中加入 Bearer 检查。
- tests: 在 `test_notify_basic_auth.py` 内新增 Bearer 正确/错误用例。

Outcome and impact

- 现在支持三种方式：`X-API-Key`、`Authorization: Bearer <key>`、`Authorization: Basic base64(api:<key>)`。
- 推荐在公共调用方使用 Bearer 方式，语义更清晰。
