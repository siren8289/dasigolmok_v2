"""OPS/QA pytest 결과를 qa/automation/results/*.json 으로 남긴다."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

AUTOMATION = Path(__file__).resolve().parent
sys.path.insert(0, str(AUTOMATION))
from evidence import NOTES, normalize_status

RESULTS = AUTOMATION / "results"
COMMAND = (
    "/tmp/qa-venv/bin/python -m pytest "
    "qa/automation/ops/test_ops.py qa/automation/qa_docs/test_qa.py"
)
RECORDS: dict[str, dict] = {}


def _case_id(node_name: str) -> str:
    raw = node_name.removeprefix("test_")
    return raw.replace("_", "-", 1)


def _reason(report) -> str:
    longrepr = report.longrepr
    if isinstance(longrepr, tuple) and len(longrepr) >= 3:
        return str(longrepr[2])
    text = str(longrepr)
    match = re.search(r"RISK:.*", text)
    if match:
        return match.group(0).splitlines()[0]
    return text


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    case_id = _case_id(item.name)
    if report.skipped:
        status = "skipped"
    elif report.failed:
        status = "failed"
    else:
        status = "passed"
    status = normalize_status(status)
    evidence = NOTES.get(case_id) or _reason(report)
    RECORDS[case_id] = {
        "id": case_id,
        "status": status,
        "evidence": evidence.replace("\n", " ")[:400],
        "defect_id": f"DEF-{case_id}" if status == "failed" else "",
    }


def pytest_sessionfinish(session, exitstatus):
    del session, exitstatus
    # 다른 스위트가 이 conftest를 불러도 OPS/QA 결과가 없으면 결과 파일을 덮어쓰지 않는다.
    if not any(key.startswith(("OPS", "QA")) for key in RECORDS):
        return
    RESULTS.mkdir(parents=True, exist_ok=True)
    ops = [RECORDS[key] for key in sorted(RECORDS, key=_sort_key) if key.startswith("OPS")]
    qa = [RECORDS[key] for key in sorted(RECORDS, key=_sort_key) if key.startswith("QA")]
    payload = {"command": COMMAND}
    (RESULTS / "OPS.json").write_text(
        json.dumps({**payload, "cases": ops}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (RESULTS / "QA.json").write_text(
        json.dumps({**payload, "cases": qa}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _sort_key(case_id: str):
    prefix, number = case_id.split("-")
    return prefix, int(number)
