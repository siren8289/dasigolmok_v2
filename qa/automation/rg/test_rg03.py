"""RG03 상권 근거 검색."""
import pytest

from rg_support import doc
from src.features.commercial_rag_001.market_search.service import (
    rerank,
    search_market_evidence,
    search_pgvector,
)
from src.features.commercial_rag_001.schemas import DocumentChunk, MarketSearchQuery


def test_RG03_001():
    """마포구 검색 결과는 market_report 만 포함한다."""
    response = search_market_evidence(MarketSearchQuery(query="연남동 상권", district="마포구", top_k=5))
    assert response.documents
    assert all(item.doc_type == "market_report" for item in response.documents)


def test_RG03_002():
    """district=마포구 1차 결과는 마포구 보고서만 담는다."""
    response = search_market_evidence(MarketSearchQuery(query="연남동 한식", district="마포구", top_k=5))
    assert response.documents
    assert {item.district for item in response.documents} == {"마포구"}


def test_RG03_003():
    """district=마포구 결과에서 강남구 문서는 빠진다."""
    response = search_market_evidence(MarketSearchQuery(query="매출 동향", district="마포구", top_k=5))
    assert response.documents
    assert all(item.district != "강남구" for item in response.documents)


def test_RG03_004():
    """행정동 연남동 일치는 rerank 점수에 0.3 을 더한다."""
    item = doc(dong="연남동", content="본문", title="제목", score=0.0)
    ranked = rerank([item], query="zzzzqqqq", dong="연남동", top_k=1)
    assert ranked[0].score == 0.3


def test_RG03_005():
    """자치구 일치는 rerank 점수에 0.2 를 더한다."""
    item = doc(district="마포구", content="본문", title="제목", score=0.0)
    ranked = rerank([item], query="zzzzqqqq", district="마포구", top_k=1)
    assert ranked[0].score == 0.2


def test_RG03_006():
    """업종 일치는 rerank 점수에 0.2 를 더한다."""
    item = doc(industry="한식음식점", content="본문", title="제목", score=0.0)
    ranked = rerank([item], query="zzzzqqqq", industry="한식음식점", top_k=1)
    assert ranked[0].score == 0.2


def test_RG03_007():
    """쿼리 토큰 2개 중 1개 일치는 0.1(비율 0.5×0.2)을 더한다."""
    item = doc(content="가나다 기타", title="제목", score=0.0)
    ranked = rerank([item], query="가나다 라마바", top_k=1)
    assert ranked[0].score == pytest.approx(0.1)


def test_RG03_008():
    """가산이 없으면 원본 score 0.75 가 유지된다."""
    item = doc(content="xxx", title="yyy", score=0.75)
    ranked = rerank([item], query="zzzzqqqq", top_k=1)
    assert ranked[0].score == 0.75


def test_RG03_009():
    """rerank 결과는 score 내림차순이다."""
    low = doc(id="low", content="a", title="a", score=0.2)
    high = doc(id="high", content="b", title="b", score=0.9)
    ranked = rerank([low, high], query="zzzzqqqq", top_k=2)
    assert [item.id for item in ranked] == ["high", "low"]
    assert ranked[0].score >= ranked[1].score


def test_RG03_010():
    """top_k=1 이면 문서 1개만 반환한다."""
    items = [doc(id=f"d{i}", content="본문", title="제목", score=0.1 * i) for i in range(1, 4)]
    ranked = rerank(items, query="zzzzqqqq", top_k=1)
    assert len(ranked) == 1


def test_RG03_011():
    """후보 5개에 top_k=3 이면 최대 3개다."""
    items = [doc(id=f"d{i}", content="본문", title="제목", score=float(i)) for i in range(5)]
    ranked = rerank(items, query="zzzzqqqq", top_k=3)
    assert len(ranked) == 3


def test_RG03_012():
    """top_k=20 이어도 마포구 보고서 후보 수를 넘지 않는다."""
    response = search_market_evidence(MarketSearchQuery(query="연남동", district="마포구", top_k=20))
    assert 1 <= len(response.documents) <= 20
    assert response.total_count == len(response.documents)
    assert len(response.documents) < 20


