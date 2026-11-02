#!/usr/bin/env python3
"""OpenAPI(Schemathesis) ASGI 검증 — web_api 2차 (httpx TestClient와 다른 엔진).

무거운 uvicorn 기동 대신 FastAPI OpenAPI 스키마로 /health·/api/v1/options를 검증한다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "ai"))


def main() -> int:
    try:
        import schemathesis
        from src.main import app
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "ERROR", "detail": str(exc)}, ensure_ascii=False))
        return 2

    try:
        schema = schemathesis.openapi.from_asgi("/openapi.json", app)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "ERROR", "detail": f"openapi load failed: {exc}"}, ensure_ascii=False))
        return 2

    checked = []
    failures = []
    for path, method in (("/health", "get"), ("/api/v1/options", "get")):
        try:
            operation = schema[path][method]
            case = operation.Case()
            response = case.call()
            case.validate_response(response)
            checked.append({"path": path, "status": getattr(response, "status_code", "UNKNOWN")})
        except Exception as exc:  # noqa: BLE001
            failures.append({"path": path, "error": str(exc)[:300]})

    ok = bool(checked) and not failures
    print(
        json.dumps(
            {
                "status": "PASS" if ok else "FAIL",
                "checked": checked,
                "failures": failures,
                "engine": "schemathesis",
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
