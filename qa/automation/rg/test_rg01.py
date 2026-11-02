"""RG01 상권 RAG HTTP."""
import pytest

from rg_support import router_module
from src.features.commercial_rag_001.router import router
from src.features.commercial_rag_001.schemas import CommercialRagResponse


def test_RG01_001(client):
    """GET /health 가 status=ok, feature=commercial_rag_001 을 반환한다."""
    response = client.get("/api/v1/commercial-rag/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["feature"] == "commercial_rag_001"


def test_RG01_002(client):
    """question='연남동 창업은?' POST /ask 가 200 CommercialRagResponse 이다."""
    response = client.post(
        "/api/v1/commercial-rag/ask",
        json={"question": "연남동 창업은?"},
    )
    assert response.status_code == 200
    body = response.json()
    for key in ("question", "answer", "intent", "evidence_documents", "policies", "citations", "warnings", "execution_metadata"):
        assert key in body
    assert body["question"] == "연남동 창업은?"
    assert isinstance(body["answer"], str) and body["answer"]
    assert body["intent"] in {"market_analysis", "support_policy", "hybrid"}


def test_RG01_003(client):
    """시장 검색 POST /market-search 가 200 MarketSearchResponse 이다."""
    response = client.post(
        "/api/v1/commercial-rag/market-search",
        json={"query": "연남동 한식 상권", "district": "마포구", "top_k": 3},
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["documents"], list)
    assert body["total_count"] == len(body["documents"])
    assert body["total_count"] >= 1


def test_RG01_004(client):
    """정책 검색 POST /support-policies 가 200 SupportPolicyResponse 이다."""
    response = client.post(
        "/api/v1/commercial-rag/support-policies",
        json={"query": "청년 창업", "target_date": "2026-11-02", "only_open": True, "top_k": 5},
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["policies"], list)
    assert body["total_count"] == len(body["policies"])
    assert body["total_count"] >= 1


def test_RG01_005(client):
    """POST /evaluate 가 200 EvaluationMetrics 이다."""
    response = client.post("/api/v1/commercial-rag/evaluate")
    assert response.status_code == 200
    body = response.json()
    for key in (
        "recall_at_k",
        "citation_accuracy",
        "relevance_score",
        "closed_policy_false_recommendation_rate",
        "total_evaluated",
        "items",
    ):
        assert key in body
    assert body["total_evaluated"] == len(body["items"])
    assert body["total_evaluated"] >= 1


def test_RG01_006(client):
    """question 필드 누락 POST /ask 는 422 이다."""
    response = client.post("/api/v1/commercial-rag/ask", json={"district": "마포구"})
    assert response.status_code == 422


def test_RG01_007(client):
    """question=null POST /ask 는 422 이다."""
    response = client.post("/api/v1/commercial-rag/ask", json={"question": None})
    assert response.status_code == 422


def test_RG01_008(client):
    """빈 질문 question='' 은 422 가드레일이어야 한다."""
    response = client.post("/api/v1/commercial-rag/ask", json={"question": ""})
    if response.status_code != 422:
        pytest.fail(f"빈 질문 question='' 이 {response.status_code}로 통과했다. 422 가드레일이 없다")


def test_RG01_009(client):
    """시장 검색 query 누락은 422 이다."""
    response = client.post("/api/v1/commercial-rag/market-search", json={"district": "마포구"})
    assert response.status_code == 422


def test_RG01_010(client, monkeypatch):
    """본문 없는 정책 검색은 기본값으로 200과 정책 목록을 반환한다."""
    from datetime import datetime

    import src.features.commercial_rag_001.support_policy.service as policy_svc

    class FixedNow(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 11, 2)

    monkeypatch.setattr(policy_svc, "datetime", FixedNow)
    response = client.post("/api/v1/commercial-rag/support-policies", json={})
    assert response.status_code == 200
    body = response.json()
    assert body["total_count"] == len(body["policies"])
    assert body["total_count"] >= 1
    assert all(item["is_open"] is True for item in body["policies"])


def test_RG01_011(client):
    """지원 정책 top_k=-1 은 422 또는 1 이상 제한이어야 한다."""
    response = client.post(
        "/api/v1/commercial-rag/support-policies",
        json={"query": "지원", "target_date": "2026-11-02", "only_open": False, "top_k": -1},
    )
    if response.status_code != 422:
        count = response.json().get("total_count")
        pytest.fail(f"top_k=-1 이 {response.status_code}로 수용되고 total_count={count}. 1 이상 제한이 없다")


def test_RG01_012(client):
    """시장 검색 top_k=0 은 422 로 거절되어야 한다."""
    response = client.post(
        "/api/v1/commercial-rag/market-search",
        json={"query": "연남동", "top_k": 0},
    )
    if response.status_code != 422:
        body = response.json()
        pytest.fail(
            f"top_k=0 이 {response.status_code}로 수용되고 documents={len(body.get('documents', []))}. 0건 요구 검증이 없다"
        )


def test_RG01_013(client):
    """지원 정책 target_date=2026/11/02 는 422 이어야 한다."""
    response = client.post(
        "/api/v1/commercial-rag/support-policies",
        json={"query": "지원", "target_date": "2026/11/02"},
    )
    if response.status_code != 422:
        pytest.fail(f"target_date=2026/11/02 가 {response.status_code}로 수용된다. 날짜 형식 검증이 없다")


def test_RG01_014(client, monkeypatch):
    """RAG ask 내부 예외는 HTTP 500 detail 로 반환된다."""
    router_mod = router_module()

    def boom(_request):
        raise RuntimeError("rag-internal-error")

    monkeypatch.setattr(router_mod, "execute_commercial_rag_workflow", boom)
    response = client.post("/api/v1/commercial-rag/ask", json={"question": "연남동 매출"})
    assert response.status_code == 500
    assert "rag-internal-error" in response.text


def test_RG01_015(client, monkeypatch):
    """지원 정책 내부 예외는 HTTP 500 detail 이다."""
    router_mod = router_module()

    def boom(_query):
        raise RuntimeError("policy-internal-error")

    monkeypatch.setattr(router_mod, "search_policies", boom)
    response = client.post("/api/v1/commercial-rag/support-policies", json={"query": "지원금"})
    assert response.status_code == 500
    assert "policy-internal-error" in response.text


def test_RG01_016(client, monkeypatch):
    """평가 내부 예외는 HTTP 500 detail 이다."""
    router_mod = router_module()

    def boom():
        raise RuntimeError("eval-internal-error")

    monkeypatch.setattr(router_mod, "run_evaluation_suite", boom)
    response = client.post("/api/v1/commercial-rag/evaluate")
    assert response.status_code == 500
    assert "eval-internal-error" in response.text


def test_RG01_017(client, monkeypatch):
    """500 detail 에 API 키 등 내부 비밀이 노출되면 안 된다."""
    router_mod = router_module()

    secret = "super-secret-RG01-017"

    def boom(_request):
        raise RuntimeError(f"GEMINI_API_KEY={secret}")

    monkeypatch.setattr(router_mod, "execute_commercial_rag_workflow", boom)
    response = client.post("/api/v1/commercial-rag/ask", json={"question": "연남동 매출"})
    assert response.status_code == 500
    if secret in response.text:
        pytest.fail(f"500 detail에 비밀값이 노출됨: {response.text[:180]}")


def test_RG01_018(client):
    """POST /ask JSON 필수 필드 타입이 스키마와 일치한다."""
    response = client.post(
        "/api/v1/commercial-rag/ask",
        json={"question": "연남동 매출 동향", "district": "마포구", "top_k": 2},
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["question"], str)
    assert isinstance(body["answer"], str)
    assert isinstance(body["intent"], str)
    assert isinstance(body["evidence_documents"], list)
    assert isinstance(body["policies"], list)
    assert isinstance(body["citations"], list)
    assert isinstance(body["warnings"], list)
    assert isinstance(body["execution_metadata"], dict)
    assert "latency_ms" in body["execution_metadata"]
    assert "logs" in body["execution_metadata"]


def test_RG01_019(client):
    """외부 호출은 인증 없이 거부되거나 라우터에 인증 의존성이 있어야 한다."""
    secured = bool(getattr(router, "dependencies", None))
    for route in router.routes:
        if getattr(route, "dependencies", None):
            secured = True
    response = client.get("/api/v1/commercial-rag/health")
    if response.status_code < 400 and not secured:
        pytest.fail(
            f"인증 의존성 없이 GET /health 가 {response.status_code}이다. 라우터 dependencies={list(router.dependencies)}"
        )


def test_RG01_020(client, monkeypatch):
    """연속 50회 POST /ask 는 429 등 과요청 제한이 있어야 한다."""
    router_mod = router_module()

    def ok(request):
        return CommercialRagResponse(question=request.question, answer="ok", intent="hybrid")

    monkeypatch.setattr(router_mod, "execute_commercial_rag_workflow", ok)
    codes = [
        client.post("/api/v1/commercial-rag/ask", json={"question": "연남동 매출"}).status_code
        for _ in range(50)
    ]
    if 429 not in codes and all(code == 200 for code in codes):
        pytest.fail(f"50회 연속 /ask 상태={set(codes)}. timeout/429 제한이 없다")
