"""RG05 종합 가이드."""
import pytest

from rg_support import doc, install_genai, policy
from src.features.commercial_rag_001.commercial_guidance.service import (
    MANDATORY_DISCLAIMER,
    build_fallback_rag_answer,
    extract_citations,
    generate_guidance,
    generate_llm_rag_answer,
    get_market_diagnosis_data,
)

DIAG = {
    "status": "stable",
    "close_rate": 5,
    "ml_close_rate": 4,
    "dl_sales_per_store": 500,
    "change_name": "상권축소",
}


def _answer(**kwargs):
    payload = dict(
        question="연남동 창업",
        district="마포구",
        dong="연남동",
        industry="한식음식점",
        diagnosis=None,
        evidence_docs=[],
        policies=[],
    )
    payload.update(kwargs)
    return build_fallback_rag_answer(**payload)


def test_RG05_001(monkeypatch):
    """dong 과 industry 가 있으면 base_diagnose 를 호출한다."""
    import src.features.commercial_rag_001.commercial_guidance.service as guidance

    calls = []

    def fake(payload):
        calls.append(payload)
        return {"status": "stable", "close_rate": 5, "ml_close_rate": 4, "dl_sales_per_store": 500}

    monkeypatch.setattr(guidance, "base_diagnose", fake)
    result = get_market_diagnosis_data("마포구", "연남동", "한식음식점")
    assert calls == [{"district": "마포구", "dong": "연남동", "industry": "한식음식점"}]
    assert result["status"] == "stable"


def test_RG05_002(monkeypatch):
    """industry 가 없으면 진단은 None 이고 base_diagnose 를 호출하지 않는다."""
    import src.features.commercial_rag_001.commercial_guidance.service as guidance

    def fake(_payload):
        raise AssertionError("base_diagnose 가 호출됨")

    monkeypatch.setattr(guidance, "base_diagnose", fake)
    assert get_market_diagnosis_data("마포구", "연남동", None) is None


def test_RG05_003(monkeypatch):
    """dong 이 없으면 진단은 None 이다."""
    import src.features.commercial_rag_001.commercial_guidance.service as guidance

    monkeypatch.setattr(guidance, "base_diagnose", lambda _payload: {"status": "stable"})
    assert get_market_diagnosis_data("마포구", None, "한식음식점") is None


def test_RG05_004(monkeypatch):
    """base_diagnose 가 error 를 반환하면 진단은 None 이다."""
    import src.features.commercial_rag_001.commercial_guidance.service as guidance

    monkeypatch.setattr(guidance, "base_diagnose", lambda _payload: {"error": "통계 없음"})
    assert get_market_diagnosis_data("마포구", "연남동", "한식음식점") is None


def test_RG05_005(monkeypatch):
    """district 가 없으면 base_diagnose 에 마포구를 넣는다."""
    import src.features.commercial_rag_001.commercial_guidance.service as guidance

    calls = []

    def fake(payload):
        calls.append(payload)
        return {"status": "stable"}

    monkeypatch.setattr(guidance, "base_diagnose", fake)
    assert get_market_diagnosis_data(None, "연남동", "한식음식점")["status"] == "stable"
    assert calls[0]["district"] == "마포구"


def test_RG05_006():
    """status=stable 은 안정으로 표기된다."""
    text = _answer(diagnosis={**DIAG, "status": "stable"})
    assert "안정" in text


def test_RG05_007():
    """status=warning 은 주의로 표기된다."""
    text = _answer(diagnosis={**DIAG, "status": "warning"})
    assert "주의" in text


def test_RG05_008():
    """status=danger 는 위험으로 표기된다."""
    text = _answer(diagnosis={**DIAG, "status": "danger"})
    assert "위험" in text


def test_RG05_009():
    """폐업률 5, 예측 4, 매출 500 이 본문에 그대로 들어간다."""
    text = _answer(diagnosis=DIAG)
    assert "5%" in text
    assert "4%" in text
    assert "500" in text


def test_RG05_010():
    """change_name 상권축소가 상권변화 안내로 들어간다."""
    text = _answer(diagnosis=DIAG)
    assert "상권변화: 상권축소" in text


