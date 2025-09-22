#!/usr/bin/env bash
set -euo pipefail

# Compile PO files into MO for runtime.

ROOT_DIR=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT_DIR"

pybabel compile -d backend/locale -D orion

echo "Compiled translations to MO files"
