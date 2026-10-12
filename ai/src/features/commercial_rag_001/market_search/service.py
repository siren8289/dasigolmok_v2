"""상권 근거 검색(Market Evidence Search) 서비스.

PostgreSQL + pgvector 연동 인터페이스를 제공하며,
DB가 준비되지 않은 환경에서도 즉시 실행 가능한 인메모리 하이브리드 검색과 재순위화(Reranking)를 지원합니다.
"""
from typing import List, Optional, Dict, Any
import re

from src.features.commercial_rag_001.schemas import DocumentChunk, MarketSearchQuery, MarketSearchResponse
from src.features.commercial_rag_001.market_knowledge.service import (
    build_document_chunks,
    get_embedding,
    compute_cosine_similarity,
)

# 메모리에 청크 데이터를 캐싱하여 반복 생성을 방지합니다.
_CHUNKS_CACHE: Optional[List[DocumentChunk]] = None
_EMBEDDINGS_CACHE: Optional[Dict[str, List[float]]] = None


def get_cached_chunks() -> List[DocumentChunk]:
    """[무엇을 하는지] 지식 베이스의 모든 청크를 메모리에 준비해 둡니다.

    [왜 필요한지] 검색할 때마다 문서를 다시 쪼개지 않고 빠르게 조회하기 위함입니다.
    """
    global _CHUNKS_CACHE
    if _CHUNKS_CACHE is None:
        _CHUNKS_CACHE = build_document_chunks()
    return _CHUNKS_CACHE


def get_cached_chunk_embeddings() -> Dict[str, List[float]]:
    """[무엇을 하는지] 각 청크의 임베딩 벡터를 미리 계산하여 딕셔너리로 보관합니다.

    [왜 필요한지] 검색 요청마다 모든 문서의 임베딩을 다시 계산하면 느려지므로 미리 저장해 둡니다.
    """
    global _EMBEDDINGS_CACHE
    if _EMBEDDINGS_CACHE is None:
        chunks = get_cached_chunks()
        _EMBEDDINGS_CACHE = {}
        for chunk in chunks:
            # 본문 + 제목 + 지역 정보를 결합하여 임베딩을 만듭니다.
            combined_text = f"{chunk.title} {chunk.district or ''} {chunk.dong or ''} {chunk.industry or ''} {chunk.content}"
            _EMBEDDINGS_CACHE[chunk.id] = get_embedding(combined_text)
    return _EMBEDDINGS_CACHE


def search_pgvector(
    conn: Any,
    query_vector: List[float],
    district: Optional[str] = None,
    dong: Optional[str] = None,
    industry: Optional[str] = None,
    quarter: Optional[str] = None,
    top_k: int = 3,
) -> List[DocumentChunk]:
    """[무엇을 하는지] PostgreSQL의 pgvector 확장을 사용해 유사 문서를 검색하는 SQL을 실행합니다.

    [왜 필요한지] 대규모 프로덕션 환경에서 DB 엔진의 인덱싱(HNSW/IVFFlat)을 활용해 초고속 벡터 검색을 수행하기 위함입니다.
    """
    if conn is None:
        return []

    # pgvector 코사인 거리 연산자 (<=>) 사용 쿼리
    sql = """
        SELECT
            id, title, content, doc_type, district, dong, industry, quarter,
            source, source_url, published_at, start_date, end_date, metadata,
            1 - (embedding <=> %s::vector) AS similarity
        FROM market_knowledge_chunks
        WHERE (%s IS NULL OR district = %s)
          AND (%s IS NULL OR dong = %s)
          AND (%s IS NULL OR industry = %s)
          AND (%s IS NULL OR quarter = %s)
        ORDER BY similarity DESC
        LIMIT %s;
    """
    params = [
        str(query_vector),
        district, district,
        dong, dong,
        industry, industry,
        quarter, quarter,
        top_k,
    ]

    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        results = []
        for r in rows:
            results.append(DocumentChunk(
                id=r[0], title=r[1], content=r[2], doc_type=r[3],
                district=r[4], dong=r[5], industry=r[6], quarter=r[7],
                source=r[8], source_url=r[9], published_at=r[10],
                start_date=r[11], end_date=r[12], metadata=r[13] or {},
                score=round(float(r[14]), 4),
            ))
        return results
    except Exception as error:
        # DB 오류 발생 시 빈 리스트 반환 후 상위에서 로컬 검색으로 전환
        print("pgvector 검색 중 오류 발생:", error)
        return []


