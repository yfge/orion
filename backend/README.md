# Orion Backend (FastAPI)

Requires Python 3.11. Recommended to use the conda env named `py311`.

Quickstart
- Activate env: `conda activate py311`
- Install deps (choose one):
  - From repo root: `pip install -e backend`
  - Or inside backend: `cd backend && pip install -e .`
- Run dev server: `cd backend && uvicorn app.main:app --reload`
- Check: GET `http://127.0.0.1:8000/healthz` → `{ "status": "ok" }`

Alembic
- Config: `backend/alembic.ini`, scripts in `backend/alembic/`
- Generate revision: `alembic -c backend/alembic.ini revision -m "init"`
- Upgrade: `alembic -c backend/alembic.ini upgrade head`

Config
- Edit `.env` at repo root or environment variables with prefix `ORION_`.
- Key vars: `ORION_DATABASE_URL` (default `sqlite:///./orion.db`).
- MySQL example:
  - URL: `mysql+pymysql://user:password@localhost:3306/orion?charset=utf8mb4`
  - Driver: PyMySQL (already included). `pool_pre_ping` is enabled to avoid stale connections.
