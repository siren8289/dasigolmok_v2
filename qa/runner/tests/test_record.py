"""기록기 누적과 미실행 섹션 생략을 pytest로 확인한다."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from record import CaseResult, allocate_run_id, read_tsv, write_run

SECTION = "DE05_결측치이상치"
AREA = "단위·통합 테스트"
DAY = "2026-11-02"


def _case(tc_id: str, status: str = "PASS", section: str = SECTION, area: str = AREA) -> CaseResult:
    return CaseResult(
        tc_id=tc_id,
        feature="기록기",
        test_type="unit",
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
        area=area,
        section=section,
    )


def test_appends_and_skips_unrun_section(tmp_path: Path) -> None:
    when = datetime(2026, 11, 2, 12, 0, tzinfo=ZoneInfo("Asia/Seoul"))
    meta = tmp_path / "reports"
    first = allocate_run_id(tmp_path, when)
    write_run(tmp_path, meta, first, when, "abc", [_case("TC-A")], [])
    skipped = _case("TC-SKIP", "NOT_RUN", section="FE01_공통라우팅", area="웹·API 테스트")
    skipped.tool_a_result = "NOT_RUN"
    skipped.tool_b_result = "NOT_RUN"
    second = allocate_run_id(tmp_path, when)
    write_run(tmp_path, meta, second, when, "def", [_case("TC-B", "FAIL"), skipped], [])
    folder = tmp_path / AREA / SECTION / DAY
    rows = read_tsv(folder / "summary.tsv")
    assert [row["TC_ID"] for row in rows] == ["TC-A", "TC-B"]
    assert rows[0]["최종상태"] == "PASS"
    assert rows[1]["최종상태"] == "FAIL"
    assert first in (folder / "pass.md").read_text(encoding="utf-8")
    assert not (tmp_path / "웹·API 테스트" / "FE01_공통라우팅").exists()
    raw = (folder / "summary.tsv").read_bytes()
    assert raw.startswith(b"\xef\xbb\xbf")
    assert (folder / "테스트_시트.xlsx").exists()
