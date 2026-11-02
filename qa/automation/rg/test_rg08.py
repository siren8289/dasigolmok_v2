"""RG08 RAG 정량 평가."""
import inspect

import pytest

from rg_support import doc, policy
from src.features.commercial_rag_001.harness.runtime import (
    calculate_citation_accuracy,
    calculate_recall_at_k,
    calculate_regional_relevance,
    evaluate_closed_policy_false_recommendations,
    run_evaluation_suite,
)
from src.features.commercial_rag_001.schemas import CitedSource


def _cite(title):
    return CitedSource(title=title, source="출처", doc_type="상권 분석 보고서", snippet="발췌")


def test_RG08_001():
    """retrieved [A,B], relevant [A,B] 의 Recall@K 는 1.0 이다."""
    assert calculate_recall_at_k(["A", "B"], ["A", "B"]) == 1.0


def test_RG08_002():
    """retrieved [A], relevant [A,B] 의 Recall@K 는 0.5 이다."""
    assert calculate_recall_at_k(["A"], ["A", "B"]) == 0.5


def test_RG08_003():
    """retrieved 가 비고 relevant 가 [A] 이면 Recall@K 는 0 이다."""
    assert calculate_recall_at_k([], ["A"]) == 0.0


def test_RG08_004():
    """relevant 가 비면 Recall@K 정의값은 1.0 이다."""
    assert calculate_recall_at_k(["A"], []) == 1.0


def test_RG08_005():
    """인용 제목이 모두 실제 문서에 있으면 인용 정확도는 1.0 이다."""
    docs = [doc(id="a", title="연남 보고서"), doc(id="b", title="역삼 보고서")]
    citations = [_cite("연남 보고서"), _cite("역삼 보고서")]
    assert calculate_citation_accuracy(citations, docs, []) == 1.0


def test_RG08_006():
    """인용 2개 중 1개만 실제 문서이면 인용 정확도는 0.5 이다."""
    docs = [doc(title="연남 보고서")]
    citations = [_cite("연남 보고서"), _cite("없는 보고서")]
    assert calculate_citation_accuracy(citations, docs, []) == 0.5


def test_RG08_007():
    """인용이 모두 실제 문서에 없으면 인용 정확도는 0 이다."""
    docs = [doc(title="연남 보고서")]
    citations = [_cite("없는 보고서"), _cite("다른 허구")]
    assert calculate_citation_accuracy(citations, docs, []) == 0.0


def test_RG08_008():
    """인용이 없으면 인용 정확도 분모 정책은 1.0 이다."""
    assert calculate_citation_accuracy([], [doc(title="연남 보고서")], []) == 1.0


def test_RG08_009():
    """문서가 모두 마포구이면 지역 적합성은 1.0 이다."""
    docs = [doc(id="a", district="마포구"), doc(id="b", district="마포구")]
    assert calculate_regional_relevance("마포구", docs, []) == 1.0


def test_RG08_010():
    """문서 2개 중 1개만 마포구이면 지역 적합성은 0.5 이다."""
    docs = [doc(id="a", district="마포구"), doc(id="b", district="강남구")]
    assert calculate_regional_relevance("마포구", docs, []) == 0.5


def test_RG08_011():
    """문서가 모두 강남구이고 질문이 마포구이면 지역 적합성은 0 이다."""
    docs = [doc(id="a", district="강남구"), doc(id="b", district="강남구")]
    assert calculate_regional_relevance("마포구", docs, []) == 0.0


def test_RG08_012():
    """target_district 가 없으면 지역 적합성 기본값은 1.0 이다."""
    docs = [doc(id="a", district="강남구")]
    assert calculate_regional_relevance(None, docs, []) == 1.0


def test_RG08_013():
    """closed 이고 is_open=False 이면 종료 정책 오안내율은 0.0 이다."""
    items = [policy(id="c", status="closed", is_open=False)]
    assert evaluate_closed_policy_false_recommendations(items) == 0.0


def test_RG08_014():
    """closed 인데 is_open=True 가 1건이면 오안내율은 1/N 이다."""
    items = [
        policy(id="bad", status="closed", is_open=True),
        policy(id="ok", status="open", is_open=True),
    ]
    assert evaluate_closed_policy_false_recommendations(items) == pytest.approx(1 / 2)


def test_RG08_015():
    """정책이 없으면 종료 정책 오안내율은 0.0 이다."""
    assert evaluate_closed_policy_false_recommendations([]) == 0.0


def test_RG08_016():
    """run_evaluation_suite 는 4개 지표와 total_evaluated, items 를 반환한다."""
    metrics = run_evaluation_suite()
    assert isinstance(metrics.recall_at_k, float)
    assert isinstance(metrics.citation_accuracy, float)
    assert isinstance(metrics.relevance_score, float)
    assert isinstance(metrics.closed_policy_false_recommendation_rate, float)
    assert metrics.total_evaluated == len(metrics.items)
    assert metrics.total_evaluated == 3


def test_RG08_017():
    """평가 지표 4개는 모두 0 이상 1 이하다."""
    metrics = run_evaluation_suite()
    for value in (
        metrics.recall_at_k,
        metrics.citation_accuracy,
        metrics.relevance_score,
        metrics.closed_policy_false_recommendation_rate,
    ):
        assert 0.0 <= value <= 1.0


def test_RG08_018():
    """빈 test_cases 로 평가해도 ZeroDivisionError 가 나지 않는다."""
    metrics = run_evaluation_suite([])
    assert metrics.total_evaluated >= 1
    assert metrics.recall_at_k == metrics.recall_at_k


def test_RG08_019():
    """같은 기본 스위트를 두 번 실행하면 4개 지표와 건수가 같다."""
    first = run_evaluation_suite()
    second = run_evaluation_suite()
    assert first.recall_at_k == second.recall_at_k
    assert first.citation_accuracy == second.citation_accuracy
    assert first.relevance_score == second.relevance_score
    assert first.closed_policy_false_recommendation_rate == second.closed_policy_false_recommendation_rate
    assert first.total_evaluated == second.total_evaluated
    assert [item.retrieved_doc_ids for item in first.items] == [item.retrieved_doc_ids for item in second.items]


def test_RG08_020(client):
    """POST /evaluate 의 items 길이와 total_evaluated 가 같다."""
    response = client.post("/api/v1/commercial-rag/evaluate")
    assert response.status_code == 200
    body = response.json()
    assert body["total_evaluated"] == len(body["items"])
    assert body["total_evaluated"] >= 1


def test_RG08_021():
    """하드코딩 샘플 평가를 운영 품질처럼 단정하면 안 된다."""
    source = inspect.getsource(run_evaluation_suite)
    metrics = run_evaluation_suite()
    hardcoded = "citation_accuracy=1.0" in source.replace(" ", "")
    blob = metrics.model_dump_json()
    marked = any(token in blob or token in source for token in ("표본", "샘플", "미검증", "비운영", "non_production"))
    if hardcoded and metrics.citation_accuracy == 1.0 and not marked:
        pytest.fail("citation_accuracy=1.0 고정이고 표본/비운영 표시가 없어 운영품질로 일반화됨")


def test_RG08_022():
    """실제 문서 제목이 아닌 인용은 인용 정확도 0 으로 검출된다."""
    citations = [_cite("서명되지 않은 허구 문서")]
    docs = [doc(id="real", title="연남 보고서")]
    assert calculate_citation_accuracy(citations, docs, [policy(title="안심창업")]) == 0.0
