---
id: 2025-09-19T00-00-00Z-pytest-asyncio-disable
date: 2025-09-19T08:13:46Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [tests, pytest]
related_paths:
  - backend/pyproject.toml
summary: "禁用全局 pytest-asyncio 插件自动加载，规避与 pytest 8 的不兼容导致的 INTERNALERROR。"
---

说明
- 在本项目 pytest 配置中加入 `-p no:pytest_asyncio`，避免加载全局旧版插件；若需要 asyncio 测试，可升级插件版本或局部启用。
