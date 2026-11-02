"""RG02 지식 베이스 청킹·임베딩."""
import pytest

from rg_support import install_genai
from src.features.commercial_rag_001.market_knowledge.service import (
    build_document_chunks,
    chunk_text,
    compute_cosine_similarity,
    get_embedding,
    load_market_knowledge_documents,
)


def test_RG02_001():
    """원본 지식 문서에 상권 보고서와 지원사업이 함께 있다."""
    docs = load_market_knowledge_documents()
    types = {doc["doc_type"] for doc in docs}
    assert "market_report" in types
    assert "support_policy" in types
    assert len(docs) >= 2


def test_RG02_002():
    """청크 doc_type 이 원본 market_report/support_policy 를 유지한다."""
    chunks = build_document_chunks()
    types = {chunk.doc_type for chunk in chunks}
    assert types == {"market_report", "support_policy"}
    reports = [chunk for chunk in chunks if chunk.doc_type == "market_report"]
    policies = [chunk for chunk in chunks if chunk.doc_type == "support_policy"]
    assert reports and policies


def test_RG02_003():
    """연남동 보고서 청크는 district=마포구, dong=연남동 으로 분리된다."""
    chunks = [
        chunk
        for chunk in build_document_chunks()
        if chunk.metadata.get("original_doc_id") == "rep-mapo-yeonnam-2024q4"
    ]
    assert chunks
    assert all(chunk.district == "마포구" and chunk.dong == "연남동" for chunk in chunks)


def test_RG02_004():
    """연남동 보고서 청크 industry 가 한식음식점으로 보존된다."""
    chunks = [
        chunk
        for chunk in build_document_chunks()
        if chunk.metadata.get("original_doc_id") == "rep-mapo-yeonnam-2024q4"
    ]
    assert chunks
    assert all(chunk.industry == "한식음식점" for chunk in chunks)


def test_RG02_005():
    """연남동 보고서 청크 quarter 가 2024-4 로 보존된다."""
    chunks = [
        chunk
        for chunk in build_document_chunks()
        if chunk.metadata.get("original_doc_id") == "rep-mapo-yeonnam-2024q4"
    ]
    assert chunks
    assert all(chunk.quarter == "2024-4" for chunk in chunks)


def test_RG02_006():
    """출처 URL https://golmok.seoul.go.kr 이 청크에 보존된다."""
    chunks = [
        chunk
        for chunk in build_document_chunks()
        if chunk.metadata.get("original_doc_id") == "rep-mapo-yeonnam-2024q4"
    ]
    assert chunks
    assert all(chunk.source_url == "https://golmok.seoul.go.kr" for chunk in chunks)


def test_RG02_007():
    """안심창업 공고 청크가 start_date=2026-01-05, end_date=2026-12-31 을 유지한다."""
    chunks = [
        chunk
        for chunk in build_document_chunks()
        if chunk.metadata.get("original_doc_id") == "pol-seoul-safe-loan-2026"
    ]
    assert chunks
    assert all(chunk.start_date == "2026-01-05" and chunk.end_date == "2026-12-31" for chunk in chunks)


def test_RG02_008():
    """max_chunk_size 보다 짧은 본문은 청크 1개다."""
    chunks = chunk_text("짧은 상권 문장입니다.", max_chunk_size=250, overlap=50)
    assert chunks == ["짧은 상권 문장입니다."]


def test_RG02_009():
    """길이가 max_chunk_size 와 같은 본문은 청크 1개다."""
    text = "가" * 250
    chunks = chunk_text(text, max_chunk_size=250, overlap=50)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_RG02_010():
    """max_chunk_size 를 넘는 본문은 중첩 청크가 2개 이상이다."""
    text = "나" * 400
    chunks = chunk_text(text, max_chunk_size=250, overlap=50)
    assert len(chunks) >= 2
    assert all(len(chunk) <= 250 for chunk in chunks)


