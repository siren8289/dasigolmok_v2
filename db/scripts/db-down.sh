#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../back"
docker compose down
echo "PostgreSQL stopped."
