#!/usr/bin/env bash
set -euo pipefail

# Update locale PO files from POT template.

ROOT_DIR=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT_DIR"

LOCALES=(zh_CN en_US)

for loc in "${LOCALES[@]}"; do
  pybabel update -i backend/locale/orion.pot -d backend/locale -D orion -l "$loc" || {
    echo "Initializing $loc"
    pybabel init -i backend/locale/orion.pot -d backend/locale -D orion -l "$loc"
  }
done

echo "Locales updated/initialized: ${LOCALES[*]}"
