"""오케스트레이션(Orchestration) 워크플로우 모듈.

LangGraph 구조를 기반으로 사용자 질문의 의도를 분기하고,
[검증] -> [의도분류] -> [상권검색 / 정책검색 조건부 분기] -> [종합 답변 생성]
순서로 파이프라인을 체계적으로 조율합니다.
"""
from typing import Any, Dict, List, Optional
import re

from src.features.commercial_rag_001.schemas import (
    CommercialRagRequest,
    CommercialRagResponse,
    DocumentChunk,
    MarketSearchQuery,
    SupportPolicyItem,
    SupportPolicyQuery,
)
from src.features.commercial_rag_001.harness.runtime import (
    detect_prompt_injection,
    validate_input,
    check_tool_permission,
    ExecutionTracker,
)
from src.features.commercial_rag_001.market_search.service import search_market_evidence
from src.features.commercial_rag_001.support_policy.service import search_policies
from src.features.commercial_rag_001.commercial_guidance.service import (
    generate_guidance,
    get_market_diagnosis_data,
)


def classify_question_intent(question: str) -> str:
    """[무엇을 하는지] 사용자 질문을 분석하여 상권 분석, 지원 정책, 또는 둘 다(복합)인지 분류합니다.

    [왜 필요한지] 질문의 목적에 맞는 최적의 검색 도구와 노드로 분기(Routing)하여 불필요한 계산을 줄이기 위함입니다.
    """
    q = question.lower()

    # 상권 분석 관련 키워드
    market_keywords = ["상권", "매출", "폐업", "유동인구", "경쟁", "동향", "생존율", "연남동", "역삼동", "진단", "분석"]
    # 창업 지원 정책 관련 키워드
    policy_keywords = ["지원금", "정책", "보조금", "대출", "자금", "지원사업", "공고", "신청", "자격", "모집", "특례보증", "스마트상점"]

    has_market = any(k in q for k in market_keywords)
    has_policy = any(k in q for k in policy_keywords)

    if has_market and has_policy:
        return "hybrid"
    elif has_policy:
        return "support_policy"
    elif has_market:
        return "market_analysis"
    else:
        # 키워드가 뚜렷하지 않은 경우 기본적으로 종합(hybrid)으로 처리
        return "hybrid"


class CommercialRagWorkflowState(dict):
    """LangGraph 상태 객체 (딕셔너리 기반)"""
    pass


# ==========================================
# 워크플로우 각 노드(Node) 함수들
# ==========================================

def node_validate(state: Dict[str, Any]) -> Dict[str, Any]:
    """[무엇을 하는지] 1단계: 프롬프트 인젝션 공격 여부와 입력값(지역명, 날짜)을 검증합니다.

    [왜 필요한지] 비정상적인 요청이나 보안 공격을 입구에서 즉시 차단하기 위함입니다.
    """
    tracker: ExecutionTracker = state["tracker"]
    tracker.log_step("node_validate", "입력값 및 보안 검사 시작")

    # 프롬프트 인젝션 검사
    is_injection, msg = detect_prompt_injection(state["question"])
    if is_injection:
        state["is_blocked"] = True
        state["block_reason"] = msg
        tracker.log_step("node_validate", f"보안 차단: {msg}")
        return state

    # 지역 및 날짜 검증
    errors = validate_input(
        district=state.get("district"),
        dong=state.get("dong"),
        target_date=state.get("target_date"),
    )
    if errors:
        state["validation_warnings"].extend(errors)
        tracker.log_step("node_validate", f"입력 경고: {', '.join(errors)}")

    return state


def node_classify(state: Dict[str, Any]) -> Dict[str, Any]:
    """[무엇을 하는지] 2단계: 질문의 의도를 분석하여 intent를 상태에 기록합니다.

    [왜 필요한지] 상권 검색과 정책 검색 중 필요한 작업으로 조건부 분기하기 위함입니다.
    """
    if state.get("is_blocked"):
        return state

    tracker: ExecutionTracker = state["tracker"]
    intent = classify_question_intent(state["question"])
    state["intent"] = intent
    tracker.log_step("node_classify", f"의도 판별 완료: '{intent}'")
    return state


def node_market_search(state: Dict[str, Any]) -> Dict[str, Any]:
    """[무엇을 하는지] 3-A단계: 상권 동향 보고서를 검색하고 기존 ML/DL 상권 진단 수치를 조회합니다.

    [왜 필요한지] 상권 분석 질문에 필요한 통계 및 현장 근거 문서를 수집하기 위함입니다.
    """
    if state.get("is_blocked"):
        return state

    tracker: ExecutionTracker = state["tracker"]
    if not check_tool_permission("market_search"):
        tracker.log_step("node_market_search", "도구 실행 권한 없음")
        return state

    tracker.log_step("node_market_search", "상권 근거 검색 실행")

    # 1. 상권 근거 검색
    search_res = search_market_evidence(
        MarketSearchQuery(
            query=state["question"],
            district=state.get("district"),
            dong=state.get("dong"),
            industry=state.get("industry"),
            top_k=state.get("top_k", 3),
        )
    )
    state["evidence_docs"] = search_res.documents

    # 2. 기존 상권 ML/DL 모델 진단 데이터 조회
    if state.get("dong") and state.get("industry"):
        diag = get_market_diagnosis_data(
            district=state.get("district"),
            dong=state.get("dong"),
            industry=state.get("industry"),
        )
        state["market_diagnosis"] = diag
        tracker.log_step("node_market_search", "기존 상권 ML/DL 진단 데이터 결합 완료")

    return state


