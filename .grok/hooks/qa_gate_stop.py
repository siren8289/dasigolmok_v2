#!/usr/bin/env python3
"""감시 중인 변경이 마지막 QA 게이트 스탬프와 다르면 종료를 막는다.

러너가 없거나 임포트에 실패하면 종료를 막지 않는다.
실패로 끝난 게이트도 스탬프를 남기므로, 그 기록을 보고한 뒤 종료할 수 있다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "qa" / "runner"


def allow() -> int:
    print("{}")
    return 0


def main() -> int:
    try:
        sys.stdin.read()
    except OSError:
        pass
    if not (RUNNER / "tree_hash.py").is_file():
        return allow()
    sys.path.insert(0, str(RUNNER))
    try:
        from tree_hash import working_tree_token
    except Exception:
        return allow()
    try:
        token = working_tree_token(ROOT)
    except Exception:
        return allow()
    if token is None:
        return allow()
    stamp_path = ROOT / "qa" / "reports" / ".gate-stamp.json"
    try:
        stamp = json.loads(stamp_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        stamp = {}
    if stamp.get("tree_token") == token:
        return allow()
    print(
        json.dumps(
            {
                "decision": "block",
                "reason": (
                    "감시 중인 파일이 마지막 QA 게이트 이후 바뀌었다. "
                    "저장소 루트에서 python qa/runner/qa_gate.py --scope auto 를 실행하고, "
                    "RUN_ID와 qa/results/{area}/{section}/{date}의 FAIL, OPEN HIGH/CRITICAL을 보고한 뒤 종료한다. "
                    "실행하지 않은 검사는 PASS가 아니다."
                ),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
