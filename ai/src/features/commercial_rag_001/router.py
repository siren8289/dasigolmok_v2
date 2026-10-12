"""상권 분석 근거 RAG 및 창업 지원 정책 안내 기능 전용 API 라우터.

FastAPI의 APIRouter를 사용하여 신규 기능 전용 엔드포인트를 제공합니다.
"""
from fastapi import APIRouter, HTTPException

from src.features.commercial_rag_001.schemas import (
    CommercialRagRequest,
    CommercialRagResponse,
    MarketSearchQuery,
    MarketSearchResponse,
    SupportPolicyQuery,
    SupportPolicyResponse,
    EvaluationMetrics,
)
from src.features.commercial_rag_001.orchestration.workflow import execute_commercial_rag_workflow
from src.features.commercial_rag_001.market_search.service import search_market_evidence
from src.features.commercial_rag_001.support_policy.service import search_policies
from src.features.commercial_rag_001.harness.runtime import run_evaluation_suite

router = APIRouter(prefix="/api/v1/commercial-rag", tags=["Commercial RAG"])


@router.get("/health")
def health_check():
    """[무엇을 하는지] 상권 RAG 서비스의 동작 상태를 확인합니다.

    [왜 필요한지] 서비스 모니터링 및 컨테이너 헬스체크를 위해 필요합니다.
    """
    return {"status": "ok", "feature": "commercial_rag_001"}


@router.post("/ask", response_model=CommercialRagResponse)
def ask_commercial_rag_api(request: CommercialRagRequest):
    """[무엇을 하는지] 질문을 받아 검증, 검색, 조건 확인, RAG 설명 생성을 오케스트레이션하여 반환합니다.

    [왜 필요한지] 프론트엔드나 백엔드에서 사용자 상권/창업 질문을 한 번에 처리하기 위한 메인 API입니다.
    """
    try:
        response = execute_commercial_rag_workflow(request)
        return response
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG 워크플로우 실행 실패: {str(exc)}")


@router.post("/market-search", response_model=MarketSearchResponse)
def market_search_api(query: MarketSearchQuery):
    """[무엇을 하는지] 지역과 업종 조건에 맞는 상권 분석 보고서 근거를 검색하고 재순위화하여 반환합니다.

    [왜 필요한지] 상권 보고서 근거 문서만 독립적으로 조회하고자 할 때 사용합니다.
    """
    try:
        return search_market_evidence(query)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"상권 검색 실패: {str(exc)}")


@router.post("/support-policies", response_model=SupportPolicyResponse)
def support_policies_api(query: SupportPolicyQuery):
    """[무엇을 하는지] 자치구 및 업종별 맞춤 창업 지원 정책을 조회하고 신청 가능 여부를 판정합니다.

    [왜 필요한지] 현재 신청 가능한 지원금 및 컨설팅 공고만 빠르게 모아보기 위해 사용합니다.
    """
    try:
        return search_policies(query)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"정책 검색 실패: {str(exc)}")


@router.post("/evaluate", response_model=EvaluationMetrics)
def evaluate_api():
    """[무엇을 하는지] RAG 시스템의 4대 핵심 품질(Recall@K, 인용 정확도, 지역 적합성, 종료 정책 오안내율)을 평가합니다.

    [왜 필요한지] 시스템의 답변 품질과 안전성 지표를 정량적으로 모니터링하기 위해 사용합니다.
    """
    try:
        return run_evaluation_suite()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"평가 실행 실패: {str(exc)}")
