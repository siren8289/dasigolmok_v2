from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class StoryAnalyzeRequest(BaseModel):
    story_id: Optional[str] = None
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    category: Optional[str] = None
    period_tag: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class SuggestedTag(BaseModel):
    name: str
    type: Literal["THEME", "PERIOD", "CATEGORY"] = "THEME"
    rationale: str = "heuristic keyword match"


class TagSuggestResponse(BaseModel):
    kind: Literal["PROPOSAL_ONLY"] = "PROPOSAL_ONLY"
    suggestions: List[SuggestedTag]
    confidence: float
    engine: str = "fastapi-heuristic"
    model_version: str = "heuristic-v1"
    prompt_version: str = "n/a"
    disclaimer: str = (
        "AI 제안입니다. 최종 태그는 사용자가 선택하며 승인/반려/공개를 자동 결정하지 않습니다."
    )


class SummaryResponse(BaseModel):
    kind: Literal["PROPOSAL_ONLY"] = "PROPOSAL_ONLY"
    summary: str
    confidence: float
    engine: str = "fastapi-heuristic"
    model_version: str = "heuristic-v1"
    prompt_version: str = "n/a"
    disclaimer: str = (
        "요약 제안입니다. 역사적 사실을 확정하지 않으며 관리자 검수를 대체하지 않습니다."
    )


class ClassifyResponse(BaseModel):
    kind: Literal["PROPOSAL_ONLY"] = "PROPOSAL_ONLY"
    category: str
    period_tag: Optional[str] = None
    labels: List[str] = Field(default_factory=list)
    confidence: float
    engine: str = "fastapi-heuristic"
    model_version: str = "heuristic-v1"
    prompt_version: str = "n/a"
    disclaimer: str = (
        "분류 후보입니다. 최종 공개 여부는 Backend 정책과 관리자 검수가 결정합니다."
    )


class CurationCandidateRequest(BaseModel):
    story_ids: List[str] = Field(default_factory=list)
    limit: int = Field(default=10, ge=1, le=50)
    prefer_tags: List[str] = Field(default_factory=list)


class CurationCandidate(BaseModel):
    story_id: str
    score: float
    reason: str


class CurationCandidateResponse(BaseModel):
    kind: Literal["PROPOSAL_ONLY"] = "PROPOSAL_ONLY"
    candidates: List[CurationCandidate]
    engine: str = "fastapi-heuristic"
    model_version: str = "heuristic-v1"
    prompt_version: str = "n/a"
    disclaimer: str = (
        "추천 후보입니다. 실제 노출은 APPROVED 콘텐츠와 Backend 큐레이션 정책을 따릅니다."
    )


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "dasi-golmok-ai"
    role: str = "assist_only"
    mutates_story_status: bool = False
    extras: Dict[str, Any] = Field(default_factory=dict)