def test_RG02_011():
    """overlap=50 이면 인접 청크 본문이 50자 겹친다."""
    text = "다" * 400
    chunks = chunk_text(text, max_chunk_size=250, overlap=50)
    assert len(chunks) >= 2
    assert chunks[0][-50:] == chunks[1][:50]


def test_RG02_012():
    """0글자·공백 문서는 검색 가능한 빈 청크를 만들면 안 된다."""
    chunks = chunk_text("   ")
    if not chunks or any(not chunk.strip() for chunk in chunks):
        pytest.fail(f"공백 문서가 검색 청크로 남음: {chunks!r}")


def test_RG02_013():
    """chunk_size 와 overlap 이 같으면 입력 거절이어야 하고 무한 생성하면 안 된다."""
    try:
        chunks = chunk_text("가" * 400, max_chunk_size=250, overlap=250)
    except (ValueError, OverflowError):
        return
    pytest.fail(f"chunk_size=overlap 인데 거절하지 않고 {len(chunks)}개 청크를 생성함")


def test_RG02_014():
    """음수 chunk_size 는 잘못된 슬라이스를 만들지 않고 거절되어야 한다."""
    try:
        chunks = chunk_text("가" * 20, max_chunk_size=-10, overlap=0)
    except (ValueError, OverflowError):
        return
    pytest.fail(f"chunk_size=-10 이 거절되지 않고 {len(chunks)}개 청크를 생성함: {chunks!r}")


def test_RG02_015():
    """한 문서의 모든 청크가 title, source, dong 을 유지한다."""
    grouped = {}
    for chunk in build_document_chunks():
        grouped.setdefault(chunk.metadata["original_doc_id"], []).append(chunk)
    multi = [items for items in grouped.values() if len(items) >= 2]
    assert multi
    for items in multi:
        titles = {item.title for item in items}
        sources = {item.source for item in items}
        dongs = {item.dong for item in items}
        assert len(titles) == 1 and len(sources) == 1 and len(dongs) == 1
        assert items[0].title and items[0].source


def test_RG02_016():
    """build_document_chunks 청크 ID 가 중복되지 않는다."""
    ids = [chunk.id for chunk in build_document_chunks()]
    assert len(ids) == len(set(ids))
    assert ids


def test_RG02_017():
    """API 키 없이 get_embedding 은 64차원 로컬 벡터를 반환한다."""
    vector = get_embedding("마포구 연남동 한식 상권")
    assert len(vector) == 64
    norm = sum(value * value for value in vector) ** 0.5
    assert norm == pytest.approx(1.0, abs=1e-4)


def test_RG02_018(monkeypatch):
    """GEMINI_API_KEY 가 있으면 Gemini 임베딩 값을 그대로 반환한다."""
    expected = [0.25] * 64

    class Embedding:
        values = expected

    class Result:
        embedding = Embedding()

    class Models:
        def embed_content(self, model, contents):
            assert model == "text-embedding-004"
            assert contents
            return Result()

    class Client:
        def __init__(self, api_key=None, http_options=None):
            assert api_key == "unit-key"
            self.models = Models()

    monkeypatch.setenv("GEMINI_API_KEY", "unit-key")
    install_genai(monkeypatch, Client)
    assert get_embedding("연남동") == expected


def test_RG02_019(monkeypatch):
    """Gemini 호출이 실패하면 64차원 로컬 임베딩으로 폴백한다."""

    class Models:
        def embed_content(self, model, contents):
            raise RuntimeError("gemini down")

    class Client:
        def __init__(self, api_key=None, http_options=None):
            self.models = Models()

    monkeypatch.setenv("GEMINI_API_KEY", "unit-key")
    install_genai(monkeypatch, Client)
    vector = get_embedding("연남동 매출")
    assert len(vector) == 64
    norm = sum(value * value for value in vector) ** 0.5
    assert norm == pytest.approx(1.0, abs=1e-4)