def test_RG03_013():
    """같은 id 문서는 rerank 결과에서 한 번만 남아야 한다."""
    duplicated = [
        doc(id="dup", content="본문", title="제목", score=0.5),
        doc(id="dup", content="본문", title="제목", score=0.4),
    ]
    ranked = rerank(duplicated, query="zzzzqqqq", top_k=5)
    ids = [item.id for item in ranked]
    if len(ids) != len(set(ids)):
        pytest.fail(f"동일 id가 중복 반환됨: {ids}")


def test_RG03_014():
    """없는 자치구는 전체 상권 보고서 fallback 으로 여러 구 문서를 반환한다."""
    response = search_market_evidence(MarketSearchQuery(query="상권 보고서", district="없는구", top_k=20))
    districts = {item.district for item in response.documents}
    assert len(response.documents) >= 2
    assert len(districts) >= 2


def test_RG03_015():
    """없는 자치구 fallback 문서가 그 지역 근거로 표시되면 안 된다."""
    response = search_market_evidence(MarketSearchQuery(query="상권 보고서", district="없는구", top_k=5))
    leaked = []
    for item in response.documents:
        marked = bool(item.metadata.get("region_mismatch") or item.metadata.get("fallback"))
        if item.district != "없는구" and not marked:
            leaked.append(item.district)
    if leaked:
        pytest.fail(f"없는구 검색이 타구 {leaked} 문서를 불일치 표시 없이 반환함")


def test_RG03_016():
    """dong=없는동 인데 다른 동 문서를 단정 근거로 반환하면 안 된다."""
    response = search_market_evidence(
        MarketSearchQuery(query="상권 동향", district="마포구", dong="없는동", top_k=5)
    )
    leaked = [
        item.dong
        for item in response.documents
        if item.dong != "없는동" and not item.metadata.get("dong_mismatch")
    ]
    if leaked:
        pytest.fail(f"없는동 검색이 다른 동 {leaked} 문서를 경고 없이 반환함")


def test_RG03_017():
    """없는 업종 검색이 타업종 보고서를 불일치 표시 없이 반환하면 안 된다."""
    response = search_market_evidence(
        MarketSearchQuery(query="상권 동향", district="마포구", industry="없는업종", top_k=5)
    )
    leaked = [
        item.industry
        for item in response.documents
        if item.industry != "없는업종" and not item.metadata.get("industry_mismatch")
    ]
    if leaked:
        pytest.fail(f"없는업종 검색이 타업종 {leaked} 보고서를 표시 없이 반환함")


def test_RG03_018():
    """quarter=1999-1 조건은 다른 분기 문서를 걸러야 한다."""
    response = search_market_evidence(
        MarketSearchQuery(query="연남동 상권", district="마포구", quarter="1999-1", top_k=5)
    )
    bad = [item.quarter for item in response.documents if item.quarter != "1999-1"]
    if bad:
        pytest.fail(f"quarter=1999-1 필터가 무시되고 {bad} 문서가 반환됨")


def test_RG03_019(monkeypatch):
    """2019년 문서는 최신 통계처럼 보이면 안 되고 오래됨 표시가 있어야 한다."""
    import src.features.commercial_rag_001.market_search.service as search

    old = doc(
        id="old-2019",
        title="2019 보고서",
        content="과거 수치",
        district="마포구",
        dong="연남동",
        quarter="2019-1",
        published_at="2019-03-01",
        score=0.0,
    )
    monkeypatch.setattr(search, "get_cached_chunks", lambda: [old])
    monkeypatch.setattr(search, "get_cached_chunk_embeddings", lambda: {old.id: [1.0] + [0.0] * 63})
    monkeypatch.setattr(search, "get_embedding", lambda _text: [1.0] + [0.0] * 63)
    response = search_market_evidence(MarketSearchQuery(query="상권", district="마포구", top_k=3))
    assert response.documents
    meta = response.documents[0].metadata
    if not any(key in meta for key in ("stale", "outdated", "as_of")):
        pytest.fail(f"2019-1 문서가 최신성 표시 없이 반환됨 metadata={meta}")


def test_RG03_020(monkeypatch):
    """청크 캐시가 있으면 build_document_chunks 는 한 번만 호출된다."""
    import src.features.commercial_rag_001.market_search.service as search

    search._CHUNKS_CACHE = None
    calls = {"n": 0}
    real = search.build_document_chunks

    def wrapped():
        calls["n"] += 1
        return real()

    monkeypatch.setattr(search, "build_document_chunks", wrapped)
    search.get_cached_chunks()
    search.get_cached_chunks()
    assert calls["n"] == 1


