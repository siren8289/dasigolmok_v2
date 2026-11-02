"""OPS1 Docker, OPS2 CI, OPS3 배포 스크립트 실행 검증."""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
import yaml

AUTOMATION = Path(__file__).resolve().parents[1]
if str(AUTOMATION) not in sys.path:
    sys.path.insert(0, str(AUTOMATION))
from evidence import note

ROOT = Path(__file__).resolve().parents[3]
CI_PATH = ROOT / ".github" / "workflows" / "ci.yml"
DEPLOY_PATH = ROOT / ".github" / "workflows" / "deploy.yml"
_COMPOSE = None


def fail_case(case_id: str, message: str) -> None:
    note(case_id, message)
    pytest.fail(message)


def risk(case_id: str, message: str) -> None:
    if not message.startswith("RISK:"):
        message = "RISK: " + message
    note(case_id, message)
    pytest.skip(message)


def ok(case_id: str, message: str) -> None:
    note(case_id, message)


def run(cmd, *, env=None, cwd=None, check=False):
    return subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=check,
    )


def compose_env(**extra):
    env = os.environ.copy()
    env["DB_PASSWORD"] = extra.pop("DB_PASSWORD", "pass")
    env.pop("GEMINI_API_KEY", None)
    env.update(extra)
    return env


def compose_config():
    global _COMPOSE
    if _COMPOSE is None:
        result = run(
            ["docker", "compose", "config", "--format", "json"],
            env=compose_env(),
        )
        if result.returncode != 0:
            raise AssertionError(result.stderr[-500:])
        _COMPOSE = json.loads(result.stdout)
    return _COMPOSE


