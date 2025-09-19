#!/usr/bin/env bash
set -euo pipefail

# Orion DB migration helper
# - Loads ORION_DATABASE_URL from environment or .env
# - Uses Alembic config at backend/alembic.ini

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Load .env if ORION_DATABASE_URL not provided
if [[ -z "${ORION_DATABASE_URL:-}" ]] && [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if ! command -v alembic >/dev/null 2>&1; then
  echo "alembic not found. Activate env and install deps, e.g.:" >&2
  echo "  conda activate py311 && pip install -e backend" >&2
  exit 1
fi

CONF="backend/alembic.ini"

cmd="${1:-upgrade}"
shift || true

case "$cmd" in
  upgrade|downgrade|current|history|stamp)
    exec alembic -c "$CONF" "$cmd" "$@"
    ;;
  revision)
    exec alembic -c "$CONF" revision "$@"
    ;;
  *)
    cat >&2 <<USAGE
Usage: ${0##*/} <command> [args]

Commands:
  upgrade [REV]     Upgrade to revision (default: head)
  downgrade [REV]   Downgrade to revision
  revision -m MSG   Create a new revision
  current           Show current revision
  history           Show revision history
  stamp [REV]       Set a revision without running migrations

Examples:
  ORION_DATABASE_URL=mysql+pymysql://root:pass@127.0.0.1:13306/orion?charset=utf8mb4 \
    ${0##*/} upgrade head

  ${0##*/} revision -m "add notifications table"
USAGE
    exit 2
    ;;
esac

