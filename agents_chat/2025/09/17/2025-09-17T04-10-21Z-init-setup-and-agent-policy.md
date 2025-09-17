---
id: 2025-09-17T04-10-21Z-orion-init
date: 2025-09-17T04:10:21Z
participants: [human, orion-assistant]
models: [gpt-4o]
tags: [init, docs, scaffolding, policy]
related_paths:
  - README.md
  - AGENTS.md
  - .gitignore
  - .pre-commit-config.yaml
  - backend/
  - frontend/
  - Docker/
  - .CLAUDE.md
  - GEMINI.md
  - .cursorrules
  - .github/instructions/agents.instructions.md
  - agents_chat/
summary: "Initialize scaffolding; unify agent rules via AGENTS.md; symlink agent files; add session logging conventions."
---

Outcome
- Added initial scaffolding (README, AGENTS, gitignore, pre-commit) and root folders (backend, frontend, Docker).
- Consolidated all agent instructions into AGENTS.md (English) as the single source of truth.
- Replaced agent-specific files with symlinks to AGENTS.md.
- Established AI session logging conventions under agents_chat/ and added this entry.

Key decisions
- Use FastAPI (Python 3.11) + Alembic for backend; Next.js + Tailwind + ShadCN for frontend.
- Enforce DI and adapter interfaces to decouple vendor APIs.
- Save significant AI collaboration sessions to agents_chat/ using date-based structure and YAML frontmatter.
- Keep Conventional Commits and pre-commit hooks (ruff, black, isort, prettier).

Files changed (high-level)
- README.md: project overview; ai-coding & vibe coding context; agent file symlink note; session logging section.
- AGENTS.md: English source of truth; architecture, process, style, and session logging rules.
- .gitignore, .pre-commit-config.yaml: base tooling.
- backend/, frontend/, Docker/: placeholders with .gitkeep.
- .CLAUDE.md, GEMINI.md, .cursorrules, .github/instructions/agents.instructions.md: symlinks to AGENTS.md.
- agents_chat/: created with .gitkeep and this summary.

Next steps
- Add architecture overview under docs/architecture/.
- Scaffold backend FastAPI app and Alembic setup.
- Decide task runner (Celery/RQ/APScheduler) and retry strategy.
- Plan frontend console MVP (channels, templates, records).
