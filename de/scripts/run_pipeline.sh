#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PGPASSWORD="${DB_PASSWORD:-app_password}"
export PGUSER="${DB_USERNAME:-app_user}"
export PGDATABASE="${DB_NAME:-dasi_golmok}"
export PGHOST="${DB_HOST:-localhost}"
export PGPORT="${DB_PORT:-5432}"
python3 -m pipeline.run
