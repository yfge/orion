# AGENTS Guidance for Orion (Source of Truth)

This file is the single source of truth for all agent/coding assistants collaborating in this repository.

Agent files policy
- Do not duplicate instructions across agent-specific files.
- The following files must be symlinks to this file: `.CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.github/instructions/agents.instructions.md`.
- Precedence of instructions: system/developer > user > this file > anything else.

Goals
- Orion is a notification gateway: decouple business systems from external channels; ensure reliability, observability, and operability.
- Demonstrate ai-coding & vibe coding with a documentation-first, auditable engineering process.

Backend architecture (FastAPI, Python 3.11)
- Suggested layout:
  - `backend/app/main.py`: FastAPI app entry, router mount, DI bootstrap.
  - `backend/app/core/`: config, logging, constants, errors, rate/retry policies.
  - `backend/app/api/`: API layer (versioned: `v1`/`v2`).
  - `backend/app/domain/`: domain models and use cases (application services).
  - `backend/app/adapters/`: channel adapters (Feishu, WeCom, WeChat, Email, SMS).
  - `backend/app/repository/`: repository ports and implementations (SQLAlchemy).
  - `backend/app/schemas/`: Pydantic schemas (request/response/config).
  - `backend/app/services/`: orchestration, gateway service, templates, routing policies.
  - `backend/alembic/`: DB migrations.
  - `backend/tasks/`: async jobs (Celery/RQ/APScheduler) and retry/backoff.
- Dependency injection: define stable ports; inject implementations via factory/provider/container; keep adapters swappable.
- State model: persist full notification lifecycle (pending/sending/success/failed/retrying/abandoned) with auditable events.
- Resilience: idempotency keys, exponential backoff, rate limiting, circuit breakers; differentiate vendor 4xx vs 5xx.

Frontend (Next.js + Tailwind + ShadCN)
- Layout suggestion: `frontend/app/`, `frontend/components/`, `frontend/lib/` (API SDK/utils).
- Features: channel configuration, templates, send history and search, alerts, retries.

Documentation workflow
- Start with an architecture overview under `docs/architecture/`.
- Add module design docs as `README.md` in each module folder.
- Implementations must follow docs; if intent changes, update docs first.
- Save AI collaboration logs to `agents_chat/` (see below) for traceability.

Coding style and tooling
- Python: ruff (lint) + black (format) + isort (imports, profile=black). Prefer full typing. Separate Pydantic vs ORM models.
- Frontend: prettier + eslint (configure later).
- Run pre-commit before pushing. Use Conventional Commits.

Commits and branches
- Examples: `feat(adapter): add feishu message sender`, `fix(api): correct webhook signature validation`, `chore: bump pre-commit hooks`.
- Branching (suggested): protected `main`; feature branches `feat/*`, fixes `fix/*`; merge via CI.

Security and secrets
- Never commit secrets or tokens. Use environment variables or a secret manager.

AI session logging (agents_chat)
- Purpose: persist ai-coding & vibe coding conversations for audit, recall, and knowledge capture.
- Root: `agents_chat/`. Organize by date (year/month/day).
- Filename: `agents_chat/YYYY/MM/DD/<timestamp>-<short-topic>.md`.
- YAML frontmatter (recommended):
  ```yaml
  ---
  id: 2024-09-01T10-23-45Z-orion-scope
  date: 2024-09-01T10:23:45Z
  participants: [human, orion-assistant]
  models: [gpt-4o, claude, gemini]
  tags: [design, backend, docs]
  related_paths:
    - backend/
    - docs/architecture/
  summary: "Initial architecture and directory conventions"
  ---
  ```
- Body suggestions:
  - Short summary (what, why, outcome, TODOs).
  - Key decisions and rationale; link PRs/commits.
  - No sensitive data; redact tokens and secrets.
- Frequency: create an entry for each major milestone/decision; long sessions split by day.
- Versioning: keep under Git; consider periodic archival for large logs.
