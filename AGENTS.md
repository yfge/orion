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

Repository layout
- Root directories (current):
  - `backend/` — FastAPI app, SQLAlchemy, Alembic, tests.
  - `frontend/` — Next.js app with Tailwind + ShadCN.
  - `docs/` — documentation and guides.
  - `Docker/` — containerization setup.
  - `scripts/` — local helper scripts (e.g., migrations).
  - `agents_chat/` — AI collaboration logs (see policy below).
  - Symlinked agent rule files → `AGENTS.md`: `.CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `.github/instructions/agents.instructions.md`.

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
- Commit messages MUST be in English and follow Conventional Commits.
  - Style: imperative mood, present tense, concise; max 72-char subject.
  - Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`, `ci`, etc.
  - Scope: use meaningful scopes (e.g., `backend`, `frontend`, `agents`, `records`).
  - Examples: `feat(adapter): add Feishu message sender`, `fix(api): validate X-API-Key in notify`, `docs(readme): update Notify API usage`, `chore(precommit): bump hook versions`.
- Branching (suggested): protected `main`; feature branches `feat/*`, fixes `fix/*`; merge via CI.

Security and secrets
- Never commit secrets or tokens. Use environment variables or a secret manager.

AI session logging (agents_chat)
- Importance: This is a vibe-coding project. Agents chat logs are core materials for review and learning; they must be complete, traceable, and reproducible.
- Directory: Root `agents_chat/`, organized by date folders: `agents_chat/YYYY/MM/DD/`.
- Filename (REQUIRED): `YYYY-MM-DDTHH-MM-SSZ-<topic>.md` (e.g., `2025-09-19T07-30-03Z-backend-systems-api.md`).
- YAML frontmatter (REQUIRED):
  ```yaml
  ---
  id: 2025-09-19T07-30-03Z-backend-systems-api
  date: 2025-09-19T07:30:03Z
  participants: [human, orion-assistant]
  models: [gpt-4o]
  tags: [backend, api]
  related_paths:
    - backend/app/api/v1/systems.py
  summary: "Implement business systems API and tests"
  ---
  ```
- Body (REQUIRED sections):
  - User original prompt and requirements: paste or summarize the user’s original instruction and goals (redact sensitive bits when necessary).
  - Background and goals: why we do this, and what to achieve.
  - Changes: what changed (files/modules/endpoints), key decisions and trade-offs.
  - Outcome and impact: feature/API/tests/docs status and usability.
  - Next steps (TODO): follow-ups, risks, validation points.
  - Linked commits/PRs: list commit messages or PR links when available.
- Frequency: Every significant commit (or small group of related commits) MUST be paired with an agents_chat entry; split long sessions by day. Trivial formatting-only commits can be batched under the nearest related entry.
- Language: Chinese is preferred for this repo; English mirror optional. Consistency matters more than perfection.
- Privacy: never include secrets; always redact tokens/keys.

CI enforcement (agents_chat coupling)
- For commits that modify application code (paths: `backend/`, `frontend/`, `Docker/`, or `docker-compose.yml`), the same commit MUST also include at least one file under `agents_chat/` describing the change.
- Allowed exceptions (must be intentional): add `skip agents-chat` in the commit body to bypass the check (use sparingly, e.g., merges, hotfix quick-follow, or pure CI/build refactors).
- The GitHub Actions workflow runs `tools/ci/check-agents-chat.js` on PRs and pushes to enforce this rule.
