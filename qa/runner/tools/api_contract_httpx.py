#!/usr/bin/env python3
"""FastAPI 계약을 httpx/TestClient로 검증한다 (web_api 1차)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "ai"))


def main() -> int:
    try:
        from fastapi.testclient import TestClient
        from src.main import app
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "ERROR", "detail": str(exc)}, ensure_ascii=False))
        return 2
    client = TestClient(app)
    checks = []
    health = client.get("/health")
    checks.append({"name": "health", "status": health.status_code, "body": health.json() if health.status_code == 200 else health.text})
    options = client.get("/api/v1/options")
    body = options.json() if options.status_code == 200 else {}
    checks.append(
        {
            "name": "options",
            "status": options.status_code,
            "keys": sorted(body.keys()) if isinstance(body, dict) else [],
        }
    )
    ok = (
        health.status_code == 200
        and isinstance(health.json(), dict)
        and health.json().get("status") == "ok"
        and options.status_code == 200
        and isinstance(body, dict)
        and {"districts", "dongs", "industries"}.issubset(body.keys())
    )
    print(json.dumps({"status": "PASS" if ok else "FAIL", "checks": checks}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
