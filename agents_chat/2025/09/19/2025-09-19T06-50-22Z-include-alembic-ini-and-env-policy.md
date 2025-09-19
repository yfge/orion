---
id: 2025-09-19T06-50-22Z-include-alembic-ini
date: 2025-09-19T06:50:22Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [db, alembic, repo, config]
related_paths:
  - backend/alembic.ini
  - .gitignore
summary: "补充提交 Alembic 配置文件；明确数据库连接应放入 .env（不纳入版本库）。"
---

动机
- 用户指出 `backend/alembic.ini` 未被提交；需纳入版本控制。
- 数据库连接必须放在 `.env` 中，且 `.env` 不能提交到 Git（模板 `.env.example` 保留）。

操作
- 将 `backend/alembic.ini` 加入版本库（其中未硬编码 DB URL，实际在 env.py 中从 Settings 读取）。
- 确认 `.env` 未存在亦未被跟踪；`.gitignore` 已包含 `.env` 规则。

结果
- Alembic 可直接通过 `-c backend/alembic.ini` 使用；DB URL 仍从环境变量/`.env` 加载，避免泄露。
