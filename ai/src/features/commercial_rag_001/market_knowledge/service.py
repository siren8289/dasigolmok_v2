"""상권 지식 베이스(Market Knowledge Base) 처리 서비스.

상권 분석 보고서와 창업 지원 공고 문서를 수집하고,
적절한 크기로 쪼개며(Chunking), 검색을 위한 벡터 임베딩(Embedding)을 생성합니다.
초급 수준의 직관적인 코드로 작성되어 누구나 쉽게 이해할 수 있습니다.
"""
import math
import os
import re
from typing import List, Dict, Any
import numpy as np

from src.features.commercial_rag_001.schemas import DocumentChunk


# [무엇을 하는지] 기본 상권 분석 보고서 및 창업 지원 공고 원본 데이터를 정의합니다.
# [왜 필요한지] 외부 DB나 크롤러가 없어도 서울시 골목상권 데이터와 지원사업을 즉시 RAG로 검색할 수 있도록 기초 지식을 제공합니다.
RAW_KNOWLEDGE_DOCUMENTS = [
    {
        "id": "rep-mapo-yeonnam-2024q4",
        "title": "2024년 4분기 마포구 연남동 골목상권 동향 보고서",
        "doc_type": "market_report",
        "district": "마포구",
        "dong": "연남동",
        "industry": "한식음식점",
        "quarter": "2024-4",
        "source": "서울시 상권분석서비스",
        "source_url": "https://golmok.seoul.go.kr",
        "published_at": "2025-01-15",
        "content": (
            "마포구 연남동 상권은 경의선 숲길을 중심으로 20~30대 젊은 유동인구가 집중되는 골목상권입니다. "
            "한식 및 퓨전 음식점의 경우 주말 유동인구가 평일 대비 1.8배 높게 나타나며 체류 시간이 깁니다. "
            "다만 최근 신규 점포 유입으로 경쟁 강도가 심화되어 3년 이상 생존율은 점진적으로 감소하고 있습니다. "
            "임대료 수준은 연트럴파크 메인 거리 기준 3.3㎡당 평균 15만원 선을 형성하고 있어 고정비 부담 관리가 핵심입니다. "
            "테이크아웃 및 브런치 메뉴를 결합한 특화 매장의 재방문율이 상대적으로 높게 유지되고 있습니다."
        ),
    },
    {
        "id": "rep-gangnam-yeoksam-2024q4",
        "title": "2024년 4분기 강남구 역삼1동 오피스 상권 동향 보고서",
        "doc_type": "market_report",
        "district": "강남구",
        "dong": "역삼1동",
        "industry": "커피-음료",
        "quarter": "2024-4",
        "source": "서울 상권 활성화 연구원",
        "source_url": "https://seoul.economy.go.kr",
        "published_at": "2025-01-20",
        "content": (
            "강남구 역삼1동은 테헤란로 중심의 대형 오피스 빌딩 밀집 지역으로 직장인 점심 및 출퇴근 시간대 유동인구가 압도적입니다. "
            "커피 및 음료 업종은 오전 8시~9시, 오후 12시~1시 사이에 일일 매출의 65% 이상이 발생하는 전형적인 타임 집중형 상권입니다. "
            "반면 주말과 공휴일에는 유동인구가 평일 대비 75% 급감하므로 주말 운영 전략이 필요합니다. "
            "프랜차이즈 저가 커피 브랜드의 진입이 포화 상태에 이르러 객단가를 높일 수 있는 디저트 결합형 매장이 유리합니다."
        ),
    },
    {
        "id": "rep-jongno-ikseon-2024q4",
        "title": "2024년 4분기 종로구 종로1·2·3·4가동 관광·전통 상권 동향 보고서",
        "doc_type": "market_report",
        "district": "종로구",
        "dong": "종로1·2·3·4가동",
        "industry": "한식음식점",
        "quarter": "2024-4",
        "source": "서울관광재단 골목길 경제 연구소",
        "source_url": "https://sto.or.kr",
        "published_at": "2025-01-10",
        "content": (
            "종로 익선동 및 인사동 권역은 전통 한옥과 트렌디한 F&B가 결합된 상권으로 외국인 관광객 비중이 35%에 달합니다. "
            "한식 및 디저트 업종의 객단가가 서울 평균 대비 약 20% 높게 형성되어 있으며 SNS 홍보 효과가 매우 큽니다. "
            "골목 내 매장 면적이 협소하여 회전율 개선이 중요하며 계절별 관광객 수요 변동에 대비한 유연한 메뉴 구성이 요구됩니다."
        ),
    },
    {
        "id": "pol-seoul-safe-loan-2026",
        "title": "2026년 서울시 소상공인 안심창업 특별자금 지원 공고",
        "doc_type": "support_policy",
        "district": "전체",
        "industry": "전체",
        "source": "서울신용보증재단",
        "source_url": "https://www.seoulshinbo.co.kr",
        "published_at": "2026-01-02",
        "start_date": "2026-01-05",
        "end_date": "2026-12-31",
        "content": (
            "서울시 내에서 창업을 준비 중인 예비창업자 및 6개월 이내 초기 창업 소상공인을 위한 특별 보증 대출 지원사업입니다. "
            "최대 5천만원 한도 내에서 저금리(이차보전 연 2.0% 지원) 융자를 지원하며, 신용보증 비율 100%를 우대 적용합니다. "
            "창업 전 서울시 자영업지원센터의 상권분석 및 창업 아카데미 교육(12시간)을 수료한 사업자에게 우선 선발 혜택을 제공합니다."
        ),
    },
    {
        "id": "pol-mapo-youth-startup-2026",
        "title": "2026년 마포구 골목상권 활성화 청년창업 원스톱 지원사업",
        "doc_type": "support_policy",
        "district": "마포구",
        "industry": "일반음식점, 커피-음료",
        "source": "마포구청 일자리경제과",
        "source_url": "https://www.mapo.go.kr",
        "published_at": "2026-02-15",
        "start_date": "2026-03-01",
        "end_date": "2026-11-30",
        "content": (
            "마포구 내 연남동, 망원동, 서교동 등 골목상권에서 외식업 또는 카페 창업을 희망하는 만 39세 이하 청년을 지원합니다. "
            "점포 초기 시설 개선비 및 간판 제작비 최대 1천만원 무상 보조금을 지급하며, 전문가 1:1 상권 현장 컨설팅을 3회 제공합니다. "
            "모집 기간은 2026년 3월 1일부터 11월 30일까지 선착순 접수로 진행됩니다."
        ),
    },
    {
        "id": "pol-gangnam-incubating-2026",
        "title": "2026년 강남구 스타트업 및 소상공인 사업화 촉진 지원사업",
        "doc_type": "support_policy",
        "district": "강남구",
        "industry": "전체",
        "source": "강남구청 지역경제과",
        "source_url": "https://www.gangnam.go.kr",
        "published_at": "2026-01-10",
        "start_date": "2026-01-15",
        "end_date": "2026-12-15",
        "content": (
            "강남구 소재 신규 사업자 등록 예정자를 대상으로 임차료 지원금 월 50만원(최대 6개월) 및 디지털 마케팅 비용을 지원합니다. "
            "오피스 상권 내 타깃 고객 분석과 배달 앱 홍보비 등 실질적인 초기 정착을 돕는 프로그램입니다."
        ),
    },
    {
        "id": "pol-seoul-closed-special-2024",
        "title": "[종료] 2024년 서울시 청년 희망창업 특례보증 특별지원",
        "doc_type": "support_policy",
        "district": "전체",
        "industry": "전체",
        "source": "서울신용보증재단",
        "source_url": "https://www.seoulshinbo.co.kr",
        "published_at": "2024-01-10",
        "start_date": "2024-01-15",
        "end_date": "2024-06-30",
        "content": (
            "[신청 마감된 지원사업 공고] 2024년 상반기 한시적으로 운영된 청년 특례보증 사업으로 2024년 6월 30일부로 모든 접수가 종료되었습니다. "
            "본 공고는 현재 신청이 불가능하며, 종료된 사업이므로 신청 대상이 아닙니다."
        ),
    },
    {
        "id": "pol-mapo-closed-localbrand-2025",
        "title": "[종료] 2025년 상반기 마포 로컬브랜드 상권 도약 패키지 지원사업",
        "doc_type": "support_policy",
        "district": "마포구",
        "industry": "전체",
        "source": "마포구 상권활성화재단",
        "source_url": "https://www.mapo.go.kr",
        "published_at": "2025-01-05",
        "start_date": "2025-01-10",
        "end_date": "2025-04-30",
        "content": (
            "[신청 마감된 지원사업 공고] 2025년 4월 30일부로 접수 마감되었습니다. "
            "현재 신규 신청이 절대 불가능한 종료된 사업입니다."
        ),
    },
]


