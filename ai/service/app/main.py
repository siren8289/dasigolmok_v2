from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import analyzer
from app.models import (
    ClassifyResponse,
    CurationCandidateRequest,
    CurationCandidateResponse,
    HealthResponse,
    StoryAnalyzeRequest,
    SummaryResponse,
    TagSuggestResponse,
)

app = FastAPI(
    title="다시, 골목 AI Assist",
    description=(
        "스토리 요약·태그·분류·큐레이션 후보를 제안하는 보조 서비스. "
        "Story 상태(APPROVED/REJECTED/HIDDEN)를 변경하지 않으며 DB를 직접 수정하지 않습니다."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        extras={
            "endpoints": [
                "/v1/analyze/tags",
                "/v1/analyze/summary",
                "/v1/analyze/classify",
                "/v1/curation/candidates",
            ]
        }
    )


@app.post("/v1/analyze/tags", response_model=TagSuggestResponse)
def analyze_tags(body: StoryAnalyzeRequest) -> TagSuggestResponse:
    return analyzer.suggest_tags(body)


@app.post("/v1/analyze/summary", response_model=SummaryResponse)
def analyze_summary(body: StoryAnalyzeRequest) -> SummaryResponse:
    return analyzer.summarize(body)


@app.post("/v1/analyze/classify", response_model=ClassifyResponse)
def analyze_classify(body: StoryAnalyzeRequest) -> ClassifyResponse:
    return analyzer.classify(body)


@app.post("/v1/curation/candidates", response_model=CurationCandidateResponse)
def curation_candidates(body: CurationCandidateRequest) -> CurationCandidateResponse:
    return analyzer.curation_candidates(body)
