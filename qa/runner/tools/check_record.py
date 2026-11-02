"""pytest 없이 기록기가 같은 날짜의 이전 RUN을 보존하는지 확인한다."""

from __future__ import annotations

import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from record import CaseResult, allocate_run_id, read_tsv, write_run


def _case(tc_id: str, status: str = "PASS") -> CaseResult:
    return CaseResult(
        tc_id=tc_id,
        feature="기록기",
        test_type="unit",
        purpose="누적 기록",
        tool_a="python",
        tool_a_command="python qa/runner/tools/check_record.py",
        tool_a_result=status,
        tool_b="pytest",
        tool_b_command="pytest qa/runner/tests/test_record.py",
        tool_b_result=status,
        final_status=status,
        expected="이전 RUN이 남는다",
        actual="두 RUN",
        evidence="append",
    )


def main() -> int:
    when = datetime(2026, 11, 2, 12, 0, tzinfo=ZoneInfo("Asia/Seoul"))
    with tempfile.TemporaryDirectory() as tmp:
        reports = Path(tmp)
        first = allocate_run_id(reports, when)
        write_run(reports, first, when, "abc", [_case("TC-A")], [])
        second = allocate_run_id(reports, when)
        if second == first:
            print("FAIL run id collision")
            return 1
        write_run(reports, second, when, "abc", [_case("TC-B", "FAIL")], [])
        rows = read_tsv(reports / "unit" / "2026-11-02" / "results.tsv")
        ids = [row["RUN_ID"] for row in rows]
        if ids != [first, second]:
            print("FAIL history overwritten", ids)
            return 1
        text = (reports / "unit" / "2026-11-02" / "pass.md").read_text(encoding="utf-8")
        if first not in text or "TC-A" not in text:
            print("FAIL pass.md lost the first run")
            return 1
        if (reports / "e2e").exists():
            print("FAIL unrun type folder created")
            return 1
    print("check_record PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
