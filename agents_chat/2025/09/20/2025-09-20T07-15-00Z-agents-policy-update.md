---
id: 2025-09-20T07-15-00Z-agents-policy-update
date: 2025-09-20T07:15:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [流程, 记录, 规范]
related_paths:
  - AGENTS.md
  - agents_chat/
summary: "更新 AGENTS.md：统一 agents_chat 命名规范，并强制记录用户原始提示与要求。"
---

用户原始提示与要求
- 「修改agents.md 强调这个规范，同时在agents chat 强调要有用户的原始提示和要求！！这是一个vibe coding 项目，对于大家review和学习 agents chat 的记录非常重要！」

背景与目标
- 强化 agents_chat 的可读性、可复盘性，保障团队评审与学习。

变更内容
- 更新 `AGENTS.md` 的 AI session logging 部分：
  - 强制命名格式：`YYYY-MM-DDTHH-MM-SSZ-<topic>.md`。
  - 强制正文包含「用户原始提示与要求」。
  - 明确每个重要提交（或提交组）都要有配套 agents_chat 记录。
  - 统一中文为主。

结果与影响
- agents_chat 记录更结构化，审阅时可直接看到用户意图与最终结果，便于知识沉淀。

后续事项（TODO）
- 回溯检查历史记录是否全部符合规范；不符合的按规范补齐或更名。
- 在 PR 模板/CI 中增加检查（可选）：验证 agents_chat 是否随提交更新。

关联提交
- 本次提交：更新 AGENTS.md 并新增此条记录。
