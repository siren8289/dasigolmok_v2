"""상권 분석 근거 RAG 및 창업 지원 정책 안내 기능의 데이터 규격(스키마).

Pydantic 모델을 사용하여 입력과 출력 형태를 명확히 정의합니다.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """검색에 사용되는 쪼개진 문서(청크) 정보입니다."""
    id: str = Field(description="문서 고유 ID")
    title: str = Field(description="문서 제목")
    content: str = Field(description="문서 내용")
    doc_type: str = Field(description="문서 종류 (market_report: 상권 보고서, support_policy: 지원 정책)")
    district: Optional[str] = Field(default=None, description="해당 자치구 (예: 마포구)")
    dong: Optional[str] = Field(default=None, description="해당 행정동 (예: 연남동)")
    industry: Optional[str] = Field(default=None, description="해당 업종 (예: 한식음식점)")
    quarter: Optional[str] = Field(default=None, description="해당 분기 (예: 2024년 4분기)")
    source: str = Field(description="출처 기관 또는 보고서명 (예: 서울시 상권분석서비스)")
    source_url: Optional[str] = Field(default=None, description="출처 웹페이지 링크")
    published_at: Optional[str] = Field(default=None, description="발행일 또는 공고일 (YYYY-MM-DD)")
    start_date: Optional[str] = Field(default=None, description="모집 시작일 (YYYY-MM-DD)")
    end_date: Optional[str] = Field(default=None, description="모집 마감일 (YYYY-MM-DD)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="기타 부가 정보")
    score: Optional[float] = Field(default=0.0, description="검색 유사도 점수")


class MarketSearchQuery(BaseModel):
    """상권 근거 검색 요청 데이터입니다."""
    query: str = Field(description="검색 키워드 또는 질문")
    district: Optional[str] = Field(default=None, description="자치구 필터")
    dong: Optional[str] = Field(default=None, description="행정동 필터")
    industry: Optional[str] = Field(default=None, description="업종 필터")
    quarter: Optional[str] = Field(default=None, description="분기 필터")
    top_k: int = Field(default=3, description="가져올 최대 문서 수")


class MarketSearchResponse(BaseModel):
    """상권 근거 검색 결과 데이터입니다."""
    documents: List[DocumentChunk] = Field(default_factory=list, description="검색된 문서 목록")
    total_count: int = Field(default=0, description="검색된 총 문서 수")


class SupportPolicyItem(BaseModel):
    """창업 지원 정책 1건의 상세 정보입니다."""
    id: str = Field(description="지원 정책 ID")
    title: str = Field(description="지원 정책 명칭")
    organization: str = Field(description="주관 기관 (예: 서울신용보증재단)")
    target_district: Optional[str] = Field(default=None, description="지원 대상 자치구 (None이면 서울시 전역)")
    target_industry: Optional[str] = Field(default=None, description="지원 대상 업종 (None이면 전업종)")
    start_date: str = Field(description="모집 시작일 (YYYY-MM-DD)")
    end_date: str = Field(description="모집 종료일 (YYYY-MM-DD)")
    status: str = Field(description="상태 (open: 모집중, closed: 마감, upcoming: 접수예정)")
    is_open: bool = Field(description="현재 신청 가능 여부")
    support_amount: Optional[str] = Field(default=None, description="지원 규모 또는 혜택")
    description: str = Field(description="지원 내용 요약")
    eligibility: Optional[str] = Field(default=None, description="신청 자격")
    source_url: Optional[str] = Field(default=None, description="공고 상세 페이지 링크")
    score: Optional[float] = Field(default=0.0, description="검색 적합도 점수")


class SupportPolicyQuery(BaseModel):
    """지원 정책 검색 요청 데이터입니다."""
    query: str = Field(default="", description="검색 질문 또는 키워드")
    district: Optional[str] = Field(default=None, description="창업 희망 자치구")
    industry: Optional[str] = Field(default=None, description="창업 희망 업종")
    target_date: Optional[str] = Field(default=None, description="기준 확인 날짜 (YYYY-MM-DD)")
    only_open: bool = Field(default=True, description="신청 가능한(마감되지 않은) 공고만 조회할지 여부")
    top_k: int = Field(default=5, description="가져올 최대 정책 수")


class SupportPolicyResponse(BaseModel):
    """지원 정책 검색 결과 데이터입니다."""
    policies: List[SupportPolicyItem] = Field(default_factory=list, description="지원 정책 목록")
    total_count: int = Field(default=0, description="조회된 총 정책 수")


class CitedSource(BaseModel):
    """답변에 인용된 출처 정보입니다."""
    title: str = Field(description="문서 또는 정책 제목")
    source: str = Field(description="출처 기관명")
    doc_type: str = Field(description="문서 종류")
    date_info: Optional[str] = Field(default=None, description="발행일 또는 공고 기간")
    snippet: str = Field(description="인용된 핵심 내용 한 줄")


class CommercialRagRequest(BaseModel):
    """상권 및 정책 종합 안내(RAG) 사용자 질문 요청 데이터입니다."""
    question: str = Field(description="사용자의 질문 내용")
    district: Optional[str] = Field(default=None, description="희망 자치구")
    dong: Optional[str] = Field(default=None, description="희망 행정동")
    industry: Optional[str] = Field(default=None, description="희망 업종")
    target_date: Optional[str] = Field(default=None, description="기준 날짜 (YYYY-MM-DD)")
    top_k: int = Field(default=3, description="참조할 문서 수")


class CommercialRagResponse(BaseModel):
    """상권 및 정책 종합 안내(RAG) 최종 응답 데이터입니다."""
    question: str = Field(description="원래 사용자 질문")
    answer: str = Field(description="AI 생성 종합 안내 답변")
    intent: str = Field(description="판별된 의도 (market_analysis, support_policy, hybrid)")
    district: Optional[str] = Field(default=None, description="분석 자치구")
    dong: Optional[str] = Field(default=None, description="분석 행정동")
    industry: Optional[str] = Field(default=None, description="분석 업종")
    market_diagnosis: Optional[Dict[str, Any]] = Field(default=None, description="기존 ML/DL 상권 진단 결과")
    evidence_documents: List[DocumentChunk] = Field(default_factory=list, description="참조된 상권 근거 문서")
    policies: List[SupportPolicyItem] = Field(default_factory=list, description="참조된 창업 지원 정책")
    citations: List[CitedSource] = Field(default_factory=list, description="출처 인용 목록")
    warnings: List[str] = Field(default_factory=list, description="안전 및 주의 안내 문구")
    execution_metadata: Dict[str, Any] = Field(default_factory=dict, description="실행 시간 및 토큰/추적 정보")


class EvaluationItem(BaseModel):
    """평가 1건에 대한 상세 결과입니다."""
    query: str
    expected_doc_ids: List[str]
    retrieved_doc_ids: List[str]
    has_recall: bool
    citation_valid: bool
    relevance_valid: bool
    closed_policy_leak: bool


class EvaluationMetrics(BaseModel):
    """RAG 시스템 품질 및 안전성 평가 지표입니다."""
    recall_at_k: float = Field(description="Recall@K (상위 K개 문서에 정답 포함 비율)")
    citation_accuracy: float = Field(description="출처 인용 정확도 (인용된 출처가 실제 문서에 존재하는 비율)")
    relevance_score: float = Field(description="지역 및 업종 적합성 비율")
    closed_policy_false_recommendation_rate: float = Field(description="종료된 정책을 신청 가능하다고 잘못 안내한 비율 (0.0이어야 함)")
    total_evaluated: int = Field(description="총 평가 질문 수")
    items: List[EvaluationItem] = Field(default_factory=list, description="개별 평가 세부 결과")
