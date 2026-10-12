"""상권 분석 근거 RAG 및 창업 지원 정책 안내 기능 (Feature 001).

이 패키지는 다음 핵심 컴포넌트를 포함합니다:
- schemas: 요청 및 응답 데이터 규격
- market_knowledge: 상권 보고서·지원사업 수집, 청킹, 임베딩
- market_search: 상권 근거 검색 및 Reranking
- support_policy: 창업 지원 정책 검색 및 기간·조건 확인
- commercial_guidance: 상권 진단 결합 RAG 설명 및 출처 인용
- orchestration: LangGraph 기반 질문 분기 및 실행 워크플로우
- harness: 입력 검증, 프롬프트 인젝션 방어, 실행 추적, 성능 평가
- router: 기능 전용 FastAPI 라우터
"""
from src.features.commercial_rag_001.router import router

__all__ = ["router"]