def load_market_knowledge_documents() -> List[Dict[str, Any]]:
    """[무엇을 하는지] 원본 상권 지식 문서 리스트를 반환합니다.

    [왜 필요한지] 상권 보고서와 정책 공고를 수집하고 메모리에서 다루기 위한 기본 데이터 소스로 사용합니다.
    """
    return RAW_KNOWLEDGE_DOCUMENTS


def chunk_text(text: str, max_chunk_size: int = 250, overlap: int = 50) -> List[str]:
    """[무엇을 하는지] 긴 텍스트를 문맥이 끊어지지 않도록 일정 크기로 나누고 겹치는 구간(오버랩)을 둡니다.

    [왜 필요한지] LLM이나 임베딩 모델이 한 번에 잘 이해할 수 있는 작은 크기(청크)로 가공하기 위함입니다.
    """
    text = text.strip()
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    start = 0
    text_len = len(text)
    step = max(1, max_chunk_size - overlap)

    while start < text_len:
        end = min(start + max_chunk_size, text_len)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= text_len:
            break
        start += step

    return chunks


def build_document_chunks() -> List[DocumentChunk]:
    """[무엇을 하는지] 원본 문서들을 읽어서 문장 단위로 쪼갠 DocumentChunk 객체 목록을 생성합니다.

    [왜 필요한지] 검색 시스템이 문서 내 특정 문단을 정확하게 찾아내고 출처 정보를 보존하기 위해서입니다.
    """
    chunk_list: List[DocumentChunk] = []
    raw_docs = load_market_knowledge_documents()

    for doc in raw_docs:
        chunks = chunk_text(doc["content"], max_chunk_size=250, overlap=40)
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{doc['id']}-c{idx+1}"
            chunk_obj = DocumentChunk(
                id=chunk_id,
                title=doc["title"],
                content=chunk,
                doc_type=doc["doc_type"],
                district=doc.get("district"),
                dong=doc.get("dong"),
                industry=doc.get("industry"),
                quarter=doc.get("quarter"),
                source=doc["source"],
                source_url=doc.get("source_url"),
                published_at=doc.get("published_at"),
                start_date=doc.get("start_date"),
                end_date=doc.get("end_date"),
                metadata={"original_doc_id": doc["id"], "chunk_index": idx + 1},
                score=0.0,
            )
            chunk_list.append(chunk_obj)

    return chunk_list


