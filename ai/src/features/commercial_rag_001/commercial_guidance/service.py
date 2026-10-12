"""상권 및 정책 종합 안내(Commercial Guidance RAG) 서비스.

기존 상권 진단(ML 폐업률 + DL 매출 예측)과 검색된 상권 보고서 근거,
그리고 창업 지원 정책을 하나로 결합하여 사장님을 위한 신뢰성 있는 맞춤 안내를 생성합니다.
출처 인용(Citation)을 명시하며, 예측치를 확정된 미래 결과로 단정 짓지 않습니다.
"""
import os
from typing import Any, Dict, List, Optional, Tuple

from src.features.commercial_rag_001.schemas import (
    CitedSource,
    DocumentChunk,
    SupportPolicyItem,
)
from src.service import diagnose as base_diagnose

# 법적 고지 및 안전 안내 문구
MANDATORY_DISCLAIMER = (
    "※ 안내 사항: 본 상권 분석의 예상 폐업률 및 점포당 매출은 서울시 상권 공공데이터 기반의 통계적 추정치이며, "
    "확정된 미래 결과나 수익을 보장하지 않습니다. 실제 창업 시 반드시 현장 실사와 임대차 계약 조건을 면밀히 확인하시기 바랍니다."
)


def get_market_diagnosis_data(district: Optional[str], dong: Optional[str], industry: Optional[str]) -> Optional[Dict[str, Any]]:
    """[무엇을 하는지] 기존 dasiGolmok 상권 진단 함수(diagnose)를 호출하여 ML 폐업률, DL 매출, 위험 등급을 가져옵니다.

    [왜 필요한지] 기존 시스템의 검증된 머신러닝/딥러닝 모델 계산 결과를 RAG 설명에 유기적으로 결합하기 위함입니다.
    """
    if not (dong and industry):
        return None

    request_payload = {
        "district": district or "마포구",
        "dong": dong,
        "industry": industry,
    }
    result = base_diagnose(request_payload)
    if "error" in result:
        return None
    return result


def extract_citations(
    evidence_docs: List[DocumentChunk],
    policies: List[SupportPolicyItem],
) -> List[CitedSource]:
    """[무엇을 하는지] 참조된 보고서 청크와 지원 정책들로부터 출처 목록(CitedSource)을 구성합니다.

    [왜 필요한지] 답변의 신뢰도를 높이고 사용자가 출처 공고 및 보고서의 원본 정보를 투명하게 확인할 수 있도록 하기 위함입니다.
    """
    citations = []

    # 1. 상권 보고서 인용 출처
    for doc in evidence_docs:
        snippet = doc.content[:120] + "..." if len(doc.content) > 120 else doc.content
        citations.append(
            CitedSource(
                title=doc.title,
                source=doc.source,
                doc_type="상권 분석 보고서",
                date_info=doc.published_at or doc.quarter,
                snippet=snippet,
            )
        )

    # 2. 지원 정책 인용 출처
    for p in policies:
        status_text = "접수 중" if p.is_open else "접수 마감"
        date_range = f"{p.start_date} ~ {p.end_date} ({status_text})"
        citations.append(
            CitedSource(
                title=p.title,
                source=p.organization,
                doc_type="창업 지원 정책",
                date_info=date_range,
                snippet=p.description,
            )
        )

    return citations


def build_fallback_rag_answer(
    question: str,
    district: Optional[str],
    dong: Optional[str],
    industry: Optional[str],
    diagnosis: Optional[Dict[str, Any]],
    evidence_docs: List[DocumentChunk],
    policies: List[SupportPolicyItem],
) -> str:
    """[무엇을 하는지] LLM API를 호출하지 못할 때 템플릿 기반으로 사실에 입각한 정교한 종합 가이드라인 답변을 만듭니다.

    [왜 필요한지] 외부 API 장애나 API 키 부재 시에도 사용자가 정확한 진단과 정책 정보를 즉시 얻을 수 있도록 보장하기 위함입니다.
    """
    lines = []

    target_name = f"{district or ''} {dong or ''} {industry or ''}".strip()
    if target_name:
        lines.append(f"[{target_name} 상권 분석 및 창업 지원 안내]")
    else:
        lines.append("[골목 상권 분석 및 창업 지원 종합 안내]")
    lines.append("")

    # 1. 기존 상권 진단 수치 요약
    if diagnosis:
        status_kor = {"stable": "안정", "warning": "주의", "danger": "위험"}.get(diagnosis.get("status"), "보통")
        lines.append("■ 상권 지표 진단 (공공데이터 모델 추정):")
        lines.append(f"- 상권 위험 단계: '{status_kor}' 단계 (상권변화: {diagnosis.get('change_name', '일반')})")
        lines.append(f"- 최근 실제 폐업률: {diagnosis.get('close_rate')}% | AI 예측 폐업률: 약 {diagnosis.get('ml_close_rate')}%")
        lines.append(f"- AI 예상 점포당 월매출: 약 {diagnosis.get('dl_sales_per_store')}만원")
        lines.append("")

    # 2. 상권 동향 보고서 근거 요약
    if evidence_docs:
        lines.append("■ 현장 상권 동향 및 특성 (출처 기반 근거):")
        for idx, doc in enumerate(evidence_docs, start=1):
            lines.append(f"({idx}) {doc.title} [{doc.source}]:")
            lines.append(f"    \"{doc.content.strip()}\"")
        lines.append("")

    # 3. 창업 지원 정책 안내
    if policies:
        lines.append("■ 신청 가능한 맞춤 창업 지원 정책:")
        open_policies = [p for p in policies if p.is_open]
        closed_policies = [p for p in policies if not p.is_open]

        if open_policies:
            for idx, p in enumerate(open_policies, start=1):
                lines.append(f"[{idx}] {p.title} (주관: {p.organization})")
                lines.append(f"    - 신청 기간: {p.start_date} ~ {p.end_date} (현재 접수 중)")
                if p.support_amount:
                    lines.append(f"    - 지원 혜택: {p.support_amount}")
                lines.append(f"    - 주요 내용: {p.description}")
        else:
            lines.append("- 현재 모집 중인 해당 조건의 지원사업이 없습니다.")

        # 마감된 정책이 목록에 포함된 경우(사용자가 문의했을 때) 명확한 마감 경고
        if closed_policies:
            lines.append("")
            lines.append("※ [주의: 접수 마감된 사업]")
            for p in closed_policies:
                lines.append(f"- {p.title}: 모집 기간({p.start_date} ~ {p.end_date})이 종료되어 현재 신청이 불가능합니다.")
        lines.append("")

    lines.append(MANDATORY_DISCLAIMER)
    return "\n".join(lines)


