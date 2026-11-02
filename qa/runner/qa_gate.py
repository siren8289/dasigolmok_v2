"""QA·Security 게이트.

변경 영향에 해당하는 검사를 서로 다른 도구 두 개로 실행하고
qa/results/{area}/{section}/{YYYY-MM-DD}/ 에 누적 기록한다.

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
CI_CHECKS = ("record", "security", "front", "python", "java", "regression", "web_api", "infra")


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
    if completed.returncode == 0:
        status = "PASS"
    elif completed.returncode == 3:
        status = "BLOCKED"
    elif completed.returncode == 2:
        status = "ERROR"
    else:
        status = "FAIL"
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
    command_a = f"{PY} qa/runner/tools/semgrep_scan.py"
    command_b = f"{PY} qa/runner/tools/secret_scan.py {ROOT}"
    risks: list[RiskItem] = [
        RiskItem(
            risk_id=f"{run_id}-CODEQL-LOCAL",
            severity="MEDIUM",
            likelihood="중간",
            impact="로컬 게이트에는 CodeQL CLI가 없어 CI codeql 잡이 2차 엔진 역할을 한다.",
            summary="CodeQL은 GitHub Actions에서 실행한다. 로컬은 Semgrep+secret_scan으로 교차한다.",
            recommendation="PR에서 codeql 잡 PASS를 필수 상태로 유지한다.",
            feature="CodeQL CI",
            test_type="security",
            tc_id="TC-SEC-001",
            file=".github/workflows/qa-gate.yml",
            line="UNKNOWN",
            function="codeql",
        )
    ]
    result_a, output_a = run_cmd([PY, "qa/runner/tools/semgrep_scan.py"], ROOT, 300)
    result_b, output_b = run_cmd([PY, "qa/runner/tools/secret_scan.py", str(ROOT)], ROOT, 120)
    if result_b == "PASS":
        # secret_scan prints JSON list; non-zero already mapped
        try:
            payload = json.loads(output_b.split("\n")[0]) if output_b.strip().startswith("[") else json.loads(output_b)
            if isinstance(payload, list):
                blocking = [item for item in payload if item.get("severity") in {"HIGH", "CRITICAL"}]
                if blocking:
                    result_b = "FAIL"
                    for index, item in enumerate(blocking, start=1):
                        risks.append(
                            RiskItem(
                                risk_id=f"{run_id}-SECRET-{index}",
                                severity=item.get("severity") or "HIGH",
                                likelihood="중간",
                                impact=item.get("label") or "secret",
                                summary=f"{item.get('label')}: {item.get('excerpt')}",
                                recommendation="비밀은 환경변수로 옮긴다.",
                                feature="비밀·렌더링",
                                test_type="security",
                                tc_id="TC-SEC-001",
                                file=item.get("file") or "UNKNOWN",
                                line=str(item.get("line") or "UNKNOWN"),
                            )
                        )
        except json.JSONDecodeError:
            pass
    case = _case(
        "security",
        "TC-SEC-001",
        "정적 보안",
        "security",
        "Semgrep OWASP 규칙과 비밀·렌더링 스캔으로 교차 검증. CodeQL은 CI에서 실행",
        "semgrep",
        command_a,
        result_a,
        output_a,
        "secret_scan",
        command_b,
        result_b,
        output_b,
        "HIGH/CRITICAL 소견 없음 + CI CodeQL 필수",
        risks,
    )
    return case, risks


def check_web_api() -> tuple[CaseResult, list[RiskItem]]:
    command_a = f"{PY} qa/runner/tools/api_contract_httpx.py"
    command_b = f"{PY} qa/runner/tools/api_smoke_curl.py"
    result_a, output_a = run_cmd([PY, "qa/runner/tools/api_contract_httpx.py"], ROOT, 120)
    result_b, output_b = run_cmd([PY, "qa/runner/tools/api_smoke_curl.py"], ROOT, 180)
    risks: list[RiskItem] = [
        RiskItem(
            risk_id="WEB-PLAYWRIGHT-PENDING",
            severity="MEDIUM",
            likelihood="중간",
            impact="브라우저 E2E가 없으면 UI 사용 흐름 회귀가 남을 수 있다.",
            summary="Playwright UI E2E는 아직 없다. API는 httpx TestClient와 Schemathesis(OpenAPI)로 교차한다.",
            recommendation="front에 Playwright를 추가해 02_web_api UI 흐름 TC를 연결한다.",
            feature="web_api 도구 확장",
            test_type="api",
            tc_id="TC-WEB-API-001",
            file="qa/config/test_map.json",
            line="UNKNOWN",
        )
    ]
    case = _case(
        "web_api",
        "TC-WEB-API-001",
        "FastAPI HTTP 계약",
        "api",
        "httpx TestClient와 Schemathesis OpenAPI ASGI로 헬스·옵션 API를 교차",
        "httpx_contract",
        command_a,
        result_a,
        output_a,
        "schemathesis",
        command_b,
        result_b,
        output_b,
        "health status=ok 이고 options에 districts/dongs/industries",
        risks,
    )
    return case, risks


def check_infra() -> tuple[CaseResult, list[RiskItem]]:
    command_a = f"{PY} qa/runner/tools/infra_compose_check.py"
    command_b = f"{PY} qa/runner/tools/infra_curl_smoke.py"
    result_a, output_a = run_cmd([PY, "qa/runner/tools/infra_compose_check.py"], ROOT, 60)
    result_b, output_b = run_cmd([PY, "qa/runner/tools/infra_curl_smoke.py"], ROOT, 60)
    risks: list[RiskItem] = []
    if result_b == "BLOCKED":
        risks.append(
            RiskItem(
                risk_id="INFRA-SMOKE-BLOCKED",
                severity="MEDIUM",
                likelihood="높음",
                impact="로컬 스택이 꺼져 있으면 배포 후 실제 HTTP 성공을 로컬에서 증명하지 못한다.",
                summary="curl 스모크가 서비스 미기동으로 BLOCKED다. compose config 검사만으로는 런타임 검증이 아니다.",
                recommendation="docker compose up 후 재실행하거나 CI/스테이징 스모크 URL을 QA_SMOKE_* 로 넣는다.",
                feature="infra smoke",
                test_type="infra",
                tc_id="TC-INFRA-001",
                file="compose.yaml",
            )
        )
    case = _case(
        "infra",
        "TC-INFRA-001",
        "Compose·HTTP 스모크",
        "infra",
        "docker compose config/healthcheck와 curl HTTP 스모크 교차",
        "compose_config",
        command_a,
        result_a,
        output_a,
        "curl_health",
        command_b,
        result_b,
        output_b,
        "compose config PASS 이고 최소 1개 엔드포인트 HTTP 성공",
        risks,
    )
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
    "web_api": check_web_api,
    "infra": check_infra,
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
        if touched("qa/runner/", "qa/config/", "qa-policy.md", "AGENTS.md"):
            names.append("record")
        if touched("front/"):
            names.append("front")
        if touched("data/", "qa/runner/"):
            names.extend(["python", "regression"])
        if touched("back/"):
            names.append("java")
        if touched("ai/", "front/", "back/"):
            names.append("web_api")
        if touched("compose.yaml", "scripts/", ".github/workflows/"):
            names.append("infra")
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
    parser.add_argument("--only", default="", help="record,security,front,python,java,regression,web_api,infra")
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