def _simple_local_embedding(text: str, dim: int = 64) -> List[float]:
    """[무엇을 하는지] 단어 해시를 활용하여 64차원의 정규화된 숫자 벡터를 만듭니다.

    [왜 필요한지] 외부 API 키가 없거나 네트워크 연결이 끊긴 환경에서도 일관된 코사인 유사도 검색을 지원하기 위함입니다.
    """
    vec = np.zeros(dim, dtype=np.float32)
    # 한글과 영문 단어를 추출합니다.
    tokens = re.findall(r"[\w가-힣]+", text.lower())
    if not tokens:
        return vec.tolist()

    for token in tokens:
        idx = abs(hash(token)) % dim
        vec[idx] += 1.0

    # L2 정규화 (길이를 1로 만듦)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()


def get_embedding(text: str) -> List[float]:
    """[무엇을 하는지] 텍스트를 받아 의미를 담은 숫자 배열(임베딩 벡터)을 돌려줍니다.

    [왜 필요한지] Gemini API를 최우선으로 사용하여 고품질 벡터를 만들고, 키가 없을 때도 로컬 벡터로 안전하게 동작하게 하기 위함입니다.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            # Gemini 임베딩 모델 호출
            result = client.models.embed_content(
                model="text-embedding-004",
                contents=text,
            )
            if hasattr(result, "embedding") and result.embedding:
                return list(result.embedding.values)
        except Exception as error:
            # 외부 API 호출 실패 시 로컬 임베딩으로 폴백합니다.
            pass

    return _simple_local_embedding(text, dim=64)


def compute_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """[무엇을 하는지] 두 벡터 사이의 코사인 유사도(-1.0 ~ 1.0)를 계산합니다.

    [왜 필요한지] 검색어와 문서 사이의 의미적 유사성을 측정하여 가장 관련 높은 문서를 찾기 위함입니다.
    """
    a = np.array(vec1, dtype=np.float32)
    b = np.array(vec2, dtype=np.float32)

    # 길이가 다르면 짧은 쪽에 맞추거나 안전하게 0 반환
    if len(a) != len(b):
        min_len = min(len(a), len(b))
        a = a[:min_len]
        b = b[:min_len]

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0

    cos_sim = float(np.dot(a, b) / (norm_a * norm_b))
    # 0.0 ~ 1.0 사이로 정규화
    return max(0.0, min(1.0, cos_sim))
