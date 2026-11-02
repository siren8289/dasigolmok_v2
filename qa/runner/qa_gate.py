"""QA·Security 게이트.

변경 영향에 해당하는 검사를 서로 다른 도구 두 개로 실행하고
qa/{영역}/{섹션}/{YYYY-MM-DD}/ 에 누적 기록한다.

실행하지 않은 섹션은 폴더를 만들지 않고, 실행하지 않은 검사를 PASS로 적지 않는다.
HIGH/CRITICAL OPEN 위험이 있으면 종료 코드 1이다.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = Path(__file__).resolve().parent
sys.path.insert(0, str(RUNNER))

from areas import CHECK_TO_SECTION  # noqa: E402
from record import (  # noqa: E402
    CaseResult,
    RiskItem,
    allocate_run_id,
    combine_status,
    now_seoul,
    open_blocking_risks,
    write_run,
)
from tree_hash import working_tree_token  # noqa: E402

PY = sys.executable
CI_CHECKS = ("record", "security", "front", "python", "java", "regression")


def run_cmd(args: list[str], cwd: Path, timeout: int = 600) -> tuple[str, str]:
    try:
        completed = subprocess.run(
            args,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        output = ((exc.stdout or "") + "\n" + (exc.stderr or ""))[-2500:]
        return "ERROR", f"timeout {timeout}s {output}"
    except OSError as exc:
        return "ERROR", str(exc)
    output = (completed.stdout + "\n" + completed.stderr).strip()
    status = "PASS" if completed.returncode == 0 else "FAIL"
    return status, output[-2500:]


def git_commit() -> str:
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (subprocess.CalledProcessError, OSError):
        return "UNKNOWN"
    dirty = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()
    return f"{sha}-dirty" if dirty else sha


def ensure_bandit() -> tuple[str, str]:
    status, output = run_cmd([PY, "-m", "bandit", "--version"], ROOT, timeout=60)
    if status == "PASS":
        return status, output
    installed, log = run_cmd([PY, "-m", "pip", "install", "bandit"], ROOT, timeout=180)
    if installed != "PASS":
        return "ERROR", log
    return run_cmd([PY, "-m", "bandit", "--version"], ROOT, timeout=60)


def _case(
    check: str,
    tc_id: str,
    feature: str,
    test_type: str,
    purpose: str,
    tool_a: str,
    command_a: str,
    result_a: str,
    output_a: str,
    tool_b: str,
    command_b: str,
    result_b: str,
    output_b: str,
    expected: str,
    risks: list[RiskItem] | None = None,
) -> CaseResult:
    final = combine_status(result_a, result_b)
    evidence = f"A[{result_a}] {output_a[-500:]} || B[{result_b}] {output_b[-500:]}"
    area, section = CHECK_TO_SECTION[check]
    case = CaseResult(
        tc_id=tc_id,
        feature=feature,
        test_type=test_type,
        purpose=purpose,
        tool_a=tool_a,
        tool_a_command=command_a,
        tool_a_result=result_a,
        tool_b=tool_b,
        tool_b_command=command_b,
        tool_b_result=result_b,
        final_status=final,
        expected=expected,
        actual=f"A={result_a}, B={result_b}, final={final}",
        evidence=evidence,
        area=area,
        section=section,
        repro=command_a,
        error_message=output_a if result_a != "PASS" else output_b if result_b != "PASS" else "",
        cause="도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다." if final != "PASS" else "",
    )
    if risks:
        for item in risks:
            item.area = area
            item.section = section
        case.risk_id = ",".join(item.risk_id for item in risks)
    return case


def check_record() -> tuple[CaseResult, list[RiskItem]]:
    command_a = f"{PY} -m pytest qa/runner/tests/test_record.py -q"
    command_b = f"{PY} qa/runner/tools/check_record.py"
    result_a, output_a = run_cmd([PY, "-m", "pytest", "qa/runner/tests/test_record.py", "-q"], ROOT, 120)
    result_b, output_b = run_cmd([PY, "qa/runner/tools/check_record.py"], ROOT, 60)
    case = _case(
        "record",
        "TC-UNIT-RECORD-001",
        "QA 기록기",
        "unit",
        "같은 날짜의 이전 RUN을 유지하고 미실행 섹션 폴더를 만들지 않는지 확인",
        "pytest",
        command_a,
        result_a,
        output_a,
        "python",
        command_b,
        result_b,
        output_b,
        "두 실행기 모두 누적 기록 검사를 통과",
    )
    return case, []


def _spawn(args: list[str], cwd: Path, timeout: int) -> tuple[subprocess.CompletedProcess[str] | None, str]:
    try:
        completed = subprocess.run(
            args,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        output = ((exc.stdout or "") + "\n" + (exc.stderr or ""))[-1500:]
        return None, f"timeout {timeout}s {output}"
    except OSError as exc:
        return None, str(exc)
    return completed, ""


def check_security(run_id: str) -> tuple[CaseResult, list[RiskItem]]:
    ready, ready_log = ensure_bandit()
    command_a = f"{PY} -m bandit -r ai/src data/etl -f json -q --severity-level medium"
    command_b = f"{PY} qa/runner/tools/secret_scan.py {ROOT}"
    risks: list[RiskItem] = []
    bandit_args = [PY, "-m", "bandit", "-r", "ai/src", "data/etl", "-f", "json", "-q", "--severity-level", "medium"]
    if ready != "PASS":
        result_a, output_a = "ERROR", ready_log
    else:
        completed, spawn_error = _spawn(bandit_args, ROOT, 180)
        if completed is None:
            result_a, output_a = "ERROR", spawn_error
        else:
            try:
                payload = json.loads(completed.stdout or "")
            except json.JSONDecodeError:
                result_a = "ERROR"
                output_a = (completed.stderr or completed.stdout or "bandit JSON 없음")[-1500:]
            else:
                findings = payload.get("results") or []
                if not isinstance(findings, list):
                    result_a = "ERROR"
                    output_a = "bandit results가 목록이 아니다"
                else:
                    highs = 0
                    for index, item in enumerate(findings, start=1):
                        severity = str(item.get("issue_severity", "LOW")).upper()
                        if severity in {"HIGH", "CRITICAL"}:
                            highs += 1
                        mapped = severity if severity in {"CRITICAL", "HIGH", "MEDIUM", "LOW"} else "MEDIUM"
                        risks.append(
                            RiskItem(
                                risk_id=f"{run_id}-BANDIT-{index}",
                                severity=mapped,
                                likelihood="중간",
                                impact="보안 결함이 배포되면 데이터나 인증이 노출될 수 있다.",
                                summary=f"{item.get('test_id')} {item.get('issue_text')}",
                                recommendation="해당 줄을 확인하고, 고치면 risk-register.tsv 상태를 MITIGATED로 바꾼다. 행은 삭제하지 않는다.",
                                feature="Python 보안",
                                test_type="security",
                                tc_id="TC-SEC-001",
                                file=str(item.get("filename") or "UNKNOWN"),
                                line=str(item.get("line_number") or "UNKNOWN"),
                                function=str(item.get("test_name") or "UNKNOWN"),
                            )
                        )
                    if completed.returncode not in {0, 1}:
                        result_a = "ERROR"
                    elif highs:
                        result_a = "FAIL"
                    else:
                        result_a = "PASS"
                    output_a = f"bandit findings={len(findings)} high={highs} exit={completed.returncode}"
    scan, spawn_error = _spawn([PY, "qa/runner/tools/secret_scan.py", str(ROOT)], ROOT, 120)
    if scan is None:
        result_b, output_b = "ERROR", spawn_error
    else:
        try:
            secret_findings = json.loads(scan.stdout or "")
        except json.JSONDecodeError:
            secret_findings = []
            result_b = "ERROR"
            output_b = (scan.stderr or scan.stdout or "secret_scan JSON 없음")[-1500:]
        else:
            if not isinstance(secret_findings, list):
                result_b = "ERROR"
                output_b = "secret_scan 결과가 목록이 아니다"
            else:
                blocking = [item for item in secret_findings if item.get("severity") in {"HIGH", "CRITICAL"}]
                if scan.returncode not in {0, 1}:
                    result_b = "ERROR"
                elif blocking:
                    result_b = "FAIL"
                else:
                    result_b = "PASS"
                output_b = f"secret findings={len(secret_findings)} blocking={len(blocking)} exit={scan.returncode}"
                for index, item in enumerate(secret_findings, start=1):
                    severity = item.get("severity") or "MEDIUM"
                    if severity not in {"CRITICAL", "HIGH", "MEDIUM", "LOW"}:
                        severity = "MEDIUM"
                    risks.append(
                        RiskItem(
                            risk_id=f"{run_id}-SECRET-{index}",
                            severity=severity,
                            likelihood="중간" if severity in {"HIGH", "CRITICAL"} else "낮음",
                            impact=item.get("label") or "UNKNOWN",
                            summary=f"{item.get('label')}: {item.get('excerpt')}",
                            recommendation="비밀은 환경변수로 옮기고, HTML 삽입은 이스케이프된 텍스트로 바꾼다.",
                            feature="비밀·렌더링",
                            test_type="security",
                            tc_id="TC-SEC-001",
                            file=item.get("file") or "UNKNOWN",
                            line=str(item.get("line") or "UNKNOWN"),
                            function=item.get("function") or "UNKNOWN",
                        )
                    )
    case = _case(
        "security",
        "TC-SEC-001",
        "정적 보안",
        "security",
        "ISTQB 예외·OWASP ASVS 비밀관리와 출력 이스케이프를 두 정적 도구로 확인",
        "bandit",
        command_a,
        result_a,
        output_a,
        "secret_scan",
        command_b,
        result_b,
        output_b,
        "HIGH/CRITICAL 비밀·취약점 없음",
        risks,
    )
    if case.final_status != "PASS" and risks:
        case.file = risks[0].file
        case.line = risks[0].line
        case.function = risks[0].function
    return case, risks


def check_front() -> tuple[CaseResult, list[RiskItem]]:
    command_a = "npm test"
    command_b = "npx tsc --noEmit --pretty false"
    result_a, output_a = run_cmd(["npm", "test"], ROOT / "front", 300)
    result_b, output_b = run_cmd(["npx", "tsc", "--noEmit", "--pretty", "false"], ROOT / "front", 180)
    case = _case(
        "front",
        "TC-UNIT-FRONT-001",
        "프론트 단위·타입",
        "unit",
        "라우팅·입력·결과·추천·API 클라이언트 테스트와 TypeScript 검사를 교차",
        "vitest",
        command_a,
        result_a,
        output_a,
        "tsc",
        command_b,
        result_b,
        output_b,
        "vitest 통과이고 tsc --noEmit 오류 없음",
    )
    risks: list[RiskItem] = []
    if result_b != "PASS":
        file_path, line_no = "UNKNOWN", "UNKNOWN"
        summary = "tsc --noEmit 실패"
        for line in output_b.splitlines():
            if "error TS" not in line or "(" not in line:
                continue
            head, _, rest = line.partition("(")
            parsed = rest.split(",", 1)[0]
            if not parsed.isdigit():
                continue
            file_path = head.strip()
            if file_path and not file_path.startswith("front/"):
                file_path = f"front/{file_path}"
            line_no = parsed
            summary = line.strip()
            break
        risks.append(
            RiskItem(
                risk_id="FRONT-TSC",
                severity="MEDIUM",
                likelihood="높음",
                impact="타입 오류가 있으면 빌드 스크립트 tsc --noEmit이 배포를 막거나, 검사를 빼면 타입 회귀가 남는다.",
                summary=summary,
                recommendation="node 타입 선언을 테스트 범위에 포함하고 tsc를 다시 실행한다.",
                feature="프론트 타입",
                test_type="unit",
                tc_id="TC-UNIT-FRONT-001",
                file=file_path,
                line=line_no,
                function="UNKNOWN",
                area=case.area,
                section=case.section,
            )
        )
        case.file = file_path
        case.line = line_no
        case.risk_id = risks[0].risk_id
    return case, risks


def check_python() -> tuple[CaseResult, list[RiskItem]]:
    command_a = f"{PY} -m pytest data/tests -q"
    command_b = f"{PY} qa/runner/tools/regression_oracle.py"
    result_a, output_a = run_cmd([PY, "-m", "pytest", "data/tests", "-q"], ROOT, 180)
    result_b, output_b = run_cmd([PY, "qa/runner/tools/regression_oracle.py"], ROOT, 120)
    case = _case(
        "python",
        "TC-UNIT-PY-001",
        "ETL 전처리",
        "unit",
        "정상값·빈 값·예외 문자·NULL과 매출 단위 변환을 pytest와 독립 오라클로 교차",
        "pytest",
        command_a,
        result_a,
        output_a,
        "regression_oracle",
        command_b,
        result_b,
        output_b,
        "pytest data/tests 통과이고 오라클 경계값 통과",
    )
    return case, []


def check_java() -> tuple[CaseResult, list[RiskItem]]:
    command_a = "./gradlew test --console=plain"
    command_b = f"{PY} qa/runner/tools/junit_audit.py {ROOT}"
    result_a, output_a = run_cmd(["./gradlew", "test", "--console=plain"], ROOT / "back", 600)
    result_b, output_b = run_cmd([PY, "qa/runner/tools/junit_audit.py", str(ROOT)], ROOT, 60)
    case = _case(
        "java",
        "TC-UNIT-JAVA-001",
        "Spring 진단·추천",
        "unit",
        "JUnit 실행과 XML 재집계로 실패가 숨지 않는지 확인",
        "gradle",
        command_a,
        result_a,
        output_a,
        "junit_audit",
        command_b,
        result_b,
        output_b,
        "Gradle test 종료 0이고 JUnit XML 실패 0",
    )
    return case, []


def check_regression() -> tuple[CaseResult, list[RiskItem]]:
    command_a = f"{PY} -m pytest qa/automation/de/test_de05.py -q"
    command_b = f"{PY} qa/runner/tools/regression_oracle.py"
    result_a, output_a = run_cmd(
        [PY, "-m", "pytest", "qa/automation/de/test_de05.py", "-q"], ROOT, 180
    )
    result_b, output_b = run_cmd([PY, "qa/runner/tools/regression_oracle.py"], ROOT, 120)
    case = _case(
        "regression",
        "TC-REG-DE05-001",
        "결측·이상치 회귀",
        "regression",
        "기존 DE05 경계 테스트와 독립 오라클이 서로 맞는지 확인",
        "pytest",
        command_a,
        result_a,
        output_a,
        "regression_oracle",
        command_b,
        result_b,
        output_b,
        "DE05 pytest와 오라클이 모두 통과",
    )
    return case, []


CHECKS = {
    "record": check_record,
    "security": None,
    "front": check_front,
    "python": check_python,
    "java": check_java,
    "regression": check_regression,
}


def selected_checks(scope: str, only: str) -> list[str]:
    if only:
        names = [item.strip() for item in only.split(",") if item.strip()]
        unknown = [item for item in names if item not in CHECKS]
        if unknown:
            raise SystemExit(f"unknown check {unknown}")
        return names
    if scope == "ci":
        return list(CI_CHECKS)
    if scope == "auto":
        from tree_hash import changed_paths

        changed = changed_paths(ROOT)
        if not changed:
            return ["security"]

        def touched(*prefixes: str) -> bool:
            return any(path == prefix or path.startswith(prefix) for path in changed for prefix in prefixes)

        names = ["security"]
        if touched("qa/runner/"):
            names.append("record")
        if touched("front/"):
            names.append("front")
        if touched("data/", "qa/runner/"):
            names.extend(["python", "regression"])
        if touched("back/"):
            names.append("java")
        return list(dict.fromkeys(names))
    raise SystemExit(f"unknown scope {scope}")


def assign_risk_ids(run_id: str, risks: list[RiskItem]) -> None:
    for index, item in enumerate(risks, start=1):
        item.risk_id = f"RISK-{run_id}-{index}"


def write_stamp(run_id: str, exit_code: int) -> None:
    meta = ROOT / "qa" / "reports"
    meta.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_id": run_id,
        "exit_code": exit_code,
        "tree_token": working_tree_token(ROOT),
        "recorded_at": now_seoul().isoformat(),
    }
    (meta / ".gate-stamp.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="dasiGolmok QA gate")
    parser.add_argument("--scope", choices=("ci", "auto"), default="auto")
    parser.add_argument("--only", default="", help="record,security,front,python,java,regression")
    args = parser.parse_args()
    names = selected_checks(args.scope, args.only)
    when = now_seoul()
    qa_root = ROOT / "qa"
    meta = qa_root / "reports"
    meta.mkdir(parents=True, exist_ok=True)
    run_id = allocate_run_id(qa_root, when)
    commit = git_commit()
    cases: list[CaseResult] = []
    risks: list[RiskItem] = []
    for name in names:
        if name == "security":
            case, found = check_security(run_id)
        else:
            case, found = CHECKS[name]()
        cases.append(case)
        risks.extend(found)
    assign_risk_ids(run_id, risks)
    for case in cases:
        linked = [item.risk_id for item in risks if item.tc_id == case.tc_id]
        if linked:
            case.risk_id = ",".join(linked)
    written = write_run(qa_root, meta, run_id, when, commit, cases, risks)
    blocking = open_blocking_risks(meta)
    failed = [case for case in cases if case.final_status != "PASS"]
    exit_code = 1 if failed or blocking else 0
    write_stamp(run_id, exit_code)
    print(f"RUN_ID {run_id}")
    print(f"folders {', '.join(written) or '-'}")
    for case in cases:
        print(f"{case.final_status} {case.tc_id} A={case.tool_a_result} B={case.tool_b_result}")
    print(f"open HIGH/CRITICAL {len(blocking)}")
    for row in blocking:
        print(f"RISK {row.get('risk_id')} {row.get('severity')} {row.get('file')}:{row.get('line')} {row.get('summary')}")
    print("GATE " + ("FAIL" if exit_code else "PASS"))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
