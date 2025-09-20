---
id: 2025-09-20T07-40-00Z-agents-commit-message-english
date: 2025-09-20T07:40:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [process, commits, docs]
related_paths:
  - AGENTS.md
summary: "Enforce English Conventional Commits and align AGENTS.md with current repository layout."
---

User original prompt and requirements
- 「继续更改agents 1. 根据现有目录更新 2. 强调commit message 需要使用英文」

Background and goals
- Make contribution guidelines precise and aligned with the current repo structure.
- Ensure all commit messages are in English and follow Conventional Commits for clarity and consistency.

Changes
- Added a "Repository layout" section to AGENTS.md reflecting current directories: backend, frontend, docs, Docker, scripts, agents_chat, and agent rule symlinks.
- Strengthened the "Commits and branches" section to REQUIRE English Conventional Commits with examples and style notes.
- Clarified agents_chat frequency rule: every significant commit (or grouped small commits) must have a paired log entry.

Outcome and impact
- Contributors have an accurate map of the repo and unambiguous commit message requirements.
- Reviewers benefit from consistent, scannable commit histories.

Next steps (TODO)
- Optionally add a pre-commit `commitlint` hook and CI check to enforce Conventional Commits.