def test_RG02_020():
    """빈 문자열 임베딩은 64차원 영벡터이고 0으로 나누지 않는다."""
    vector = get_embedding("")
    assert len(vector) == 64
    assert all(value == 0.0 for value in vector)


def test_RG02_021():
    """같은 벡터의 코사인 유사도는 1.0 이다."""
    vector = get_embedding("연남동 매출 동향")
    assert compute_cosine_similarity(vector, vector) == pytest.approx(1.0, abs=1e-5)


def test_RG02_022():
    """영벡터와의 코사인 유사도는 0.0 이다."""
    assert compute_cosine_similarity([0.0] * 64, [1.0] * 64) == 0.0


def test_RG02_023():
    """64차원과 512차원은 경고 또는 예외로 알려야 하고 조용히 자르면 안 된다."""
    import warnings

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            score = compute_cosine_similarity([1.0] * 64, [1.0] * 512)
        except (ValueError, TypeError):
            return
    if score == 1.0 and not caught:
        pytest.fail(f"64차원과 512차원을 경고 없이 유사도 {score}으로 잘랐다")


def test_RG02_024(monkeypatch):
    """Gemini 768차원 벡터는 DB vector(64)와 맞추거나 거절해야 한다."""

    class Embedding:
        values = [0.01] * 768

    class Result:
        embedding = Embedding()

    class Models:
        def embed_content(self, model, contents):
            return Result()

    class Client:
        def __init__(self, api_key=None, http_options=None):
            self.models = Models()

    monkeypatch.setenv("GEMINI_API_KEY", "unit-key")
    install_genai(monkeypatch, Client)
    try:
        vector = get_embedding("마포구")
    except (ValueError, TypeError):
        return
    if len(vector) != 64:
        pytest.fail(f"API 768차원이 DB vector(64) 검증 없이 {len(vector)}차원으로 반환됨")


def test_RG02_025():
    """하드코딩 문서는 실제 공시 확인 전 표본/미검증으로 표시되어야 한다."""
    docs = load_market_knowledge_documents()
    unlabeled = []
    for doc in docs:
        blob = " ".join(str(doc.get(key, "")) for key in ("title", "source", "content", "metadata"))
        marked = any(token in blob for token in ("샘플", "표본", "미검증", "미확인", "예시"))
        marked = marked or doc.get("is_sample") is True or doc.get("verified") is False
        if not marked:
            unlabeled.append(doc["id"])
    if unlabeled:
        pytest.fail(f"표본/미검증 표시 없는 문서 {len(unlabeled)}건: {', '.join(unlabeled[:4])}")


def test_RG02_026():
    """원본에 보고서를 추가하면 검색 캐시가 그 문서를 반영해야 한다."""
    from src.features.commercial_rag_001.market_knowledge import service as knowledge
    from src.features.commercial_rag_001.market_search import service as search

    search._CHUNKS_CACHE = None
    search._EMBEDDINGS_CACHE = None
    search.get_cached_chunks()
    knowledge.RAW_KNOWLEDGE_DOCUMENTS.append(
        {
            "id": "rep-cache-refresh-probe",
            "title": "캐시 갱신 프로브",
            "doc_type": "market_report",
            "district": "중구",
            "dong": "명동",
            "industry": "한식음식점",
            "quarter": "2024-4",
            "source": "테스트",
            "source_url": "https://example.test/probe",
            "published_at": "2026-11-02",
            "content": "캐시 갱신 확인용 본문",
        }
    )
    try:
        ids = [chunk.id for chunk in search.get_cached_chunks()]
        if not any(chunk_id.startswith("rep-cache-refresh-probe") for chunk_id in ids):
            pytest.fail("보고서 추가 후에도 get_cached_chunks 가 기존 캐시만 반환함")
    finally:
        knowledge.RAW_KNOWLEDGE_DOCUMENTS.pop()
        search._CHUNKS_CACHE = None
        search._EMBEDDINGS_CACHE = None
