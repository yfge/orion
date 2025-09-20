---
id: 2025-09-20T07-55-00Z-rewrite-commit-messages-en
date: 2025-09-20T07:55:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [git, process]
related_paths:
  - .git/
  - AGENTS.md
summary: "Rewrite previous non-English commit messages to English using git filter-branch to comply with the updated policy."
---

User original prompt and requirements
- “使用git 命令调整之前commit message 为英文”。

Background and goals
- Enforce the policy that all commit messages must be in English (Conventional Commits).

Changes
- Used `git filter-branch --msg-filter` to rewrite specific commit messages:
  - chore(agents): unify agents_chat naming to YYYY-MM-DDTHH-MM-SSZ and record the change (was Chinese)
  - docs(agents): add Chinese record for RJSF integration (was Chinese)
- Local branch history has been rewritten; commit SHAs have changed from those points onward.

Outcome and impact
- Local history now complies with English commit message policy.
- If a remote branch exists, a force push is required to update remote: `git push --force-with-lease`.

Next steps (TODO)
- Optionally add commitlint CI to prevent future non-English messages.