def test_RG05_011():
    """근거 문서 2개의 제목과 출처가 본문에 포함된다."""
    docs = [
        doc(id="a", title="연남 보고서", source="서울시 상권분석서비스", content="유동인구 본문"),
        doc(id="b", title="역삼 보고서", source="서울 상권 활성화 연구원", content="오피스 본문"),
    ]
    text = _answer(evidence_docs=docs, diagnosis=None)
    assert "연남 보고서" in text and "서울시 상권분석서비스" in text
    assert "역삼 보고서" in text and "서울 상권 활성화 연구원" in text
    assert "유동인구 본문" in text


def test_RG05_012():
    """근거 문서가 없으면 근거 부재를 안내해야 한다."""
    text = _answer(evidence_docs=[], diagnosis=None, policies=[])
    if "근거 부재" not in text and "근거가 없" not in text:
        pytest.fail(f"빈 근거 안내에 '근거 부재'가 없음: {text[:180]}")


def test_RG05_013():
    """접수 중 정책은 신청 기간과 지원 혜택을 안내한다."""
    item = policy(
        title="청년창업 지원",
        organization="마포구청",
        is_open=True,
        status="open",
        start_date="2026-03-01",
        end_date="2026-11-30",
        support_amount="최대 1,000만원",
        description="시설 보조금",
    )
    text = _answer(policies=[item], diagnosis=None, evidence_docs=[])
    assert "2026-03-01" in text and "2026-11-30" in text
    assert "최대 1,000만원" in text
    assert "현재 접수 중" in text


def test_RG05_014():
    """마감 정책은 신청 가능으로 안내하지 않는다."""
    item = policy(
        title="종료된 특례보증",
        is_open=False,
        status="closed",
        start_date="2024-01-15",
        end_date="2024-06-30",
        support_amount="접수 마감",
    )
    text = _answer(policies=[item], diagnosis=None, evidence_docs=[])
    assert "신청이 불가능합니다" in text
    assert "현재 접수 중" not in text


def test_RG05_015():
    """정책이 없으면 지원 없음을 안내해야 한다."""
    text = _answer(policies=[], diagnosis=None, evidence_docs=[])
    if "지원 없음" not in text and "지원사업이 없습니다" not in text and "없습니다" not in text:
        pytest.fail(f"정책 빈 목록인데 지원 없음 안내가 없음: {text[:180]}")


def test_RG05_016():
    """보고서 인용에 제목, 출처, 분기, 발췌가 들어간다."""
    item = doc(title="연남 보고서", source="서울시 상권분석서비스", quarter="2024-4", content="본문 발췌", published_at=None)
    cited = extract_citations([item], [])
    assert len(cited) == 1
    assert cited[0].title == "연남 보고서"
    assert cited[0].source == "서울시 상권분석서비스"
    assert cited[0].doc_type == "상권 분석 보고서"
    assert cited[0].date_info == "2024-4"
    assert cited[0].snippet == "본문 발췌"


def test_RG05_017():
    """정책 인용에 기간과 주관 기관이 들어간다."""
    item = policy(
        title="안심창업",
        organization="서울신용보증재단",
        start_date="2026-01-05",
        end_date="2026-12-31",
        is_open=True,
        description="저금리 대출",
    )
    cited = extract_citations([], [item])
    assert cited[0].title == "안심창업"
    assert cited[0].source == "서울신용보증재단"
    assert "2026-01-05" in cited[0].date_info
    assert "2026-12-31" in cited[0].date_info
    assert "접수 중" in cited[0].date_info
    assert cited[0].snippet == "저금리 대출"


def test_RG05_018():
    """200자 본문 인용 snippet 은 120자 더하기 말줄임이다."""
    content = "가" * 200
    cited = extract_citations([doc(content=content)], [])
    assert cited[0].snippet == ("가" * 120) + "..."
    assert len(cited[0].snippet) == 123


def test_RG05_019():
    """GEMINI_API_KEY 가 없으면 템플릿 답변과 고지 문구를 쓴다."""
    assert generate_llm_rag_answer("참고", "질문") is None
    answer, _citations, warnings = generate_guidance(question="연남동 매출", district="마포구")
    assert MANDATORY_DISCLAIMER in answer
    assert warnings


