---
id: 2025-09-19T00-00-00Z-gitignore-orion-db
date: 2025-09-19T07:51:38Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [git, ignore]
related_paths:
  - .gitignore
summary: "将本地 SQLite orion.db 加入 .gitignore，避免误提交。"
---

说明
- 本地开发使用 SQLite 时产生的 `orion.db` 属于环境工件，不应纳入版本控制；已加入 .gitignore。