def generate_llm_rag_answer(
    prompt_context: str,
    question: str,
) -> Optional[str]:
    """[무엇을 하는지] Google Gemini LLM을 호출하여 사장님 눈높이에 맞춘 친절한 RAG 문장을 생성합니다.

    [왜 필요한지] 정형화된 데이터와 보고서 근거를 결합해 자연스럽고 이해하기 쉬운 상담형 답변을 제공하기 위함입니다.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return None

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=10000),
        )
        system_instruction = (
            "너는 서울시 소상공인 골목상권 창업 상담 전문 AI 어시스턴트다.\n"
            "주어진 근거 데이터(상권 진단 수치, 보고서, 지원 정책)에만 기반하여 사실 그대로 답변하라.\n"
            "규칙 1: 종료된(마감된) 지원사업을 절대 신청 가능하다고 안내하지 마라.\n"
            "규칙 2: 예상 매출과 폐업률은 확정된 미래 결과가 아니라 공공데이터 기반 통계 추정치임을 반드시 밝혀라.\n"
            "규칙 3: 인용한 근거의 출처([출처: ...])를 자연스럽게 명시하라.\n"
            "규칙 4: 답변 끝에 현장 실사와 계약 검토가 필수라는 안전 유의 문구를 포함하라."
        )

        full_prompt = f"{system_instruction}\n\n[참고 데이터]\n{prompt_context}\n\n[사용자 질문]\n{question}"
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=full_prompt,
        )
        if response.text:
            return response.text.strip()
    except Exception as error:
        print("Gemini RAG 호출 실패 (폴백 사용):", error)

    return None


def generate_guidance(
    question: str,
    district: Optional[str] = None,
    dong: Optional[str] = None,
    industry: Optional[str] = None,
    diagnosis: Optional[Dict[str, Any]] = None,
    evidence_docs: Optional[List[DocumentChunk]] = None,
    policies: Optional[List[SupportPolicyItem]] = None,
) -> Tuple[str, List[CitedSource], List[str]]:
    """[무엇을 하는지] 수집된 모든 정보(상권진단, 근거 보고서, 지원 정책)를 조합하여 최종 RAG 답변을 완성합니다.

    [왜 필요한지] 사용자 질문에 대해 출처 인용과 안전 주의사항이 완비된 고품질 맞춤형 안내를 반환하기 위함입니다.
    """
    docs = evidence_docs or []
    pols = policies or []

    # 1. 출처 인용 목록 구성
    citations = extract_citations(docs, pols)

    # 2. 필수 경고 목록 구성
    warnings = [
        "예상 폐업률 및 매출은 통계적 추정치이며 실제 결과를 보장하지 않습니다.",
        "창업 지원사업은 예산 소진 시 조기 마감될 수 있으므로 주관 기관 공식 홈페이지에서 최종 확인이 필요합니다.",
    ]

    # 3. 답변 본문 생성 (Gemini 호출 시도 -> 실패 시 템플릿 폴백)
    fallback_text = build_fallback_rag_answer(
        question=question,
        district=district,
        dong=dong,
        industry=industry,
        diagnosis=diagnosis,
        evidence_docs=docs,
        policies=pols,
    )

    llm_text = generate_llm_rag_answer(fallback_text, question)
    final_answer = llm_text if llm_text else fallback_text

    return final_answer, citations, warnings
