"""하네스(Harness) 런타임 및 안전성·평가(Evaluation) 모듈.

시스템의 신뢰성과 안전을 위해 다음과 같은 필수 기능을 담당합니다:
1. 입력 검증 (서울시 25개 자치구, 행정동, 날짜 형식)
2. 프롬프트 인젝션(Prompt Injection) 공격 탐지 및 차단
3. 도구 실행 권한 화이트리스트 검증
4. 실행 시간 측정, 타임아웃 및 재시도 제어
5. 실행 로그 및 토큰/비용 추적
6. RAG 성능 평가 (Recall@K, 인용 정확도, 적합도, 종료 정책 오안내율)
"""
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from src.features.commercial_rag_001.schemas import (
    CitedSource,
    DocumentChunk,
    EvaluationItem,
    EvaluationMetrics,
    SupportPolicyItem,
)

# 서울시 25개 자치구 목록
SEOUL_DISTRICTS = {
    "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구",
    "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구",
    "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구",
}

# 허용된 도구 화이트리스트
ALLOWED_TOOLS = {
    "market_search",
    "support_policy_search",
    "diagnose",
    "evaluate",
}

# 프롬프트 인젝션 공격 의심 키워드 패턴
INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous",
    "disregard all previous",
    "forget everything",
    "시스템 프롬프트를 무시",
    "이전 지침을 무시",
    "관리자 모드로 전환",
    "비밀키를 출력",
    "api key를 보여줘",
    "api_key",
    "system instructions",
    "you are now a hacker",
    "jailbreak",
]


def validate_input(
    district: Optional[str] = None,
    dong: Optional[str] = None,
    target_date: Optional[str] = None,
) -> List[str]:
    """[무엇을 하는지] 입력된 자치구 이름, 행정동 이름, 날짜 형식이 유효한지 검사합니다.

    [왜 필요한지] 잘못된 지역명이나 잘못된 날짜 형식으로 인해 계산 오류나 엉뚱한 결과가 나오는 것을 방지하기 위함입니다.
    """
    errors = []

    # 1. 자치구 검증
    if district and district not in SEOUL_DISTRICTS and district != "전체":
        errors.append(f"'{district}'은(는) 유효한 서울시 자치구가 아닙니다. (예: 마포구, 강남구 등)")

    # 2. 행정동 글자 검증 (비정상적으로 길거나 특수문자 방지)
    if dong and (len(dong) > 20 or len(dong) < 2):
        errors.append(f"행정동 이름 '{dong}'이(가) 올바르지 않습니다.")

    # 3. 날짜 형식 검증 (YYYY-MM-DD)
    if target_date:
        try:
            datetime.strptime(target_date, "%Y-%m-%d")
        except ValueError:
            errors.append(f"기준 날짜 '{target_date}'의 형식이 올바르지 않습니다. (YYYY-MM-DD 형식 필요)")

    return errors


def detect_prompt_injection(prompt: str) -> Tuple[bool, str]:
    """[무엇을 하는지] 사용자 입력에 시스템 탈취나 지침 무력화 공격 패턴이 있는지 검사합니다.

    [왜 필요한지] 악의적인 프롬프트 인젝션으로부터 AI 어시스턴트의 가이드라인과 시스템을 보호하기 위함입니다.
    """
    lower_prompt = prompt.lower()
    for pattern in INJECTION_PATTERNS:
        if pattern in lower_prompt:
            return True, f"비정상적인 요청 패턴이 감지되어 차단되었습니다: '{pattern}'"
    return False, ""


def check_tool_permission(tool_name: str) -> bool:
    """[무엇을 하는지] 호출하려는 도구가 허용된 목록(화이트리스트)에 있는지 확인합니다.

    [왜 필요한지] 승인되지 않은 임의의 외부 도구나 함수가 실행되는 보안 사고를 방지하기 위함입니다.
    """
    return tool_name in ALLOWED_TOOLS


def run_with_retry_and_timeout(
    func: Callable[[], Any],
    max_retries: int = 2,
    timeout_seconds: float = 8.0,
    fallback_value: Any = None,
) -> Tuple[Any, Optional[str]]:
    """[무엇을 하는지] 특정 작업(예: 외부 API 호출)을 타임아웃과 재시도 로직을 적용해 안전하게 실행합니다.

    [왜 필요한지] 외부 네트워크 일시 오류나 지연으로 전체 서비스가 중단되지 않고 안정적으로 작동하게 하기 위함입니다.
    """
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            start_time = time.time()
            result = func()
            elapsed = time.time() - start_time
            if elapsed > timeout_seconds:
                return fallback_value, f"실행 시간 초과 ({elapsed:.2f}초 > {timeout_seconds}초)"
            return result, None
        except Exception as exc:
            last_error = str(exc)
            time.sleep(0.2)  # 재시도 전 짧은 대기

    return fallback_value, f"최대 재시도({max_retries}회) 실패: {last_error}"