def test_RG03_021(monkeypatch):
    """임베딩 캐시가 있으면 두 번째 조회에서 get_embedding 을 다시 호출하지 않는다."""
    import src.features.commercial_rag_001.market_search.service as search

    search._CHUNKS_CACHE = None
    search._EMBEDDINGS_CACHE = None
    calls = {"n": 0}

    def fake(_text):
        calls["n"] += 1
        return [0.0] * 64

    monkeypatch.setattr(search, "get_embedding", fake)
    search.get_cached_chunk_embeddings()
    first = calls["n"]
    search.get_cached_chunk_embeddings()
    assert first == len(search.get_cached_chunks())
    assert calls["n"] == first
    assert first >= 1


def test_RG03_022():
    """pgvector SQL 이 district, dong, industry, quarter 를 바인딩한다."""
    captured = {}

    class Cursor:
        def execute(self, sql, params):
            captured["sql"] = sql
            captured["params"] = params

        def fetchall(self):
            return []

    class Conn:
        def cursor(self):
            return Cursor()

    search_pgvector(Conn(), [0.1, 0.2], district="마포구", dong="연남동", industry="한식음식점", quarter="2024-4", top_k=3)
    sql = captured["sql"].lower()
    assert "district" in sql and "dong" in sql and "industry" in sql and "quarter" in sql
    params = captured["params"]
    assert params.count("마포구") == 2
    assert params.count("연남동") == 2
    assert params.count("한식음식점") == 2
    assert params.count("2024-4") == 2
    assert params[-1] == 3


def test_RG03_023():
    """DROP 문자열이 SQL 본문에 이어 붙지 않고 파라미터로만 전달된다."""
    payload = "'; DROP TABLE market_knowledge_chunks;--"
    captured = {}

    class Cursor:
        def execute(self, sql, params):
            captured["sql"] = sql
            captured["params"] = params

        def fetchall(self):
            return []

    class Conn:
        def cursor(self):
            return Cursor()

    search_pgvector(Conn(), [0.1], district=payload, top_k=1)
    assert "DROP" not in captured["sql"]
    assert payload in captured["params"]


def test_RG03_024():
    """연결이 없거나 execute 가 실패하면 빈 목록을 반환한다."""
    assert search_pgvector(None, [0.1, 0.2]) == []

    class Cursor:
        def execute(self, sql, params):
            raise RuntimeError("db down")

    class Conn:
        def cursor(self):
            return Cursor()

    assert search_pgvector(Conn(), [0.1, 0.2], district="마포구") == []


def test_RG03_025():
    """쿼리 벡터 차원이 색인 vector(64)와 다르면 거절되어야 한다."""
    sent = {}

    class Cursor:
        def execute(self, sql, params):
            sent["sql"] = sql
            sent["params"] = params

        def fetchall(self):
            return []

    class Conn:
        def cursor(self):
            return Cursor()

    wide = [0.1] * 768
    try:
        search_pgvector(Conn(), wide, top_k=1)
    except (ValueError, TypeError):
        return
    if "vector(64)" not in sent.get("sql", "") and len(wide) != 64:
        pytest.fail("768차원 쿼리 벡터가 vector(64) 검사 없이 execute 로 전달됨")


def test_RG03_026(monkeypatch):
    """search_market_evidence 가 pgvector 검색 경로를 사용해야 한다."""
    import src.features.commercial_rag_001.market_search.service as search

    calls = {"n": 0}

    def spy(*_args, **_kwargs):
        calls["n"] += 1
        return []

    monkeypatch.setattr(search, "search_pgvector", spy)
    search._CHUNKS_CACHE = None
    search._EMBEDDINGS_CACHE = None
    search.search_market_evidence(MarketSearchQuery(query="연남동 상권", district="마포구", top_k=2))
    if calls["n"] == 0:
        pytest.fail("search_market_evidence 가 search_pgvector 를 호출하지 않음")


def test_RG03_027():
    """content 가 None 이어도 rerank 가 TypeError 를 내지 않아야 한다."""
    broken = DocumentChunk.model_construct(
        id="null-content",
        title="제목",
        content=None,
        doc_type="market_report",
        source="출처",
        score=0.75,
        metadata={},
    )
    try:
        rerank([broken], query="테스트", top_k=1)
    except Exception as exc:
        pytest.fail(f"content=None 타입 에러 미방어: {type(exc).__name__}: {exc}")