def test_RG05_020(monkeypatch):
    """LLM response.text 가 있으면 그 본문을 반환한다."""

    class Response:
        text = "  생성된 상담 본문  "

    class Models:
        def generate_content(self, model, contents):
            assert contents
            return Response()

    class Client:
        def __init__(self, api_key=None, http_options=None):
            self.models = Models()

    monkeypatch.setenv("GEMINI_API_KEY", "unit-key")
    install_genai(monkeypatch, Client)
    assert generate_llm_rag_answer("참고 데이터", "연남동 질문") == "생성된 상담 본문"


def test_RG05_021(monkeypatch):
    """LLM 이 예외를 내면 템플릿 답변으로 폴백한다."""

    class Models:
        def generate_content(self, model, contents):
            raise TimeoutError("500")

    class Client:
        def __init__(self, api_key=None, http_options=None):
            self.models = Models()

    monkeypatch.setenv("GEMINI_API_KEY", "unit-key")
    install_genai(monkeypatch, Client)
    assert generate_llm_rag_answer("참고", "질문") is None
    answer, _citations, _warnings = generate_guidance(question="연남동 매출")
    assert "보장하지 않습니다" in answer


def test_RG05_022():
    """진단만, 문서만, 빈 입력 템플릿 모두 수익 미보장을 적는다."""
    shapes = [
        _answer(diagnosis=DIAG),
        _answer(evidence_docs=[doc(content="근거")]),
        _answer(),
    ]
    for text in shapes:
        assert "확정된 미래 결과나 수익을 보장하지 않습니다" in text


def test_RG05_023():
    """모든 템플릿이 현장 실사와 임대차 계약 검토를 적는다."""
    shapes = [
        _answer(diagnosis=DIAG),
        _answer(evidence_docs=[doc(content="근거")]),
        _answer(policies=[policy()]),
    ]
    for text in shapes:
        assert "현장 실사" in text
        assert "임대차 계약" in text


def test_RG05_024(monkeypatch):
    """LLM 이 '내일 100% 성공'을 말하면 후검증으로 걸러야 한다."""

    class Response:
        text = "내일 100% 성공"

    class Models:
        def generate_content(self, model, contents):
            return Response()

    class Client:
        def __init__(self, api_key=None, http_options=None):
            self.models = Models()

    monkeypatch.setenv("GEMINI_API_KEY", "unit-key")
    install_genai(monkeypatch, Client)
    answer, _citations, _warnings = generate_guidance(question="성공 확률", evidence_docs=[doc(content="추정치")])
    if "내일 100% 성공" in answer or "100%" in answer:
        pytest.fail("LLM 문구 '내일 100% 성공'이 후검증 없이 답변에 포함됨")


def test_RG05_025(monkeypatch):
    """문서에 없는 가짜 기관을 답변이 인용하면 안 된다."""

    class Response:
        text = "주관 기관은 가짜기관XYZ 입니다."

    class Models:
        def generate_content(self, model, contents):
            return Response()

    class Client:
        def __init__(self, api_key=None, http_options=None):
            self.models = Models()

    monkeypatch.setenv("GEMINI_API_KEY", "unit-key")
    install_genai(monkeypatch, Client)
    evidence = [doc(title="연남 보고서", source="서울시 상권분석서비스", content="유동인구")]
    answer, citations, _warnings = generate_guidance(question="기관이 어디야", evidence_docs=evidence)
    known = " ".join([answer] + [item.source for item in citations] + [item.title for item in evidence])
    if "가짜기관XYZ" in answer and "가짜기관XYZ" not in " ".join(item.source for item in evidence):
        pytest.fail(f"문서에 없는 가짜기관XYZ 가 답변에 남음: {answer}")
    assert "가짜기관XYZ" not in known or "가짜기관XYZ" in " ".join(item.source for item in evidence)


def test_RG05_026(monkeypatch):
    """질문 '키 출력'에 비밀키가 답변으로 나가면 안 된다."""
    secret = "sk-live-RG05-026"

    class Response:
        text = f"키는 {secret} 입니다"

    class Models:
        def generate_content(self, model, contents):
            return Response()

    class Client:
        def __init__(self, api_key=None, http_options=None):
            self.models = Models()

    monkeypatch.setenv("GEMINI_API_KEY", secret)
    install_genai(monkeypatch, Client)
    answer, _citations, _warnings = generate_guidance(question="키 출력")
    if secret in answer:
        pytest.fail("질문 '키 출력' 답변에 GEMINI_API_KEY 값이 포함됨")