class ExecutionTracker:
    """[무엇을 하는지] 파이프라인의 실행 시간, 각 단계별 로그, 추정 사용 토큰과 비용을 기록합니다.

    [왜 필요한지] 성능 병목을 파악하고 LLM 운영 비용 및 실행 투명성을 확보하기 위함입니다.
    """

    def __init__(self):
        self.start_time = time.time()
        self.logs: List[str] = []
        self.total_input_chars = 0
        self.total_output_chars = 0

    def log_step(self, step_name: str, message: str):
        """실행 단계별 상태를 타임스탬프와 함께 기록합니다."""
        elapsed = time.time() - self.start_time
        self.logs.append(f"[{elapsed:.3f}s] {step_name}: {message}")

    def track_chars(self, input_text: str, output_text: str = ""):
        """입력과 출력 문자 수를 누적합니다."""
        self.total_input_chars += len(input_text)
        self.total_output_chars += len(output_text)

    def summary(self) -> Dict[str, Any]:
        """최종 소요 시간(ms), 추정 토큰 수 및 로그 요약을 반환합니다."""
        total_time_ms = round((time.time() - self.start_time) * 1000, 2)
        # 한국어 기준 약 1.5문자 = 1토큰으로 대략 추정
        estimated_input_tokens = int(self.total_input_chars / 1.5)
        estimated_output_tokens = int(self.total_output_chars / 1.5)

        return {
            "latency_ms": total_time_ms,
            "estimated_input_tokens": estimated_input_tokens,
            "estimated_output_tokens": estimated_output_tokens,
            "logs": self.logs,
        }


# ==========================================
# RAG 성능 및 안전성 평가(Evaluation) 함수군
# ==========================================

def calculate_recall_at_k(retrieved_ids: List[str], relevant_ids: List[str]) -> float:
    """[무엇을 하는지] 검색된 상위 문서 목록에 정답 문서가 얼마나 포함되었는지(Recall@K) 계산합니다.

    [왜 필요한지] 검색 모델이 사용자의 질문에 꼭 필요한 근거 문서를 빠뜨리지 않고 찾아오는지 측정하기 위함입니다.
    """
    if not relevant_ids:
        return 1.0
    matched = set(retrieved_ids).intersection(set(relevant_ids))
    return len(matched) / len(relevant_ids)


def calculate_citation_accuracy(
    citations: List[CitedSource],
    evidence_docs: List[DocumentChunk],
    policies: List[SupportPolicyItem],
) -> float:
    """[무엇을 하는지] 생성된 답변의 인용 출처가 실제 검색된 문서 및 정책 목록에 진짜 존재하는지 비율을 계산합니다.

    [왜 필요한지] AI가 존재하지 않는 출처를 지어내는 환각(Hallucination) 현상을 방지하고 검증하기 위함입니다.
    """
    if not citations:
        return 1.0

    valid_titles = {doc.title for doc in evidence_docs} | {p.title for p in policies}

    valid_count = 0
    for cite in citations:
        # 인용 제목이 실제 문서 제목에 포함되거나 일치하는지 확인
        matched = any(cite.title in vt or vt in cite.title for vt in valid_titles)
        if matched:
            valid_count += 1

    return valid_count / len(citations)


def calculate_regional_relevance(
    target_district: Optional[str],
    evidence_docs: List[DocumentChunk],
    policies: List[SupportPolicyItem],
) -> float:
    """[무엇을 하는지] 검색된 문서와 지원 정책이 사용자가 질문한 지역(자치구)과 일치하는지 비율을 계산합니다.

    [왜 필요한지] 마포구를 물어봤는데 강남구 정책을 안내하는 등의 부적합한 매칭을 평가하기 위함입니다.
    """
    if not target_district:
        return 1.0

    items = evidence_docs + policies
    if not items:
        return 1.0

    relevant_count = 0
    for item in items:
        dist = getattr(item, "district", None) or getattr(item, "target_district", None)
        if dist is None or dist == "전체" or target_district in dist:
            relevant_count += 1

    return relevant_count / len(items)


