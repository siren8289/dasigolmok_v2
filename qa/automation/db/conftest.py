"""DB01–DB03 실행 결과를 qa/automation/results/DB.json 에 남긴다."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "qa" / "automation" / "results" / "DB.json"
SECTIONS = {
    "DB01": "DB01_진단영속성",
    "DB02": "DB02_SQL마이그레이션",
    "DB03": "DB03_pgvector전용",
}
EXPECTED = [f"DB0{n}-{i:03d}" for n, last in ((1, 20), (2, 24), (3, 19)) for i in range(1, last + 1)]

ROWS: dict[str, dict] = {}


def _case_id(nodeid: str) -> str | None:
    name = nodeid.split("::")[-1]
    if not name.startswith("test_DB"):
        return None
    return name[len("test_") :].replace("_", "-", 1)


def _text(report) -> str:
    raw = getattr(report, "longreprtext", "") or str(report.longrepr)
    return " ".join(raw.split())[-900:]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    cid = _case_id(item.nodeid)
    if cid is None or report.when == "teardown":
        return
    if report.when == "setup" and report.passed:
        return
    if report.passed:
        status = "PASS"
    elif report.skipped:
        status = "RISK"
    else:
        status = "FAIL"
    found = [value for key, value in item.user_properties if key == "evidence"]
    evidence = str(found[-1]) if found else _text(report)
    ROWS[cid] = {
        "id": cid,
        "section": SECTIONS[cid.split("-")[0]],
        "status": status,
        "evidence": evidence or "증적 없음",
        "defect_id": f"DEF-{cid}" if status == "FAIL" else "",
    }


def pytest_sessionfinish(session, exitstatus):
    for cid in EXPECTED:
        ROWS.setdefault(
            cid,
            {
                "id": cid,
                "section": SECTIONS[cid.split("-")[0]],
                "status": "RISK",
                "evidence": "RISK: 해당 테스트가 수집·실행되지 않았다.",
                "defect_id": "",
            },
        )
    payload = {
        "command": "/tmp/qa-venv/bin/python -m pytest qa/automation/db/test_db.py -q --tb=line",
        "cases": [ROWS[cid] for cid in EXPECTED],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _ = (session, exitstatus)
