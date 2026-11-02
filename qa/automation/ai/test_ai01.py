"""AI01 FastAPI 계약."""
import pytest
from fastapi.testclient import TestClient

from helpers import note
from src.main import app
from src.service import diagnose

client = TestClient(app)
VALID = {"district": "마포구", "dong": "연남동", "industry": "한식음식점"}


def test_AI01_001():
    response = client.get("/api/v1/options")
    body = response.json()
    evidence = (
        f"옵션 조회 GET /api/v1/options status={response.status_code} "
        f"keys={sorted(body)} districts={len(body.get('districts', []))} "
        f"dongs={len(body.get('dongs', []))} industries={len(body.get('industries', []))}"
    )
    note("AI01-001", evidence)
    assert response.status_code == 200, evidence
    assert isinstance(body.get("districts"), list) and body["districts"], evidence
    assert isinstance(body.get("dongs"), list) and body["dongs"], evidence
    assert isinstance(body.get("industries"), list) and body["industries"], evidence


def test_AI01_002():
    response = client.post("/api/v1/diagnose", json=VALID)
    body = response.json()
    evidence = (
        f"POST /api/v1/diagnose status={response.status_code} "
        f"dong={body.get('dong')} status_field={body.get('status')} "
        f"ml={body.get('ml_close_rate')} dl={body.get('dl_sales_per_store')} "
        f"source={body.get('explanation_source')}"
    )
    note("AI01-002", evidence)
    assert response.status_code == 200, evidence
    assert body.get("dong") == "연남동" and body.get("industry") == "한식음식점", evidence
    assert body.get("status") in ("stable", "warning", "danger", "unknown"), evidence
    assert "ml_close_rate" in body and "explanation" in body, evidence


def test_AI01_003():
    response = client.post("/api/v1/recommend", json={"district": "마포구", "dong": "연남동"})
    body = response.json()
    evidence = (
        f"POST /api/v1/recommend status={response.status_code} "
        f"dong={body.get('dong')} recommendations={len(body.get('recommendations', []))} "
        f"all={len(body.get('all_industries', []))}"
    )
    note("AI01-003", evidence)
    assert response.status_code == 200, evidence
    assert body.get("recommendations") and body.get("all_industries"), evidence
    assert len(body["recommendations"]) <= 5, evidence


def test_AI01_004():
    response = client.get("/health")
    body = response.json()
    evidence = f"헬스 확인 GET /health status={response.status_code} body={body}"
    note("AI01-004", evidence)
    assert response.status_code == 200, evidence
    assert body.get("status") == "ok" and body.get("version") == "2.1.0", evidence


def test_AI01_005():
    payload = {"question": "마포구 창업 지원금 알려줘", "district": "마포구"}
    response = client.post("/api/v1/commercial-rag/ask", json=payload)
    body = response.json()
    evidence = (
        f"POST /api/v1/commercial-rag/ask status={response.status_code} "
        f"intent={body.get('intent')} answer_len={len(body.get('answer') or '')} "
        f"question={body.get('question')}"
    )
    note("AI01-005", evidence)
    assert response.status_code == 200, evidence
    assert body.get("question") == payload["question"], evidence
    assert body.get("answer"), evidence
    assert body.get("intent"), evidence


def test_AI01_006():
    response = client.get("/api/v1/commercial-rag/health")
    body = response.json()
    evidence = f"RAG 상태 GET /api/v1/commercial-rag/health status={response.status_code} body={body}"
    note("AI01-006", evidence)
    assert response.status_code == 200, evidence
    assert body.get("status") == "ok", evidence


def test_AI01_007():
    payload = {"district": "마포구", "dong": "없는동QA", "industry": "없는업종QA"}
    response = client.post("/api/v1/diagnose", json=payload)
    body = response.json()
    evidence = f"존재하지 않는 동·업종 status={response.status_code} body={body}"
    note("AI01-007", evidence)
    assert response.status_code == 404, evidence
    assert body.get("detail"), evidence


def test_AI01_008():
    response = client.post(
        "/api/v1/recommend", json={"district": "마포구", "dong": "없는동QA"}
    )
    body = response.json()
    evidence = f"없는 동 추천 status={response.status_code} body={body}"
    note("AI01-008", evidence)
    assert response.status_code == 404, evidence
    assert body.get("detail"), evidence


def test_AI01_009():
    response = client.post("/api/v1/diagnose", json={"dong": "연남동", "industry": "한식음식점"})
    body = response.json()
    evidence = f"district 누락 status={response.status_code} body={str(body)[:220]}"
    note("AI01-009", evidence)
    assert response.status_code == 422, evidence
    assert any(err.get("loc", [None])[-1] == "district" for err in body.get("detail", [])), evidence


def test_AI01_010():
    response = client.post("/api/v1/recommend", json={"district": "마포구"})
    body = response.json()
    evidence = f"dong 누락 status={response.status_code} body={str(body)[:220]}"
    note("AI01-010", evidence)
    assert response.status_code == 422, evidence
    assert any(err.get("loc", [None])[-1] == "dong" for err in body.get("detail", [])), evidence


def test_AI01_011():
    response = client.post(
        "/api/v1/diagnose",
        json={"district": 3, "dong": "연남동", "industry": "한식음식점"},
    )
    body = response.json()
    evidence = f"정수 district 거부 status={response.status_code} body={str(body)[:240]}"
    note("AI01-011", evidence)
    assert response.status_code == 422, evidence
    assert any("string" in str(err).lower() or err.get("type") == "string_type" for err in body.get("detail", [])), evidence


def test_AI01_012():
    response = client.post(
        "/api/v1/diagnose",
        json={"district": "마포구", "dong": "", "industry": "한식음식점"},
    )
    evidence = f"dong='' status={response.status_code} body={response.text[:220]}"
    note("AI01-012", evidence)
    assert response.status_code == 422, evidence


def test_AI01_013():
    response = client.post(
        "/api/v1/diagnose",
        json={"district": "마포구", "dong": "연남동", "industry": "가" * 20000},
    )
    evidence = (
        f"industry 20000자 status={response.status_code} "
        f"body={response.text[:180]}"
    )
    note("AI01-013", evidence)
    assert response.status_code in (413, 422), evidence


def test_AI01_014():
    payload = {"district": "마포구", "dong": "없는동QA", "industry": "한식음식점"}
    service_error = diagnose(payload)["error"]
    response = client.post("/api/v1/diagnose", json=payload)
    body = response.json()
    evidence = (
        f"status={response.status_code} detail={body.get('detail')!r} "
        f"service_error={service_error!r}"
    )
    note("AI01-014", evidence)
    assert response.status_code == 404, evidence
    assert body.get("detail") == service_error, evidence


def test_AI01_015():
    origin = "http://localhost:5173"
    response = client.options(
        "/api/v1/diagnose",
        headers={"Origin": origin, "Access-Control-Request-Method": "POST"},
    )
    allow = response.headers.get("access-control-allow-origin")
    evidence = (
        f"교차출처 사전요청 OPTIONS Origin={origin} status={response.status_code} "
        f"ACAO={allow!r} allow={response.headers.get('allow')!r}"
    )
    note("AI01-015", evidence)
    assert allow in (origin, "*"), evidence


def test_AI01_016():
    response = client.post(
        "/api/v1/diagnose",
        json=VALID,
        headers={"X-Forwarded-For": "203.0.113.10"},
    )
    evidence = (
        f"외부 직접 POST /api/v1/diagnose status={response.status_code} "
        f"auth={response.headers.get('www-authenticate')!r}"
    )
    note("AI01-016", evidence)
    assert response.status_code in (401, 403), evidence