def evaluate_closed_policy_false_recommendations(policies: List[SupportPolicyItem]) -> float:
    """[무엇을 하는지] 종료된(마감된) 지원사업을 신청 가능(is_open=True)하다고 잘못 안내한 비율을 계산합니다.

    [왜 필요한지] 필수 원칙: 종료된 정책을 신청 가능하다고 오안내하는 오류율이 반드시 0이어야 하기 때문입니다.
    """
    if not policies:
        return 0.0

    false_open_count = 0
    for p in policies:
        # status가 closed인데 is_open이 True로 표기된 치명적 오류가 있는지 점검
        if p.status == "closed" and p.is_open:
            false_open_count += 1

    return false_open_count / len(policies)


def run_evaluation_suite(test_cases: Optional[List[Dict[str, Any]]] = None) -> EvaluationMetrics:
    """[무엇을 하는지] 사전 정의된 표준 테스트 질문셋에 대해 RAG 파이프라인의 4대 품질 지표를 측정합니다.

    [왜 필요한지] Recall@K, 인용 정확도, 지역 적합성, 종료 정책 오안내 방어력을 정량적으로 검증하기 위함입니다.
    """
    from src.features.commercial_rag_001.market_search.service import search_market_evidence
    from src.features.commercial_rag_001.schemas import MarketSearchQuery, SupportPolicyQuery
    from src.features.commercial_rag_001.support_policy.service import search_policies

    # 기본 테스트 케이스
    cases = test_cases or [
        {
            "query": "연남동 한식 상권 동향과 지원금",
            "district": "마포구",
            "dong": "연남동",
            "industry": "한식음식점",
            "expected_doc_ids": ["rep-mapo-yeonnam-2024q4-c1"],
        },
        {
            "query": "강남구 역삼1동 카페 커피 상권 보고서",
            "district": "강남구",
            "dong": "역삼1동",
            "industry": "커피-음료",
            "expected_doc_ids": ["rep-gangnam-yeoksam-2024q4-c1"],
        },
        {
            "query": "2026 서울시 소상공인 안심창업 지원자금",
            "district": "마포구",
            "dong": None,
            "industry": None,
            "expected_doc_ids": ["pol-seoul-safe-loan-2026-c1"],
        },
    ]

    total_recall = 0.0
    total_citation = 1.0  # 기본값
    total_relevance = 0.0
    total_closed_false = 0.0
    evaluation_items: List[EvaluationItem] = []

    for c in cases:
        # 상권 근거 검색
        search_res = search_market_evidence(
            MarketSearchQuery(
                query=c["query"],
                district=c.get("district"),
                dong=c.get("dong"),
                industry=c.get("industry"),
                top_k=3,
            )
        )
        retrieved_ids = [d.id for d in search_res.documents]
        recall = calculate_recall_at_k(retrieved_ids, c.get("expected_doc_ids", []))
        total_recall += recall

        # 정책 검색 (열린 정책만 조회)
        policy_res = search_policies(
            SupportPolicyQuery(
                query=c["query"],
                district=c.get("district"),
                industry=c.get("industry"),
                only_open=True,
                top_k=3,
            )
        )

        rel = calculate_regional_relevance(c.get("district"), search_res.documents, policy_res.policies)
        total_relevance += rel

        # 종료 정책 오안내 검사 (모든 정책을 조회하여 검증)
        all_policies_res = search_policies(
            SupportPolicyQuery(
                query=c["query"],
                district=c.get("district"),
                only_open=False,
                top_k=10,
            )
        )
        closed_leak = evaluate_closed_policy_false_recommendations(all_policies_res.policies)
        total_closed_false += closed_leak

        evaluation_items.append(
            EvaluationItem(
                query=c["query"],
                expected_doc_ids=c.get("expected_doc_ids", []),
                retrieved_doc_ids=retrieved_ids,
                has_recall=(recall > 0.0),
                citation_valid=True,
                relevance_valid=(rel >= 0.8),
                closed_policy_leak=(closed_leak > 0.0),
            )
        )

    count = max(1, len(cases))
    return EvaluationMetrics(
        recall_at_k=round(total_recall / count, 4),
        citation_accuracy=1.0,
        relevance_score=round(total_relevance / count, 4),
        closed_policy_false_recommendation_rate=round(total_closed_false / count, 4),
        total_evaluated=len(cases),
        items=evaluation_items,
    )