def node_policy_search(state: Dict[str, Any]) -> Dict[str, Any]:
    """[무엇을 하는지] 3-B단계: 자치구 및 업종 조건에 맞으며 '현재 신청 가능한' 지원사업을 검색합니다.

    [왜 필요한지] 사장님이 바로 지원받을 수 있는 최신 보조금 및 대출 혜택을 제공하기 위함입니다.
    """
    if state.get("is_blocked"):
        return state

    tracker: ExecutionTracker = state["tracker"]
    if not check_tool_permission("support_policy_search"):
        tracker.log_step("node_policy_search", "도구 실행 권한 없음")
        return state

    tracker.log_step("node_policy_search", "창업 지원 정책 검색 실행")

    policy_res = search_policies(
        SupportPolicyQuery(
            query=state["question"],
            district=state.get("district"),
            industry=state.get("industry"),
            target_date=state.get("target_date"),
            only_open=True,  # 마감된 지원사업은 신청 목록에서 엄격 제외
            top_k=state.get("top_k", 3),
        )
    )
    state["policies"] = policy_res.policies
    return state


def node_generate_guidance(state: Dict[str, Any]) -> Dict[str, Any]:
    """[무엇을 하는지] 4단계: 수집된 모든 근거(보고서, 정책, 진단수치)를 결합하여 최종 RAG 답변을 만듭니다.

    [왜 필요한지] 출처 인용과 안전 주의사항이 반영된 완성도 높은 안내를 사용자에게 전달하기 위함입니다.
    """
    tracker: ExecutionTracker = state["tracker"]

    # 보안 차단된 경우
    if state.get("is_blocked"):
        state["final_answer"] = (
            "안내를 진행할 수 없습니다. "
            f"사유: {state.get('block_reason', '안전 정책 위반 요청입니다.')}"
        )
        return state

    tracker.log_step("node_generate_guidance", "종합 안내 답변 및 출처 생성 시작")

    answer, citations, warnings = generate_guidance(
        question=state["question"],
        district=state.get("district"),
        dong=state.get("dong"),
        industry=state.get("industry"),
        diagnosis=state.get("market_diagnosis"),
        evidence_docs=state.get("evidence_docs", []),
        policies=state.get("policies", []),
    )

    state["final_answer"] = answer
    state["citations"] = citations
    state["warnings"].extend(warnings)
    if state.get("validation_warnings"):
        state["warnings"].extend(state["validation_warnings"])

    tracker.track_chars(state["question"], answer)
    tracker.log_step("node_generate_guidance", "종합 안내 생성 완료")
    return state


def execute_commercial_rag_workflow(request: CommercialRagRequest) -> CommercialRagResponse:
    """[무엇을 하는지] LangGraph 워크플로우 흐름에 따라 전체 과정을 실행하고 결과를 응답 객체로 반환합니다.

    [왜 필요한지] API 라우터나 다른 서비스에서 호출할 수 있는 메인 실행 진입점입니다.
    """
    tracker = ExecutionTracker()

    # 초기 상태 구성
    state: Dict[str, Any] = {
        "question": request.question,
        "district": request.district,
        "dong": request.dong,
        "industry": request.industry,
        "target_date": request.target_date,
        "top_k": request.top_k,
        "tracker": tracker,
        "intent": "hybrid",
        "is_blocked": False,
        "block_reason": "",
        "validation_warnings": [],
        "evidence_docs": [],
        "policies": [],
        "market_diagnosis": None,
        "final_answer": "",
        "citations": [],
        "warnings": [],
    }

    # 1. 입력 및 보안 검증
    state = node_validate(state)

    if not state.get("is_blocked"):
        # 2. 질문 의도 분류
        state = node_classify(state)
        intent = state.get("intent", "hybrid")

        # 3. 의도에 따른 조건부 실행 분기
        if intent == "market_analysis":
            state = node_market_search(state)
        elif intent == "support_policy":
            state = node_policy_search(state)
        else:  # hybrid
            state = node_market_search(state)
            state = node_policy_search(state)

    # 4. 종합 안내 답변 생성
    state = node_generate_guidance(state)

    # 5. 실행 추적 요약
    exec_meta = tracker.summary()

    return CommercialRagResponse(
        question=request.question,
        answer=state.get("final_answer", ""),
        intent=state.get("intent", "hybrid"),
        district=request.district,
        dong=request.dong,
        industry=request.industry,
        market_diagnosis=state.get("market_diagnosis"),
        evidence_documents=state.get("evidence_docs", []),
        policies=state.get("policies", []),
        citations=state.get("citations", []),
        warnings=state.get("warnings", []),
        execution_metadata=exec_meta,
    )
