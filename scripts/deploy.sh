#!/usr/bin/env bash
# 서버에서 전체를 다시 빌드하고 올린다.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  echo ".env 파일이 없습니다. .env.example 을 복사해서 DB_PASSWORD 를 넣으세요."
  exit 1
fi

docker compose up -d --build
docker compose ps
