#!/usr/bin/env bash
set -euo pipefail

# Extract translatable strings from backend Python/Jinja2 into POT/PO files.
# Requires: pybabel (pip install Babel)

ROOT_DIR=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT_DIR"

mkdir -p backend/locale

pybabel extract \
  -F backend/babel.cfg \
  -o backend/locale/orion.pot \
  backend/app

echo "Extracted to backend/locale/orion.pot"