def rerank(
    documents: List[DocumentChunk],
    query: str,
    district: Optional[str] = None,
    dong: Optional[str] = None,
    industry: Optional[str] = None,
    top_k: int = 3,
) -> List[DocumentChunk]:
    """[무엇을 하는지] 검색된 문서들을 키워드 일치도와 메타데이터 가중치를 고려하여 재정렬(Reranking)합니다.

    [왜 필요한지] 벡터 유사도만으로는 놓칠 수 있는 특정 동(연남동), 구(마포구), 업종(한식)의 정확한 키워드 매칭을 보완하기 위함입니다.
    """
    query_tokens = set(re.findall(r"[\w가-힣]+", query.lower()))
    reranked = []

    for doc in documents:
        score = doc.score or 0.0

        # 1. 행정동 일치 가중치 (+0.3점)
        if dong and doc.dong and dong in doc.dong:
            score += 0.3

        # 2. 자치구 일치 가중치 (+0.2점)
        if district and doc.district and (district in doc.district or doc.district == "전체"):
            score += 0.2

        # 3. 업종 일치 가중치 (+0.2점)
        if industry and doc.industry and (industry in doc.industry or doc.industry == "전체"):
            score += 0.2

        # 4. 쿼리 키워드 출현 가중치
        doc_tokens = set(re.findall(r"[\w가-힣]+", (doc.title + " " + doc.content).lower()))
        matched_tokens = query_tokens.intersection(doc_tokens)
        if query_tokens:
            keyword_score = len(matched_tokens) / len(query_tokens)
            score += 0.2 * keyword_score

        # 점수 업데이트
        doc_copy = doc.model_copy()
        doc_copy.score = round(score, 4)
        reranked.append(doc_copy)

    # 점수 높은 순으로 정렬
    reranked.sort(key=lambda d: d.score or 0.0, reverse=True)
    return reranked[:top_k]


def search_market_evidence(query_obj: MarketSearchQuery) -> MarketSearchResponse:
    """[무엇을 하는지] 상권 질문에 대한 최적의 근거 문서들을 검색하고 재순위화하여 반환합니다.

    [왜 필요한지] 상권 진단 결과에 공공데이터 보고서의 구체적인 통계 및 실제 동향 근거를 덧붙이기 위함입니다.
    """
    chunks = get_cached_chunks()
    embeddings = get_cached_chunk_embeddings()

    # 1. 쿼리 임베딩 생성
    q_vec = get_embedding(query_obj.query)

    candidates: List[DocumentChunk] = []

    # 2. 1차 필터링 및 코사인 유사도 계산
    for chunk in chunks:
        # 상권 보고서 문서를 우선 대상으로 함
        if chunk.doc_type != "market_report":
            continue

        # 명시적 자치구 필터가 있으면 확인
        if query_obj.district and chunk.district and query_obj.district != chunk.district:
            continue

        c_vec = embeddings.get(chunk.id, [])
        sim = compute_cosine_similarity(q_vec, c_vec)

        chunk_item = chunk.model_copy()
        chunk_item.score = round(sim, 4)
        candidates.append(chunk_item)

    # 만약 필터 결과가 비어있다면 전체 상권 보고서에서 검색
    if not candidates:
        for chunk in chunks:
            if chunk.doc_type == "market_report":
                c_vec = embeddings.get(chunk.id, [])
                sim = compute_cosine_similarity(q_vec, c_vec)
                chunk_item = chunk.model_copy()
                chunk_item.score = round(sim, 4)
                candidates.append(chunk_item)

    # 3. Reranking 적용
    top_docs = rerank(
        documents=candidates,
        query=query_obj.query,
        district=query_obj.district,
        dong=query_obj.dong,
        industry=query_obj.industry,
        top_k=query_obj.top_k,
    )

    return MarketSearchResponse(
        documents=top_docs,
        total_count=len(top_docs),
    )
