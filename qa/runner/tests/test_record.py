"""기록기 누적과 미실행 폴더 생략을 pytest로 확인한다."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from record import CaseResult, allocate_run_id, read_tsv, write_run


def _case(tc_id: str, status: str = "PASS", test_type: str = "unit") -> CaseResult:
    return CaseResult(
        tc_id=tc_id,
        feature="기록기",
        test_type=test_type,
        purpose="누적 기록",
        tool_a="pytest",
        tool_a_command="pytest qa/runner/tests/test_record.py",
        tool_a_result=status,
        tool_b="python",
        tool_b_command="python qa/runner/tools/check_record.py",
        tool_b_result=status,
        final_status=status,
        expected="이전 RUN이 남는다",
        actual=status,
        evidence="pytest",
    )


def test_appends_and_skips_unrun_type(tmp_path: Path) -> None:
    when = datetime(2026, 11, 2, 12, 0, tzinfo=ZoneInfo("Asia/Seoul"))
    first = allocate_run_id(tmp_path, when)
    write_run(tmp_path, first, when, "abc", [_case("TC-A")], [])
    skipped = _case("TC-SKIP", "NOT_RUN", "e2e")
    skipped.tool_a_result = "NOT_RUN"
    skipped.tool_b_result = "NOT_RUN"
    second = allocate_run_id(tmp_path, when)
    write_run(tmp_path, second, when, "def", [_case("TC-B", "FAIL"), skipped], [])
    rows = read_tsv(tmp_path / "unit" / "2026-11-02" / "results.tsv")
    assert [row["RUN_ID"] for row in rows] == [first, second]
    assert [row["TC_ID"] for row in rows] == ["TC-A", "TC-B"]
    assert rows[0]["final_status"] == "PASS"
    assert rows[1]["final_status"] == "FAIL"
    assert first in (tmp_path / "unit" / "2026-11-02" / "pass.md").read_text(encoding="utf-8")
    assert not (tmp_path / "e2e").exists()
    raw = (tmp_path / "unit" / "2026-11-02" / "results.tsv").read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf")