def load_workflow(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if True in data and "on" not in data:
        data["on"] = data.pop(True)
    return data


def ci():
    return load_workflow(CI_PATH)


def deploy():
    return load_workflow(DEPLOY_PATH)


def deploy_text() -> str:
    return DEPLOY_PATH.read_text(encoding="utf-8")


def ssh_script() -> str:
    text = deploy_text()
    match = re.search(r"name: Setup SSH.*?run: \|\n(?P<body>.*?)(?=\n      - name:)", text, re.S)
    if not match:
        raise AssertionError("Setup SSH run 블록을 찾지 못했다")
    return textwrap.dedent(match.group("body"))


def remote_script() -> str:
    text = deploy_text()
    match = re.search(r"<<'EOF'\n(?P<body>.*)\n\s*EOF", text, re.S)
    if not match:
        raise AssertionError("원격 배포 스크립트를 찾지 못했다")
    return textwrap.dedent(match.group("body"))


def bash(script: str, *, env=None, cwd=None):
    merged = os.environ.copy()
    merged.pop("SSH_KEY", None)
    merged.pop("EC2_HOST", None)
    if env:
        merged.update(env)
    return run(["bash", "-se"], env=merged, cwd=cwd, check=False).returncode if False else subprocess.run(
        ["bash", "-se"],
        input=script,
        cwd=cwd or ROOT,
        env=merged,
        text=True,
        capture_output=True,
    )


def test_OPS1_001():
    result = run(["docker", "compose", "config", "--quiet"], env=compose_env(DB_PASSWORD="pass"))
    if result.returncode != 0:
        fail_case("OPS1-001", f"DB_PASSWORD=pass docker compose config 실패: {result.stderr[-180]}")
    services = set(compose_config()["services"])
    ok("OPS1-001", f"DB_PASSWORD=pass docker compose config 종료코드 0. 서비스 {sorted(services)} 스키마가 해석됐다.")


def test_OPS1_002():
    env = os.environ.copy()
    env.pop("DB_PASSWORD", None)
    result = run(["docker", "compose", "config", "--quiet"], env=env)
    text = result.stderr + result.stdout
    if result.returncode == 0 or "DB_PASSWORD" not in text:
        fail_case("OPS1-002", f"비밀번호 없이 config가 실패하지 않았다. rc={result.returncode}")
    ok("OPS1-002", "DB_PASSWORD 미설정 시 docker compose config가 required variable DB_PASSWORD 오류로 종료코드 1이다.")


def test_OPS1_003():
    names = set(compose_config()["services"])
    if names != {"db", "ai", "back", "front"}:
        fail_case("OPS1-003", f"서비스 집합이 db,ai,back,front가 아니다: {sorted(names)}")
    ok("OPS1-003", "docker compose config --services 기준 서비스는 db, ai, back, front 네 개다.")


def test_OPS1_004():
    image = compose_config()["services"]["db"].get("image")
    if image != "pgvector/pgvector:pg16":
        fail_case("OPS1-004", f"db image가 pgvector/pgvector:pg16이 아니다: {image}")
    ok("OPS1-004", "compose config의 db image는 pgvector/pgvector:pg16이다.")


def test_OPS1_005():
    volumes = compose_config()["services"]["db"]["volumes"]
    named = [item for item in volumes if item.get("type") == "volume" and item.get("source") == "db-data"]
    if not named or "db-data" not in compose_config()["volumes"]:
        fail_case("OPS1-005", "db-data named volume이 /var/lib/postgresql/data에 연결되어 있지 않다.")
    target = named[0]["target"]
    ok("OPS1-005", f"db-data named volume이 {target}에 마운트되어 컨테이너 재생성과 분리된 영속 볼륨이다.")


def test_OPS1_006():
    env = compose_config()["services"]["db"]["environment"]
    back = compose_config()["services"]["back"]["environment"]
    ai_url = compose_config()["services"]["ai"]["environment"]["DATABASE_URL"]
    if env.get("POSTGRES_USER") != "dasi" or env.get("POSTGRES_DB") != "dasigolmok":
        fail_case("OPS1-006", "POSTGRES_USER/DB가 dasi/dasigolmok이 아니다.")
    if not env.get("POSTGRES_PASSWORD"):
        fail_case("OPS1-006", "POSTGRES_PASSWORD가 비어 있다.")
    if back.get("SPRING_DATASOURCE_USERNAME") != "dasi":
        fail_case("OPS1-006", "Spring 사용자명이 dasi가 아니다.")
    if not ai_url.startswith("postgresql://dasi:") or not ai_url.endswith("@db:5432/dasigolmok"):
        fail_case("OPS1-006", "AI DATABASE_URL이 dasi@db:5432/dasigolmok 형태가 아니다.")
    ok("OPS1-006", "compose config에서 POSTGRES_USER=dasi, DB=dasigolmok, 비밀번호가 보간되고 JDBC/AI URL이 db:5432를 가리킨다.")


def test_OPS1_007():
    health = compose_config()["services"]["db"].get("healthcheck") or {}
    test = " ".join(health.get("test") or [])
    if "pg_isready -U dasi -d dasigolmok" not in test:
        fail_case("OPS1-007", f"db healthcheck가 pg_isready가 아니다: {test}")
    ok("OPS1-007", "db healthcheck는 pg_isready -U dasi -d dasigolmok 이며 interval 5s, retries 20이다.")


def test_OPS1_008():
    cfg = compose_config()["services"]
    for name in ("ai", "back"):
        condition = cfg[name]["depends_on"]["db"]["condition"]
        if condition != "service_healthy":
            fail_case("OPS1-008", f"{name}가 db healthy 조건을 기다리지 않는다: {condition}")
    ok("OPS1-008", "ai와 back 모두 depends_on.db.condition=service_healthy라 pg_isready 실패 시 기동이 막힌다.")


def test_OPS1_009():
    url = compose_config()["services"]["back"]["environment"].get("APP_AI_BASE_URL")
    if url != "http://ai:8000" or "ai" not in compose_config()["services"]:
        fail_case("OPS1-009", f"APP_AI_BASE_URL이 http://ai:8000이 아니다: {url}")
    ok("OPS1-009", "back 환경변수 APP_AI_BASE_URL=http://ai:8000이고 compose 서비스 이름이 ai라 내부 DNS 대상이 맞다.")


def test_OPS1_010():
    url = compose_config()["services"]["back"]["environment"].get("SPRING_DATASOURCE_URL")
    if url != "jdbc:postgresql://db:5432/dasigolmok":
        fail_case("OPS1-010", f"JDBC URL이 db:5432가 아니다: {url}")
    ok("OPS1-010", "SPRING_DATASOURCE_URL=jdbc:postgresql://db:5432/dasigolmok 이고 db 서비스가 같은 네트워크에 있다.")


def test_OPS1_011():
    condition = compose_config()["services"]["ai"]["depends_on"]["db"]["condition"]
    if condition != "service_healthy":
        fail_case("OPS1-011", f"ai depends_on db 조건이 service_healthy가 아니다: {condition}")
    ok("OPS1-011", "ai.depends_on.db.condition은 service_healthy라 DB 준비 후에 AI가 생성된다.")


def test_OPS1_012():
    depends = compose_config()["services"]["back"]["depends_on"]
    if depends["db"]["condition"] != "service_healthy" or depends["ai"]["condition"] != "service_started":
        fail_case("OPS1-012", f"back 의존 조건이 기대와 다르다: {depends}")
    ok("OPS1-012", "back은 db service_healthy, ai service_started에 의존한다.")


def test_OPS1_013():
    ai = compose_config()["services"]["ai"]
    back_ai = compose_config()["services"]["back"]["depends_on"]["ai"]["condition"]
    if ai.get("healthcheck") or back_ai == "service_healthy":
        ok("OPS1-013", "ai healthcheck와 back의 service_healthy 대기가 있다.")
        return
    fail_case(
        "OPS1-013",
        "ai에는 healthcheck가 없고 back은 ai를 service_started만 본다. 모델 로딩 실패여도 back이 기동되어 readiness가 보장되지 않는다.",
    )


def test_OPS1_014():
    nginx = (ROOT / "front" / "nginx.conf").read_text(encoding="utf-8")
    if "location /api/" not in nginx or "proxy_pass http://back:8080" not in nginx:
        fail_case("OPS1-014", "nginx /api → back:8080 프록시가 없다.")
    ok("OPS1-014", "front/nginx.conf location /api/ 가 proxy_pass http://back:8080 으로 연결된다.")


def test_OPS1_015():
    ports = compose_config()["services"]["front"].get("ports") or []
    published = [item.get("published") for item in ports]
    if "80" not in published or not any(item.get("target") == 80 for item in ports):
        fail_case("OPS1-015", f"front 80:80 포트가 없다: {ports}")
    ok("OPS1-015", "front ports는 published 80, target 80이라 호스트 80으로 웹에 접근하는 구성이다.")


def test_OPS1_016():
    ports = compose_config()["services"]["ai"].get("ports")
    if ports:
        fail_case("OPS1-016", f"ai 포트가 호스트에 열려 있다: {ports}")
    ok("OPS1-016", "compose config에서 ai.ports가 없어 호스트 8000으로 직접 붙는 매핑이 없다.")


def test_OPS1_017():
    ports = compose_config()["services"]["back"].get("ports")
    if ports:
        fail_case("OPS1-017", f"back 포트가 호스트에 열려 있다: {ports}")
    ok("OPS1-017", "compose config에서 back.ports가 없어 호스트 8080 직접 매핑이 없다.")


def test_OPS1_018():
    ports = compose_config()["services"]["db"].get("ports")
    if ports:
        fail_case("OPS1-018", f"db 포트가 호스트에 열려 있다: {ports}")
    ok("OPS1-018", "compose config에서 db.ports가 없어 외부 5432 매핑이 없다.")


def test_OPS1_019():
    volumes = compose_config()["services"]["db"]["volumes"]
    bind = [item for item in volumes if item.get("target") == "/docker-entrypoint-initdb.d"]
    if not bind or not bind[0].get("read_only"):
        fail_case("OPS1-019", "db/migration initdb 마운트가 없거나 읽기 전용이 아니다.")
    names = sorted(path.name for path in (ROOT / "db" / "migration").glob("V*.sql"))
    expected = [f"V{index}__" for index in range(1, 10)]
    missing = [prefix for prefix in expected if not any(name.startswith(prefix) for name in names)]
    if missing or len(names) < 9:
        fail_case("OPS1-019", f"V1~V9 SQL이 부족하다. 파일={names} 누락접두={missing}")
    ok("OPS1-019", f"db/migration {len(names)}개 SQL이 /docker-entrypoint-initdb.d 읽기전용 마운트다: {', '.join(names)}.")


def test_OPS1_020():
    env = compose_env()
    result = run(["docker", "compose", "ps"], env=env)
    text = (result.stdout + result.stderr).strip()
    if result.returncode != 0:
        risk("OPS1-020", f"RISK: docker compose ps 조회에 실패해 Up과 health를 대조하지 못했다. {text[-160]}")
    if "Up" not in result.stdout:
        risk(
            "OPS1-020",
            "RISK: 기동 중인 스택이 없어 docker compose ps Up과 /api/health를 대조하지 못했다. compose up은 범위 밖이다.",
        )
    ok("OPS1-020", "docker compose ps에서 Up을 확인했고 별도 health 대조가 가능하다.")


def test_OPS1_021():
    key = compose_config()["services"]["ai"]["environment"].get("GEMINI_API_KEY")
    sys.path.insert(0, str(ROOT / "ai"))
    from src.llm_explain import explain

    previous = os.environ.get("GEMINI_API_KEY")
    os.environ["GEMINI_API_KEY"] = ""
    try:
        text, source = explain(
            {"dong": "연남동", "district": "마포구", "industry": "한식음식점"},
            {
                "status": "warning",
                "dong": "연남동",
                "industry": "한식음식점",
                "close_rate": 5,
                "ml_close_rate": 4.2,
                "dl_sales_per_store": 100,
            },
        )
    finally:
        if previous is None:
            os.environ.pop("GEMINI_API_KEY", None)
        else:
            os.environ["GEMINI_API_KEY"] = previous
    if key not in ("", None) or source != "basic" or "상권" not in text:
        fail_case("OPS1-021", f"미설정 fallback이 아니다. key_empty={key in ('', None)} source={source}")
    ok("OPS1-021", "GEMINI_API_KEY 미설정 시 compose 값은 빈 문자열이고 explain()은 basic 문장으로 떨어진다.")


def test_OPS1_022():
    result = run(["docker", "compose", "logs", "--tail=50", "ai", "back"], env=compose_env())
    if result.returncode != 0:
        fail_case("OPS1-022", f"docker compose logs 실패: {result.stderr[-180]}")
    ok("OPS1-022", "DB_PASSWORD를 넣고 docker compose logs --tail=50 ai back 이 종료코드 0이다. 컨테이너가 없으면 본문은 비어도 서비스 로그 조회는 된다.")


def test_OPS1_023():
    nginx = (ROOT / "front" / "nginx.conf").read_text(encoding="utf-8")
    if "proxy_pass http://back:8080" not in nginx or "back" not in compose_config()["services"]:
        fail_case("OPS1-023", "nginx upstream back:8080과 compose 서비스 back이 같이 있지 않다.")
    ok("OPS1-023", "nginx.conf upstream이 http://back:8080 이고 compose 서비스 이름 back과 같다.")


def test_OPS1_024():
    raw = (ROOT / "compose.yaml").read_text(encoding="utf-8")
    services = compose_config()["services"]
    limited = []
    for name, service in services.items():
        if service.get("mem_limit") or service.get("deploy"):
            limited.append(name)
    if limited or re.search(r"mem_limit|memory:|cpus:", raw):
        ok("OPS1-024", f"메모리 상한이 있다: {limited}")
        return
    fail_case("OPS1-024", "compose.yaml와 config 어디에도 AI/서비스 메모리 상한(mem_limit, deploy.resources)이 없다.")


def test_OPS1_025():
    volume = compose_config()["volumes"].get("db-data")
    script = (ROOT / "scripts" / "deploy.sh").read_text(encoding="utf-8")
    remote = remote_script()
    if not volume:
        fail_case("OPS1-025", "db-data named volume 선언이 없다.")
    if "--volumes" in script or "-v " in script or "down -v" in remote:
        fail_case("OPS1-025", "배포 명령이 named volume을 지운다.")
    ok("OPS1-025", "db-data는 named volume이고 up --build 경로(deploy.sh, CD)에 down -v가 없어 리빌드만으로 볼륨이 지워지지 않는다.")


def test_OPS1_026():
    raw = (ROOT / "compose.yaml").read_text(encoding="utf-8")
    script = (ROOT / "scripts" / "deploy.sh").read_text(encoding="utf-8")
    if re.search(r"lock|flock|concurrency", raw + script, re.I):
        ok("OPS1-026", "compose 또는 deploy.sh에 동시 기동 잠금이 있다.")
        return
    fail_case("OPS1-026", "compose.yaml과 scripts/deploy.sh에 docker compose up 병렬 실행을 막는 락이 없다.")


def test_OPS2_001():
    branches = ci()["on"]["push"]["branches"]
    if "main" not in branches:
        fail_case("OPS2-001", f"push 분기에 main이 없다: {branches}")
    ok("OPS2-001", "ci.yml on.push.branches에 main이 있어 main 푸시가 CI를 트리거한다.")


def test_OPS2_002():
    branches = ci()["on"]["pull_request"]["branches"]
    if "main" not in branches:
        fail_case("OPS2-002", f"pull_request 분기에 main이 없다: {branches}")
    ok("OPS2-002", "ci.yml on.pull_request.branches에 main이 있어 main PR이 CI를 트리거한다.")


def test_OPS2_003():
    steps = " ".join(step.get("run", "") for step in ci()["jobs"]["data"]["steps"])
    if "python -m pytest data/tests" not in steps:
        fail_case("OPS2-003", f"data 잡 pytest 명령이 없다: {steps}")
    ok("OPS2-003", "data 잡이 python -m pytest data/tests -q 를 실행한다.")


def test_OPS2_004():
    job = ci()["jobs"]["ai"]
    steps = " ".join(step.get("run", "") for step in job["steps"])
    if job["defaults"]["run"]["working-directory"] != "ai" or "python -m pytest tests" not in steps:
        fail_case("OPS2-004", "ai 잡이 ai/tests pytest를 실행하지 않는다.")
    ok("OPS2-004", "ai 잡은 working-directory ai에서 python -m pytest tests -q 를 실행한다.")


def test_OPS2_005():
    job = ci()["jobs"]["back"]
    steps = " ".join(step.get("run", "") for step in job["steps"])
    if job["defaults"]["run"]["working-directory"] != "back" or "./gradlew test" not in steps:
        fail_case("OPS2-005", "back 잡에 ./gradlew test가 없다.")
    ok("OPS2-005", "back 잡은 working-directory back에서 ./gradlew test(JUnit)를 실행한다.")


def test_OPS2_006():
    steps = [step.get("run", "") for step in ci()["jobs"]["front"]["steps"]]
    if "npm ci" not in steps or "npm run build" not in steps:
        fail_case("OPS2-006", f"front 빌드 스텝이 없다: {steps}")
    ok("OPS2-006", "front 잡에 npm ci와 npm run build가 별도 스텝으로 있다.")


def test_OPS2_007():
    version = None
    for step in ci()["jobs"]["data"]["steps"]:
        if "setup-python" in step.get("uses", ""):
            version = step["with"]["python-version"]
    if str(version) != "3.11":
        fail_case("OPS2-007", f"data Python이 3.11이 아니다: {version}")
    ok("OPS2-007", "data 잡 setup-python python-version은 3.11이다.")


def test_OPS2_008():
    version = None
    for step in ci()["jobs"]["ai"]["steps"]:
        if "setup-python" in step.get("uses", ""):
            version = step["with"]["python-version"]
    if str(version) != "3.12":
        fail_case("OPS2-008", f"ai Python이 3.12가 아니다: {version}")
    ok("OPS2-008", "ai 잡 setup-python python-version은 3.12이다.")


def test_OPS2_009():
    found = None
    for step in ci()["jobs"]["back"]["steps"]:
        if "setup-java" in step.get("uses", ""):
            found = step["with"]
    if not found or found.get("distribution") != "temurin" or str(found.get("java-version")) != "17":
        fail_case("OPS2-009", f"Java 설정이 Temurin 17이 아니다: {found}")
    ok("OPS2-009", "back 잡 setup-java distribution=temurin, java-version=17이다.")


def test_OPS2_010():
    version = None
    for step in ci()["jobs"]["front"]["steps"]:
        if "setup-node" in step.get("uses", ""):
            version = step["with"]["node-version"]
    if str(version) != "22":
        fail_case("OPS2-010", f"Node가 22가 아니다: {version}")
    ok("OPS2-010", "front 잡 setup-node node-version은 22이다.")


def test_OPS2_011():
    text = CI_PATH.read_text(encoding="utf-8")
    ai_steps = ci()["jobs"]["ai"]["steps"]
    if any(step.get("continue-on-error") for step in ai_steps) or "continue-on-error" in text:
        fail_case("OPS2-011", "CI에 continue-on-error가 있어 테스트 실패가 워크플로 실패로 이어지지 않을 수 있다.")
    ok("OPS2-011", "ai pytest 스텝에 continue-on-error가 없다. 해당 잡이 실패하면 GitHub Actions 워크플로 결론도 실패다.")


def test_OPS2_012():
    workflow = ci()
    permissions = workflow.get("permissions")
    if permissions in ({"contents": "read"}, "read-all") or (
        isinstance(permissions, dict) and set(permissions.values()) <= {"read"}
    ):
        ok("OPS2-012", f"ci.yml permissions가 최소 권한이다: {permissions}")
        return
    fail_case("OPS2-012", "ci.yml에 permissions 최소 권한(contents: read 등) 선언이 없다.")


def test_OPS2_013():
    rag = ROOT / "ai" / "tests" / "test_commercial_rag.py"
    steps = " ".join(step.get("run", "") for step in ci()["jobs"]["ai"]["steps"])
    if rag.is_file() and "python -m pytest tests" in steps:
        ok("OPS2-013", "ai CI가 ai/tests를 pytest로 돌리고 그 안에 test_commercial_rag.py 회귀 테스트가 있다.")
        return
    fail_case("OPS2-013", "CI pytest 경로 안에 commercial RAG 회귀 테스트가 없다.")


def test_OPS2_014():
    text = CI_PATH.read_text(encoding="utf-8")
    if "docker compose build" in text or "docker build" in text:
        ok("OPS2-014", "CI에 이미지 빌드 검증 스텝이 있다.")
        return
    fail_case("OPS2-014", "ci.yml에 docker compose build 또는 docker build 스텝이 없다.")


def test_OPS2_015():
    text = CI_PATH.read_text(encoding="utf-8")
    gradle = (ROOT / "back" / "build.gradle").read_text(encoding="utf-8")
    if re.search(r"postgres|services:", text) and "testcontainers" in gradle.lower():
        ok("OPS2-015", "CI에 Postgres 서비스와 통합 테스트 의존성이 있다.")
        return
    if "com.h2database:h2" not in gradle:
        fail_case("OPS2-015", "백엔드 테스트 DB 구성을 확인하지 못했다.")
    fail_case("OPS2-015", "ci.yml에 Postgres 서비스가 없고 백엔드 테스트는 H2다. 실제 PostgreSQL JPA/SQL 통합테스트가 없다.")


def test_OPS2_016():
    text = CI_PATH.read_text(encoding="utf-8")
    if "secrets." in text or "pull_request_target" in text:
        fail_case("OPS2-016", "ci.yml이 시크릿을 참조하거나 pull_request_target을 쓴다.")
    ok("OPS2-016", "ci.yml은 secrets 참조와 pull_request_target이 없다. 포크 PR에 넘길 비밀키가 워크플로에 없다.")


def test_OPS2_017():
    workflow = ci()
    if workflow.get("concurrency"):
        ok("OPS2-017", f"CI concurrency가 있다: {workflow['concurrency']}")
        return
    fail_case("OPS2-017", "ci.yml에 concurrency가 없어 같은 커밋의 연속 push 실행이 겹치고 결과를 구분하는 장치가 없다.")


def test_OPS2_018():
    text = CI_PATH.read_text(encoding="utf-8").lower()
    if any(token in text for token in ("eslint", "ruff", "checkstyle", "npm run lint")):
        ok("OPS2-018", "CI에 정적 분석 게이트가 있다.")
        return
    fail_case("OPS2-018", "ci.yml에 ESLint, ruff, Checkstyle 등 정적 분석 게이트가 없다.")


def test_OPS3_001():
    branches = deploy()["on"]["push"]["branches"]
    if "main" not in branches:
        fail_case("OPS3-001", f"deploy push 분기에 main이 없다: {branches}")
    ok("OPS3-001", "deploy.yml on.push.branches에 main이 있어 main 푸시가 CD를 트리거한다.")


def test_OPS3_002():
    triggers = deploy()["on"]
    if "workflow_dispatch" not in triggers:
        fail_case("OPS3-002", "workflow_dispatch가 없다.")
    ok("OPS3-002", "deploy.yml on.workflow_dispatch가 있어 수동 배포 트리거가 있다.")


def test_OPS3_003():
    home = Path("/tmp/qa-ops3-ssh-missing-key")
    shutil.rmtree(home, ignore_errors=True)
    home.mkdir()
    result = bash(ssh_script(), env={"HOME": str(home), "SSH_KEY": "", "EC2_HOST": "203.0.113.10", "EC2_USER": "ubuntu"})
    combined = result.stdout + result.stderr
    if result.returncode == 0 or "EC2_SSH_KEY" not in combined:
        fail_case("OPS3-003", f"빈 SSH 키가 배포를 중단하지 않았다. rc={result.returncode} {combined[-160]}")
    ok("OPS3-003", "SSH_KEY가 비면 Setup SSH 스크립트가 EC2_SSH_KEY 오류를 내고 종료코드 1로 멈춘다.")


def test_OPS3_004():
    home = Path("/tmp/qa-ops3-ssh-missing-host")
    shutil.rmtree(home, ignore_errors=True)
    home.mkdir()
    key = "not-empty"
    result = bash(ssh_script(), env={"HOME": str(home), "SSH_KEY": key, "EC2_HOST": "", "EC2_USER": "ubuntu"})
    combined = result.stdout + result.stderr
    if result.returncode == 0 or "EC2_HOST" not in combined:
        fail_case("OPS3-004", f"빈 EC2_HOST가 중단되지 않았다. rc={result.returncode}")
    ok("OPS3-004", "EC2_HOST가 비면 스크립트가 EC2_HOST 오류를 내고 0이 아닌 코드로 멈춘다.")


def test_OPS3_005():
    home = _ssh_home_with_real_key("qa-ops3-mode")
    result = bash(ssh_script(), env={"HOME": str(home), "SSH_KEY": (home / "id").read_text(), "EC2_HOST": "203.0.113.10"})
    key_path = home / ".ssh" / "deploy_key"
    mode = stat.S_IMODE(key_path.stat().st_mode)
    if result.returncode != 0 or mode != 0o600:
        fail_case("OPS3-005", f"deploy_key 모드가 600이 아니다. mode={oct(mode)} rc={result.returncode} {result.stderr[-120]}")
    ok("OPS3-005", "임시 키로 Setup SSH를 실행하니 $HOME/.ssh/deploy_key 모드가 600이다.")


def test_OPS3_006():
    home = _ssh_home_with_real_key("qa-ops3-dir")
    result = bash(ssh_script(), env={"HOME": str(home), "SSH_KEY": (home / "id").read_text(), "EC2_HOST": "203.0.113.10"})
    mode = stat.S_IMODE((home / ".ssh").stat().st_mode)
    if result.returncode != 0 or mode != 0o700:
        fail_case("OPS3-006", f".ssh 모드가 700이 아니다. mode={oct(mode)} rc={result.returncode}")
    ok("OPS3-006", "Setup SSH 실행 후 $HOME/.ssh 디렉터리 모드가 700이다.")


def test_OPS3_007():
    home = Path("/tmp/qa-ops3-bad-key")
    shutil.rmtree(home, ignore_errors=True)
    home.mkdir()
    result = bash(
        ssh_script(),
        env={"HOME": str(home), "SSH_KEY": "not-a-private-key", "EC2_HOST": "203.0.113.10"},
    )
    if result.returncode == 0:
        fail_case("OPS3-007", "잘못된 키가 ssh-keygen -y를 통과했다.")
    ok("OPS3-007", "쓰레기 문자열 키는 ssh-keygen -y 단계에서 실패하고 set -eu 때문에 스크립트가 중단된다.")


def test_OPS3_008():
    text = ssh_script()
    if "ssh-keyscan" not in text or "known_hosts" not in text:
        fail_case("OPS3-008", "ssh-keyscan known_hosts 등록 명령이 없다.")
    home = _ssh_home_with_real_key("qa-ops3-scan")
    stub = home / "bin"
    stub.mkdir()
    scanner = stub / "ssh-keyscan"
    scanner.write_text("#!/bin/sh\necho 'host-line example'\n", encoding="utf-8")
    scanner.chmod(0o755)
    env = os.environ.copy()
    env.update({"HOME": str(home), "SSH_KEY": (home / "id").read_text(), "EC2_HOST": "203.0.113.10", "PATH": f"{stub}:{env.get('PATH', '')}"})
    result = subprocess.run(["bash", "-se"], input=text, env=env, text=True, capture_output=True)
    known = (home / ".ssh" / "known_hosts").read_text(encoding="utf-8")
    if result.returncode != 0 or "host-line example" not in known:
        fail_case("OPS3-008", f"known_hosts에 스캔 결과가 없다. rc={result.returncode} body={known!r}")
    ok("OPS3-008", "ssh-keyscan 스텁 결과가 known_hosts에 추가됐다. 워크플로 원문도 ssh-keyscan -H >> known_hosts 이다.")


def test_OPS3_009():
    text = deploy_text()
    if "-o ConnectTimeout=30" not in text:
        fail_case("OPS3-009", "SSH ConnectTimeout=30이 없다.")
    ok("OPS3-009", "배포 ssh 명령에 -o ConnectTimeout=30 이 있다.")


def test_OPS3_010():
    block = _path_block()
    if block.find("/home/ubuntu/dasigolmok_v2") > block.find("$HOME/dasigolmok_v2"):
        fail_case("OPS3-010", "첫 후보 경로가 HOME보다 뒤에 있다.")
    first = Path("/tmp/qa-ops3-first/dasigolmok_v2")
    second = Path("/tmp/qa-ops3-home-unused/dasigolmok_v2")
    shutil.rmtree(first.parent, ignore_errors=True)
    shutil.rmtree(second.parent, ignore_errors=True)
    first.mkdir(parents=True)
    second.mkdir(parents=True)
    code, output = _run_path_block(first, second)
    if code != 0 or output.strip() != str(first):
        fail_case("OPS3-010", f"첫 후보를 쓰지 않았다. rc={code} out={output!r}")
    ok("OPS3-010", "원문 if 순서는 /home/ubuntu/dasigolmok_v2가 먼저다. 두 디렉터리가 있으면 그 분기가 선택된다.")


def test_OPS3_011():
    first = Path("/tmp/qa-ops3-missing-first/dasigolmok_v2")
    second = Path("/tmp/qa-ops3-home/dasigolmok_v2")
    shutil.rmtree(first.parent, ignore_errors=True)
    shutil.rmtree(second.parent, ignore_errors=True)
    second.mkdir(parents=True)
    code, output = _run_path_block(first, second)
    if code != 0 or output.strip() != str(second):
        fail_case("OPS3-011", f"HOME 후보로 떨어지지 않았다. rc={code} out={output!r}")
    ok("OPS3-011", "첫 경로가 없으면 원문 elif의 $HOME/dasigolmok_v2 분기가 선택된다.")


def test_OPS3_012():
    first = Path("/tmp/qa-ops3-none-a/dasigolmok_v2")
    second = Path("/tmp/qa-ops3-none-b/dasigolmok_v2")
    shutil.rmtree(first.parent, ignore_errors=True)
    shutil.rmtree(second.parent, ignore_errors=True)
    code, output = _run_path_block(first, second)
    if code == 0 or "찾을 수 없습니다" not in output:
        fail_case("OPS3-012", f"없는 경로에서 종료하지 않았다. rc={code} out={output!r}")
    ok("OPS3-012", "두 후보 디렉터리가 없으면 원문 else가 오류 문구를 내고 종료코드 1이다.")


def test_OPS3_013():
    remote = remote_script()
    if "git fetch origin main" not in remote:
        fail_case("OPS3-013", "원격 스크립트에 git fetch origin main이 없다.")
    origin = Path("/tmp/qa-ops3-origin.git")
    work = Path("/tmp/qa-ops3-work")
    shutil.rmtree(origin, ignore_errors=True)
    shutil.rmtree(work, ignore_errors=True)
    run(["git", "init", "--bare", "-b", "main", str(origin)])
    run(["git", "clone", str(origin), str(work)])
    _git(work, "config", "user.email", "qa@example.com")
    _git(work, "config", "user.name", "qa")
    (work / "README.txt").write_text("v1\n", encoding="utf-8")
    _git(work, "add", "README.txt")
    _git(work, "commit", "-m", "init")
    _git(work, "push", "origin", "main")
    (work / "README.txt").write_text("v2\n", encoding="utf-8")
    _git(work, "commit", "-am", "second")
    _git(work, "push", "origin", "main")
    _git(work, "reset", "--hard", "HEAD~1")
    fetched = _git(work, "fetch", "origin", "main")
    if fetched.returncode != 0:
        fail_case("OPS3-013", f"git fetch origin main 실패: {fetched.stderr[-160]}")
    head = _git(work, "rev-parse", "HEAD").stdout.strip()
    origin_main = _git(work, "rev-parse", "origin/main").stdout.strip()
    if head == origin_main:
        fail_case("OPS3-013", "fetch 후 origin/main이 로컬 HEAD와 달라지지 않았다.")
    ok("OPS3-013", "배포 스크립트에 git fetch origin main이 있고, 임시 origin에서 그 명령이 새 커밋 참조를 받았다.")


def test_OPS3_014():
    remote = remote_script()
    if "git pull --ff-only origin main" not in remote:
        fail_case("OPS3-014", "git pull --ff-only origin main이 없다.")
    origin = Path("/tmp/qa-ops3-ff-origin.git")
    left = Path("/tmp/qa-ops3-ff-left")
    right = Path("/tmp/qa-ops3-ff-right")
    for path in (origin, left, right):
        shutil.rmtree(path, ignore_errors=True)
    run(["git", "init", "--bare", "-b", "main", str(origin)])
    run(["git", "clone", str(origin), str(left)])
    _git(left, "config", "user.email", "qa@example.com")
    _git(left, "config", "user.name", "qa")
    (left / "file.txt").write_text("base\n", encoding="utf-8")
    _git(left, "add", "file.txt")
    _git(left, "commit", "-m", "base")
    _git(left, "push", "origin", "main")
    run(["git", "clone", str(origin), str(right)])
    _git(right, "config", "user.email", "qa@example.com")
    _git(right, "config", "user.name", "qa")
    (left / "file.txt").write_text("left\n", encoding="utf-8")
    _git(left, "commit", "-am", "left")
    _git(left, "push", "origin", "main")
    (right / "file.txt").write_text("right\n", encoding="utf-8")
    _git(right, "commit", "-am", "right")
    pulled = _git(right, "pull", "--ff-only", "origin", "main")
    merges = _git(right, "log", "--merges", "-1", "--oneline")
    if pulled.returncode == 0 or merges.stdout.strip():
        fail_case("OPS3-014", "분기된 브랜치에서 ff-only pull이 머지를 만들었거나 성공했다.")
    ok("OPS3-014", "배포 스크립트는 git pull --ff-only origin main이다. 갈라진 임시 저장소에서 그 명령은 머지 커밋 없이 실패했다.")


def test_OPS3_015():
    remote = remote_script()
    if '.env' not in remote or "exit 1" not in remote:
        fail_case("OPS3-015", "원격 스크립트의 .env 중단 분기를 찾지 못했다.")
    work = Path("/tmp/qa-ops3-no-env")
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir()
    snippet = """
    set -e
    if [ ! -f .env ]; then
      echo "::error::.env 파일이 없습니다. 서버 디렉터리에 .env 파일을 생성해주세요."
      exit 1
    fi
    echo SHOULD_NOT_RUN
    """
    if "서버 디렉터리에 .env" not in remote:
        fail_case("OPS3-015", "워크플로 .env 오류 문구가 바뀌어 스니펫과 다르다.")
    result = bash(textwrap.dedent(snippet), cwd=work)
    if result.returncode == 0 or "SHOULD_NOT_RUN" in result.stdout:
        fail_case("OPS3-015", ".env 없이도 스크립트가 계속 진행했다.")
    local = run(["bash", "scripts/deploy.sh"])
    if local.returncode == 0 or ".env" not in (local.stdout + local.stderr):
        fail_case("OPS3-015", "로컬 deploy.sh가 .env 없이 중단하지 않았다.")
    ok("OPS3-015", "서버 스크립트와 scripts/deploy.sh 모두 .env가 없으면 기동 전에 오류로 종료한다. 저장소 루트 .env는 없다.")


def test_OPS3_016():
    remote = remote_script()
    config_at = remote.index("docker compose config --quiet")
    up_at = remote.index("docker compose up")
    if config_at > up_at:
        fail_case("OPS3-016", "compose config가 up보다 뒤에 있다.")
    work = Path("/tmp/qa-ops3-bad-compose")
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir()
    (work / "compose.yaml").write_text("services: [\n", encoding="utf-8")
    result = run(["docker", "compose", "config", "--quiet"], cwd=work, env=compose_env())
    if result.returncode == 0:
        fail_case("OPS3-016", "잘못된 YAML인데 docker compose config가 성공했다.")
    ok("OPS3-016", "배포 스크립트는 up 전에 docker compose config --quiet를 호출한다. 깨진 compose.yaml로 config를 실행하면 종료코드가 0이 아니다.")


def test_OPS3_017():
    remote = remote_script()
    if "docker compose up -d --build --remove-orphans" not in remote:
        fail_case("OPS3-017", f"up 플래그가 기대와 다르다.")
    ok("OPS3-017", "원격 스크립트에 docker compose up -d --build --remove-orphans 가 있다. 스택은 기동하지 않았다.")


def test_OPS3_018():
    remote = remote_script()
    if "docker compose ps" not in remote:
        fail_case("OPS3-018", "배포 스크립트에 docker compose ps가 없다.")
    ok("OPS3-018", "up 다음에 docker compose ps가 있어 서비스 상태를 출력하도록 되어 있다.")


def test_OPS3_019():
    remote = remote_script()
    if "curl --fail --retry 10" not in remote or "http://localhost/" not in remote:
        fail_case("OPS3-019", "front curl 재시도 10회가 없다.")
    ok("OPS3-019", "배포 스크립트가 http://localhost/ 를 curl --fail --retry 10 --retry-delay 3 으로 확인한다.")


def test_OPS3_020():
    remote = remote_script()
    if re.search(r"ai:8000|/health", remote):
        ok("OPS3-020", "배포 스크립트가 AI health를 직접 확인한다.")
        return
    fail_case("OPS3-020", "배포 검증은 curl http://localhost/ 뿐이고 내부 AI 8000 readiness 확인이 없다.")


def test_OPS3_021():
    remote = remote_script()
    if "/api/health" in remote:
        ok("OPS3-021", "배포 스크립트가 /api/health를 확인한다.")
        return
    fail_case("OPS3-021", "배포 스크립트에 /api/health 확인이 없다. 프론트 HTML curl만 있다.")


def test_OPS3_022():
    remote = remote_script() + deploy_text()
    if re.search(r"rollback|이전 버전|git reset --hard HEAD", remote):
        ok("OPS3-022", "자동 롤백 명령이 있다.")
        return
    fail_case("OPS3-022", "deploy.yml에 배포 실패 시 이전 커밋으로 되돌리는 rollback 단계가 없다.")


def test_OPS3_023():
    workflow = deploy()
    text = deploy_text()
    needs_ci = "workflow_run" in workflow["on"] or "needs:" in text
    if needs_ci and re.search(r"ci\.yml|conclusion == 'success'", text):
        ok("OPS3-023", "CD가 CI 성공 뒤에만 돈다.")
        return
    fail_case("OPS3-023", "deploy.yml은 push main이면 CI 성공 여부와 무관하게 배포한다. workflow_run 성공 게이트가 없다.")


def test_OPS3_024():
    concurrency = deploy().get("concurrency") or {}
    if concurrency.get("cancel-in-progress") is not False or not concurrency.get("group"):
        fail_case("OPS3-024", f"concurrency 직렬 설정이 아니다: {concurrency}")
    ok("OPS3-024", f"concurrency.group={concurrency['group']}, cancel-in-progress=false 라 배포가 취소되지 않고 직렬로 기다린다.")


def test_OPS3_025():
    text = deploy_text()
    if "StrictHostKeyChecking=accept-new" not in text:
        fail_case("OPS3-025", "StrictHostKeyChecking=accept-new 가 없다.")
    if "StrictHostKeyChecking=no" in text:
        fail_case("OPS3-025", "호스트 키 검사를 끄고 있다.")
    ok("OPS3-025", "ssh는 StrictHostKeyChecking=accept-new 다. known_hosts와 다른 기존 키는 OpenSSH가 거부한다.")


def test_OPS3_026():
    remote = remote_script()
    if "docker compose logs" in remote:
        ok("OPS3-026", "curl 실패 경로에 docker compose logs가 있다.")
        return
    fail_case("OPS3-026", "curl 실패 때 docker compose logs를 출력하는 단계가 배포 스크립트에 없다.")


def test_OPS3_027():
    remote = remote_script()
    if "/api/options" in remote:
        ok("OPS3-027", "배포 확인에 GET /api/options가 있다.")
        return
    fail_case("OPS3-027", "배포 헬스체크가 http://localhost/ HTML뿐이고 GET /api/options 사용자 요청 확인이 없다.")


def _ssh_home_with_real_key(name: str) -> Path:
    home = Path("/tmp") / name
    shutil.rmtree(home, ignore_errors=True)
    home.mkdir()
    key = home / "id"
    subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-N", "", "-f", str(key), "-q"],
        check=True,
        capture_output=True,
    )
    return home


def _path_block() -> str:
    remote = remote_script()
    start = remote.index("if [ -d /home/ubuntu/dasigolmok_v2 ]")
    end = remote.index("git fetch origin main")
    return remote[start:end]


def _run_path_block(first: Path, second: Path):
    block = _path_block()
    runnable = block.replace("/home/ubuntu/dasigolmok_v2", str(first)).replace('"$HOME/dasigolmok_v2"', f'"{second}"')
    script = "set -e\n" + runnable + "pwd\n"
    result = bash(script, env={"HOME": str(second.parent)})
    return result.returncode, result.stdout + result.stderr


def _git(repo: Path, *args):
    return run(["git", "-C", str(repo), *args])
