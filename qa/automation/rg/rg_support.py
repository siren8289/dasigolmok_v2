"""RG 테스트 공용 픽스처 헬퍼. 프로덕션 코드가 아니다."""
import sys
import types


def router_module():
    """패키지 __init__ 가 router 이름으로 가리므로 sys.modules 의 실제 모듈을 반환한다."""
    import src.features.commercial_rag_001.router  # noqa: F401

    return sys.modules["src.features.commercial_rag_001.router"]

from src.features.commercial_rag_001.schemas import DocumentChunk, SupportPolicyItem


def doc(**kwargs) -> DocumentChunk:
    base = dict(
        id="d1",
        title="제목",
        content="본문",
        doc_type="market_report",
        source="서울시 상권분석서비스",
        score=0.0,
    )
    base.update(kwargs)
    return DocumentChunk(**base)


def policy(**kwargs) -> SupportPolicyItem:
    base = dict(
        id="p1",
        title="정책",
        organization="기관",
        start_date="2026-01-01",
        end_date="2026-12-31",
        status="open",
        is_open=True,
        description="설명",
        score=0.0,
    )
    base.update(kwargs)
    return SupportPolicyItem(**base)


def raw_policy(**kwargs) -> dict:
    base = dict(
        id="p",
        title="제목",
        organization="기관",
        target_district=None,
        target_industry=None,
        start_date="2026-01-01",
        end_date="2026-12-31",
        support_amount="100만원",
        description="설명",
        eligibility="자격",
        source_url="https://example.test/policy",
    )
    base.update(kwargs)
    return base


def install_genai(monkeypatch, client_cls):
    genai_mod = types.ModuleType("google.genai")
    genai_mod.Client = client_cls
    types_mod = types.ModuleType("google.genai.types")

    class HttpOptions:
        def __init__(self, timeout=None):
            self.timeout = timeout

    types_mod.HttpOptions = HttpOptions
    genai_mod.types = types_mod
    google_mod = types.ModuleType("google")
    google_mod.genai = genai_mod
    monkeypatch.setitem(sys.modules, "google", google_mod)
    monkeypatch.setitem(sys.modules, "google.genai", genai_mod)
    monkeypatch.setitem(sys.modules, "google.genai.types", types_mod)
