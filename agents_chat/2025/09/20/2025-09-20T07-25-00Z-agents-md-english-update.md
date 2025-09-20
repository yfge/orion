---
id: 2025-09-20T07-25-00Z-agents-md-english-update
date: 2025-09-20T07:25:00Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [docs, process]
related_paths:
  - AGENTS.md
summary: "Rewrite AI logging policy in AGENTS.md back to English while enforcing strict naming and content requirements."
---

User original prompt and requirements
- “agents.md 是不是写英文更好？ 你现在写了什么 ？ 改回英文”。

Background and goals
- Keep AGENTS.md as the English source-of-truth while retaining the stricter agents_chat policy (naming, required sections, frequency, privacy).

Changes
- Updated the “AI session logging (agents_chat)” section to English.
- Preserved enforced rules: timestamped file naming, required frontmatter, mandatory “user original prompt & requirements”, and per-commit logging.

Outcome and impact
- Contributors now see the policy in English while continuing to follow the stronger logging conventions.

Next steps (TODO)
- Optionally add `AGENTS.zh-CN.md` as a mirrored Chinese version.
