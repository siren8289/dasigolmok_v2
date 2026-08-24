from __future__ import annotations

import re
from collections import Counter

from app.models import (
    ClassifyResponse,
    CurationCandidate,
    CurationCandidateRequest,
    CurationCandidateResponse,
    StoryAnalyzeRequest,
    SuggestedTag,
    SummaryResponse,
    TagSuggestResponse,
)

THEME_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("시장", ("시장", "장터", "점포", "가게", "상점")),
    ("거리", ("골목", "거리", "도로", "네온", "골목길")),
    ("문화유산", ("한옥", "문화", "유산", "공장", "흔적", "유적")),
    ("학교", ("학교", "교실", "교문", "운동장")),
    ("상점", ("카페", "커피", "식당", "상점", "가게")),
]

PERIOD_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("1970s", ("1970", "70년대", "70s")),
    ("1980s", ("1980", "80년대", "80s")),
    ("1990s", ("1990", "90년대", "90s")),
    ("2000s", ("2000", "00년대", "2000s")),
]

CATEGORY_ORDER = ("거리", "상점", "학교", "문화유산", "시장")


def _normalize(text: str) -> str:
    return (text or "").lower()


def _contains_any(text: str, keys: tuple[str, ...]) -> bool:
    return any(k.lower() in text for k in keys)


def suggest_tags(req: StoryAnalyzeRequest) -> TagSuggestResponse:
    text = _normalize(f"{req.title} {req.description} {' '.join(req.tags)}")
    suggestions: list[SuggestedTag] = []
    seen: set[str] = set()

    for name, keys in THEME_RULES:
        if _contains_any(text, keys) and name not in seen:
            suggestions.append(
                SuggestedTag(name=name, type="THEME", rationale="키워드 휴리스틱 매칭")
            )
            seen.add(name)

    for name, keys in PERIOD_RULES:
        if _contains_any(text, keys) and name not in seen:
            suggestions.append(
                SuggestedTag(name=name, type="PERIOD", rationale="시대 키워드 휴리스틱 매칭")
            )
            seen.add(name)

    if req.category and req.category not in seen:
        suggestions.append(
            SuggestedTag(name=req.category, type="CATEGORY", rationale="요청 category 반영")
        )
        seen.add(req.category)

    if req.period_tag and req.period_tag not in seen:
        suggestions.append(
            SuggestedTag(name=req.period_tag, type="PERIOD", rationale="요청 period_tag 반영")
        )

    if not any(s.type == "THEME" for s in suggestions):
        suggestions.insert(
            0, SuggestedTag(name="거리", type="THEME", rationale="기본 테마 fallback")
        )

    confidence = min(0.45 + 0.08 * len(suggestions), 0.85)
    return TagSuggestResponse(suggestions=suggestions, confidence=round(confidence, 2))


def summarize(req: StoryAnalyzeRequest) -> SummaryResponse:
    title = req.title.strip()
    desc = re.sub(r"\s+", " ", req.description.strip())
    short = desc if len(desc) <= 120 else desc[:117] + "..."
    period = req.period_tag or next(
        (p for p, keys in PERIOD_RULES if _contains_any(_normalize(desc), keys)),
        None,
    )
    theme = next(
        (t for t, keys in THEME_RULES if _contains_any(_normalize(f"{title} {desc}"), keys)),
        req.category or "지역 기억",
    )
    bits = [f"「{title}」"]
    if period:
        bits.append(f"{period} 무렵")
    bits.append(f"{theme} 이야기로, {short}")
    summary = " ".join(bits)
    return SummaryResponse(summary=summary, confidence=0.62)


def classify(req: StoryAnalyzeRequest) -> ClassifyResponse:
    text = _normalize(f"{req.title} {req.description}")
    scores: Counter[str] = Counter()
    for name, keys in THEME_RULES:
        if _contains_any(text, keys):
            scores[name] += 1
    category = req.category
    if not category:
        if scores:
            category = scores.most_common(1)[0][0]
        else:
            category = "거리"
    period = req.period_tag
    if not period:
        for name, keys in PERIOD_RULES:
            if _contains_any(text, keys):
                period = name
                break
    labels = [name for name, _ in scores.most_common(3)]
    if category not in labels:
        labels.insert(0, category)
    confidence = 0.7 if scores else 0.5
    return ClassifyResponse(
        category=category,
        period_tag=period,
        labels=labels,
        confidence=confidence,
    )


def curation_candidates(req: CurationCandidateRequest) -> CurationCandidateResponse:
    """Rank provided story IDs only — does not query or mutate DB."""
    prefer = {t.lower() for t in req.prefer_tags}
    ranked: list[CurationCandidate] = []
    for idx, story_id in enumerate(req.story_ids):
        # Stable heuristic: prefer earlier IDs slightly; tag preference boosts score if id hash overlaps.
        base = max(0.1, 1.0 - (idx * 0.05))
        boost = 0.15 if prefer and (hash(story_id) % 3 == 0) else 0.0
        ranked.append(
            CurationCandidate(
                story_id=story_id,
                score=round(min(base + boost, 1.0), 3),
                reason="공개 후보 재순위(보조). Backend가 APPROVED만 노출해야 함.",
            )
        )
    ranked.sort(key=lambda c: c.score, reverse=True)
    return CurationCandidateResponse(candidates=ranked[: req.limit])
