#!/usr/bin/env bash
# Rebuild everything downstream of data/atlas.csv:
#   1. validate atlas.csv against the schema
#   2. regenerate data/atlas.xlsx
#   3. publish a copy of atlas.csv into docs/ for the dashboard
#
# Usage: scripts/build.sh   (run from repo root; uses .venv if present)
set -euo pipefail
cd "$(dirname "$0")/.."

PY=python3
[ -x ".venv/bin/python" ] && PY=".venv/bin/python"

echo "==> validating schema"
"$PY" scripts/04_validate_schema.py

echo "==> building data/atlas.xlsx"
"$PY" scripts/03_build_xlsx.py

echo "==> publishing docs/atlas.csv"
cp data/atlas.csv docs/atlas.csv

echo "==> done"
