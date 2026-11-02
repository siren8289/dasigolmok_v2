"""pytest 결과(PASS/FAIL/skipped)를 QA 결과 JSON으로 남긴다."""
import json
import os
import sys
from pathlib import Path

os.environ["GEMINI_API_KEY"] = ""
sys.path.insert(0, str(Path(__file__).resolve().parent))

RESULTS = {}
FAILS = {}

SPEC_DIR = Path(__file__).resolve().parents[2] / "_meta" / "sections"
OUT_PATH = Path(__file__).resolve().parents[1] / "results" / "AI.json"
COMMAND = (
    "cd /Users/jeong-yelim/orca/dasigolmok_v2/ai && "
    "/tmp/qa-venv/bin/python -m pytest ../qa/automation/ai "
    "--rootdir=. --override-ini='testpaths=' -q --tb=line"
)


def pytest_runtest_logreport(report):
    name = report.nodeid.split("::")[-1]
    if not name.startswith("test_AI"):
        return
    case_id = name[len("test_") :].replace("_", "-", 1)
    if report.when == "call" or (report.when == "setup" and report.failed):
        RESULTS[case_id] = report.outcome
    if report.failed:
        FAILS[case_id] = str(report.longrepr)[-300:]


def _spec_ids():
    ids = []
    for path in sorted(SPEC_DIR.glob("AI0*.json")):
        ids.extend(item["id"] for item in json.loads(path.read_text(encoding="utf-8")))
    return ids


def pytest_sessionfinish(session, exitstatus):
    from helpers import EVIDENCE

    cases = []
    for case_id in _spec_ids():
        outcome = RESULTS.get(case_id)
        if outcome == "passed":
            status = "PASS"
        elif outcome == "failed":
            status = "FAIL"
        else:
            status = "RISK"
        evidence = EVIDENCE.get(case_id) or FAILS.get(case_id) or ""
        if not evidence:
            evidence = "RISK: 테스트가 수집·실행되지 않음" if outcome is None else outcome
        if status == "RISK" and outcome == "skipped" and not evidence.startswith("RISK:"):
            evidence = "RISK: " + evidence
        cases.append(
            {
                "id": case_id,
                "status": status,
                "evidence": str(evidence)[:400],
                "defect_id": f"DEF-{case_id}" if status == "FAIL" else "",
            }
        )
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps({"command": COMMAND, "cases": cases}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
