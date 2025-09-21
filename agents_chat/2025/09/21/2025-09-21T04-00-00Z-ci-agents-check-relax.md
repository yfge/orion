---
id: 2025-09-21T04-00-00Z-ci-agents-check-relax
date: 2025-09-21T04:00:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [ci, agents_chat]
related_paths:
  - tools/ci/check-agents-chat.js
  - .github/workflows/commitlint.yml
  - AGENTS.md
summary: "Relax agents_chat CI to check only commits after introduction and narrow code-touch paths"
---

User original prompt and requirements

- CI 报错：历史多笔提交未包含 agents_chat。希望调整规则，避免对历史记录造成失败，同时保留对新提交的强约束。

Background and goals

- 我们已在 CI 加入 agents_chat 耦合检查，但 push 时会检查最近 N 条提交，包含历史提交，导致失败。

Changes

- `tools/ci/check-agents-chat.js`：
  - 仅对在该脚本引入之后的提交生效（通过 `git merge-base --is-ancestor <since> <commit>` 判断）。
  - 将“代码改动”范围收窄到 `backend/app/`、`frontend/app/`、`frontend/lib/`、`Docker/`、`docker-compose.yml`，避免 tests/docs-only 触发。
- `AGENTS.md`：文档化上述范围与“自引入日之后才生效”的说明。

Outcome and impact

- 现有主分支历史不会再触发失败；新提交仍需在同一提交包含 agents_chat，流程可执行。

Next steps (TODO)

- 持续观察 CI 噪音；必要时进一步白名单某些目录或对“chore/ci/build-only”类别自动放行。
