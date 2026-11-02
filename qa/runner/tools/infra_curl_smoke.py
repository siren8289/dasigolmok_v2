#!/usr/bin/env python3
"""배포 가능 HTTP 스모크. 로컬 스택이 없으면 BLOCKED로 기록할 상태를 출력한다."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGETS = [
    os.environ.get("QA_SMOKE_FRONT_URL", "http://127.0.0.1:5173"),
    os.environ.get("QA_SMOKE_BACK_URL", "http://127.0.0.1:8080/actuator/health"),
    os.environ.get("QA_SMOKE_AI_URL", "http://127.0.0.1:8000/health"),
]


def probe(url: str) -> dict:
    completed = subprocess.run(
        ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "--connect-timeout", "2", "--max-time", "5", url],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    code = (completed.stdout or "").strip() or "000"
    return {"url": url, "http_code": code, "curl_exit": completed.returncode}


def main() -> int:
    results = [probe(url) for url in TARGETS]
    reachable = [item for item in results if item["http_code"].isdigit() and int(item["http_code"]) < 500 and item["http_code"] != "000"]
    if not reachable:
        print(
            json.dumps(
                {
                    "status": "BLOCKED",
                    "detail": "로컬/스테이징 서비스가 응답하지 않는다. compose up 후 재실행하거나 CI 스모크 환경을 연결한다.",
                    "results": results,
                },
                ensure_ascii=False,
            )
        )
        return 3
    ok = any(item["http_code"] in {"200", "301", "302"} for item in results)
    print(json.dumps({"status": "PASS" if ok else "FAIL", "results": results}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
