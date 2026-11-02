"""RG 스위트 공통 설정. 외부 임베딩 API는 호출하지 않는다."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def _disable_external_gemini(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)


@pytest.fixture(autouse=True)
def _reset_search_cache():
    yield
    from src.features.commercial_rag_001.market_search import service as ms

    ms._CHUNKS_CACHE = None
    ms._EMBEDDINGS_CACHE = None


@pytest.fixture
def client():
    from src.features.commercial_rag_001.router import router

    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as test_client:
        yield test_client
