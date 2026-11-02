#!/usr/bin/env python3
"""docker compose 설정·healthcheck 존재 여부를 검증한다 (infra 1차)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    compose = ROOT / "compose.yaml"
    if not compose.exists():
        print(json.dumps({"status": "FAIL", "detail": "compose.yaml missing"}, ensure_ascii=False))
        return 1
    env = os.environ.copy()
    # 로컬 .env 없이도 config 파싱이 되도록 더미 값 주입 (실제 비밀 아님)
    env.setdefault("DB_PASSWORD", "qa-compose-check-dummy")
    env.setdefault("GEMINI_API_KEY", "")
    completed = subprocess.run(
        ["docker", "compose", "-f", str(compose), "config"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    if completed.returncode != 0:
        print(json.dumps({"status": "FAIL", "detail": (completed.stderr or completed.stdout)[-1500:]}, ensure_ascii=False))
        return 1
    text = compose.read_text(encoding="utf-8")
    required = ["healthcheck:", "services:", "db:", "ai:", "back:"]
    missing = [item for item in required if item not in text]
    ok = not missing
    print(
        json.dumps(
            {
                "status": "PASS" if ok else "FAIL",
                "missing": missing,
                "compose_config_exit": completed.returncode,
            },
            ensure_ascii=False,
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
