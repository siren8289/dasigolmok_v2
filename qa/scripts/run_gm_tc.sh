#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export QA_BASE_URL="${QA_BASE_URL:-http://localhost:8080/api/v1}"
export PGPASSWORD="${DB_PASSWORD:-app_password}"
export PGUSER="${DB_USERNAME:-app_user}"
export PGDATABASE="${DB_NAME:-dasi_golmok}"
export PGHOST="${DB_HOST:-localhost}"
python3 "$ROOT/scripts/run_gm_tc.py"
