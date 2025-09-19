---
id: 2025-09-19T00-00-00Z-tests-update
date: 2025-09-19T09:33:08Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [tests]
related_paths:
  - backend/tests/test_notify.py
summary: "更新通知测试，验证发送后 SendRecord 与 SendDetail 落库（基于内存 SQLite）。"
---

说明
- 使用 mocked HttpSender，调用 /api/v1/notify 后查询内存库中的 SendRecord/SendDetail 数量，确认落库成功。
