"""QA 게이트 실행 결과를 날짜별 MD·TSV에 누적한다.

과거 행은 지우거나 덮어쓰지 않는다. 실행하지 않은 테스트 종류는 폴더를 만들지 않는다.
날짜와 시각은 Asia/Seoul 기준이다.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SEOUL = ZoneInfo("Asia/Seoul")
STATUSES = ("PASS", "FAIL", "BLOCKED", "ERROR", "NOT_RUN", "SKIPPED")
TSV_HEADER = [
    "RUN_ID",
    "TC_ID",
    "executed_at",
    "feature",
    "test_type",
    "tool_a",
    "tool_a_result",
    "tool_b",
    "tool_b_result",
    "final_status",
    "git_commit",
    "file",
    "function",
    "line",
    "issue_id",
    "risk_id",
    "evidence",
]
RISK_HEADER = [
    "risk_id",
    "opened_at",
    "run_id",
    "severity",
    "likelihood",
    "impact",
    "status",
    "feature",
    "test_type",
    "file",
    "function",
    "line",
    "tc_id",
    "summary",
    "recommendation",
]


@dataclass
class CaseResult:
    tc_id: str
    feature: str
    test_type: str
    purpose: str
    tool_a: str
    tool_a_command: str
    tool_a_result: str
    tool_b: str
    tool_b_command: str
    tool_b_result: str
    final_status: str
    expected: str
    actual: str
    evidence: str
    file: str = "UNKNOWN"
    function: str = "UNKNOWN"
    line: str = "UNKNOWN"
    issue_id: str = ""
    risk_id: str = ""
    input_value: str = ""
    error_message: str = ""
    repro: str = ""
    cause: str = ""
    fix_location: str = ""
    recheck: str = ""

    def __post_init__(self) -> None:
        if self.final_status not in STATUSES:
            raise ValueError(f"bad status {self.final_status}")
        for name in ("tool_a_result", "tool_b_result"):
            if getattr(self, name) not in STATUSES:
                raise ValueError(f"bad {name}")


@dataclass
class RiskItem:
    risk_id: str
    severity: str
    likelihood: str
    impact: str
    summary: str
    recommendation: str
    feature: str
    test_type: str
    tc_id: str = ""
    status: str = "OPEN"
    file: str = "UNKNOWN"
    function: str = "UNKNOWN"
    line: str = "UNKNOWN"
    fingerprint: str = ""
    extra: dict = field(default_factory=dict)


def now_seoul() -> datetime:
    return datetime.now(SEOUL)


def flatten(value: object) -> str:
    return " ".join(str(value or "").replace("\t", " ").split())


def combine_status(left: str, right: str) -> str:
    """두 도구 결과 중 더 나쁜 상태를 최종 상태로 쓴다. PASS는 둘 다 PASS일 때만."""
    rank = {"ERROR": 5, "FAIL": 4, "BLOCKED": 3, "NOT_RUN": 2, "SKIPPED": 1, "PASS": 0}
    if left not in rank or right not in rank:
        return "ERROR"
    return left if rank[left] >= rank[right] else right


def _existing_run_ids(reports: Path) -> set[str]:
    found: set[str] = set()
    if not reports.exists():
        return found
    for path in reports.glob("*/*/results.tsv"):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row in reader:
                if row.get("RUN_ID"):
                    found.add(row["RUN_ID"])
    return found


def allocate_run_id(reports: Path, when: datetime | None = None) -> str:
    when = when or now_seoul()
    base = when.strftime("%Y%m%d-%H%M%S")
    used = _existing_run_ids(reports)
    if base not in used:
        return base
    index = 2
    while f"{base}-{index}" in used:
        index += 1
    return f"{base}-{index}"


def _append_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        if new_file:
            handle.write("\ufeff")
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(header)
        else:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow([flatten(cell) for cell in row])


def _append_md(path: Path, title: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"# {title}\n\n{block}", encoding="utf-8")
        return
    existing = path.read_text(encoding="utf-8")
    if not existing.endswith("\n"):
        existing += "\n"
    path.write_text(existing + "\n" + block, encoding="utf-8")


def _case_bullets(case: CaseResult, when: str, commit: str) -> list[str]:
    lines = [
        f"### {case.tc_id} {case.feature}",
        "",
        f"- 실행 시각: {when}",
        f"- Git Commit: {commit or 'UNKNOWN'}",
        f"- 테스트 종류: {case.test_type}",
        f"- 검증 목적: {case.purpose}",
        f"- 도구 A: {case.tool_a} / 결과 {case.tool_a_result}",
        f"- 도구 A 명령: `{case.tool_a_command}`",
        f"- 도구 B: {case.tool_b} / 결과 {case.tool_b_result}",
        f"- 도구 B 명령: `{case.tool_b_command}`",
        f"- 최종 상태: {case.final_status}",
        f"- 기대 결과: {case.expected}",
        f"- 실제 결과: {case.actual}",
        f"- 근거: {case.evidence}",
        f"- 파일: {case.file}",
        f"- 함수: {case.function}",
        f"- 줄 번호: {case.line}",
        f"- ISSUE_ID: {case.issue_id or '-'}",
        f"- RISK_ID: {case.risk_id or '-'}",
    ]
    return lines


def _fail_block(case: CaseResult, when: str, commit: str) -> str:
    lines = _case_bullets(case, when, commit)
    lines.extend(
        [
            f"- 입력값: {case.input_value or '-'}",
            f"- 오류 메시지: {case.error_message or '-'}",
            f"- 재현 방법: {case.repro or case.tool_a_command}",
            f"- 원인 분석: {case.cause or '-'}",
            f"- 수정 코드 위치: {case.fix_location or '아직 수정하지 않음'}",
            f"- 재검증: {case.recheck or '아직 재검증하지 않음'}",
        ]
    )
    return "\n".join(lines) + "\n"


def _risk_fingerprint(item: RiskItem) -> str:
    if item.fingerprint:
        return item.fingerprint
    return "|".join(
        [
            item.severity,
            item.file,
            item.line,
            flatten(item.summary)[:160],
        ]
    )


def load_risk_register(reports: Path) -> list[dict[str, str]]:
    path = reports / "risk-register.tsv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def open_blocking_risks(reports: Path) -> list[dict[str, str]]:
    return [
        row
        for row in load_risk_register(reports)
        if row.get("status") == "OPEN" and row.get("severity") in {"HIGH", "CRITICAL"}
    ]


def write_run(
    reports: Path,
    run_id: str,
    when: datetime,
    commit: str,
    cases: list[CaseResult],
    risks: list[RiskItem],
) -> list[str]:
    """실행된 종류만 날짜 폴더에 누적한다. 만든 종류 목록을 반환한다."""
    stamp = when.strftime("%Y-%m-%dT%H:%M:%S%z")
    day = when.strftime("%Y-%m-%d")
    written: list[str] = []
    by_type: dict[str, list[CaseResult]] = {}
    for case in cases:
        if case.final_status == "NOT_RUN" and case.tool_a_result == "NOT_RUN":
            continue
        by_type.setdefault(case.test_type, []).append(case)

    for test_type, typed in by_type.items():
        folder = reports / test_type / day
        folder.mkdir(parents=True, exist_ok=True)
        passed = [case for case in typed if case.final_status == "PASS"]
        failed = [case for case in typed if case.final_status in {"FAIL", "ERROR", "BLOCKED"}]
        typed_risks = [item for item in risks if item.test_type == test_type]
        run_heading = f"## {run_id}\n\n- 실행 시각: {stamp}\n- Git Commit: {commit or 'UNKNOWN'}\n"

        if passed:
            body = run_heading + "\n".join("\n".join(_case_bullets(case, stamp, commit)) for case in passed) + "\n"
        else:
            body = run_heading + "이 RUN에서 PASS는 없다.\n"
        _append_md(folder / "pass.md", "PASS", body)

        if failed:
            body = run_heading + "\n".join(_fail_block(case, stamp, commit) for case in failed)
        else:
            body = run_heading + "이 RUN에서 FAIL, ERROR, BLOCKED는 없다.\n"
        _append_md(folder / "fail.md", "FAIL", body)

        if typed_risks:
            chunks = [run_heading.rstrip(), ""]
            for item in typed_risks:
                chunks.extend(
                    [
                        f"### {item.risk_id} {item.severity} {item.status}",
                        "",
                        f"- 기능: {item.feature}",
                        f"- 관련 TC_ID: {item.tc_id or '-'}",
                        f"- 발생 가능성: {item.likelihood}",
                        f"- 영향: {item.impact}",
                        f"- 내용: {item.summary}",
                        f"- 권장 조치: {item.recommendation}",
                        f"- 처리 상태: {item.status}",
                        f"- 파일: {item.file}",
                        f"- 함수: {item.function}",
                        f"- 줄 번호: {item.line}",
                        "",
                    ]
                )
            _append_md(folder / "risk.md", "RISK", "\n".join(chunks))
        else:
            _append_md(folder / "risk.md", "RISK", run_heading + "이 RUN에서 새 위험은 없다.\n")

        _append_tsv(
            folder / "results.tsv",
            TSV_HEADER,
            [
                [
                    run_id,
                    case.tc_id,
                    stamp,
                    case.feature,
                    case.test_type,
                    case.tool_a,
                    case.tool_a_result,
                    case.tool_b,
                    case.tool_b_result,
                    case.final_status,
                    commit or "UNKNOWN",
                    case.file,
                    case.function,
                    case.line,
                    case.issue_id,
                    case.risk_id,
                    case.evidence,
                ]
                for case in typed
            ],
        )
        written.append(test_type)

    fresh_risks = _new_risks(reports, risks)
    if fresh_risks:
        _append_tsv(
            reports / "risk-register.tsv",
            RISK_HEADER,
            [
                [
                    item.risk_id,
                    stamp,
                    run_id,
                    item.severity,
                    item.likelihood,
                    item.impact,
                    item.status,
                    item.feature,
                    item.test_type,
                    item.file,
                    item.function,
                    item.line,
                    item.tc_id,
                    item.summary,
                    item.recommendation,
                ]
                for item in fresh_risks
            ],
        )
    return written


def _new_risks(reports: Path, risks: list[RiskItem]) -> list[RiskItem]:
    seen = {flatten(row.get("summary", "")) + "|" + row.get("file", "") + "|" + row.get("line", "") + "|" + row.get("severity", "") for row in load_risk_register(reports)}
    fresh: list[RiskItem] = []
    for item in risks:
        key = flatten(item.summary) + "|" + item.file + "|" + item.line + "|" + item.severity
        if key in seen:
            continue
        seen.add(key)
        fresh.append(item)
    return fresh


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8-sig")
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))
