---
id: 2025-09-22T06-55-00Z-frontend-i18n-fix-api-keys-label
date: 2025-09-22T06:55:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [i18n, frontend]
related_paths:
  - frontend/messages/zh-CN.json
summary: "将侧边栏 'API Keys' 中文标签改为 'API 密钥'，统一本地化"
---

## 背景

- 侧边栏 nav.apiKeys 在中文环境仍显示英文 “API Keys”。

## 变更

- zh-CN 文案 `nav.apiKeys` 从 “API Keys” 改为 “API 密钥”。

## 结果

- 中文界面侧边栏显示 “API 密钥”，与其他中文文案一致。
