"""QA 4영역과 섹션 매핑.

결과 기록 경로: qa/{영역}/{섹션}/{YYYY-MM-DD}/
"""

from __future__ import annotations

AREAS = (
    "단위·통합 테스트",
    "웹·API 테스트",
    "보안·품질 검사",
    "인프라·배포 검사",
)

SECTION_TO_AREA: dict[str, str] = {
    "AI05_위험판정경계": "단위·통합 테스트",
    "AI06_학습피처": "단위·통합 테스트",
    "AI07_폐업ML추론": "단위·통합 테스트",
    "AI08_매출DL추론": "단위·통합 테스트",
    "AI09_LLM기본설명": "단위·통합 테스트",
    "BE01_진단요청DTO": "단위·통합 테스트",
    "BE02_진단CRUD": "단위·통합 테스트",
    "DB01_진단영속성": "단위·통합 테스트",
    "DB02_SQL마이그레이션": "단위·통합 테스트",
    "DB03_pgvector전용": "단위·통합 테스트",
    "DE01_공공API수집": "단위·통합 테스트",
    "DE02_CSV인코딩": "단위·통합 테스트",
    "DE03_점포정제": "단위·통합 테스트",
    "DE04_매출인구정제": "단위·통합 테스트",
    "DE05_결측치이상치": "단위·통합 테스트",
    "DE06_테이블결합": "단위·통합 테스트",
    "DE07_옵션생성": "단위·통합 테스트",
    "DE08_ETL실행저장": "단위·통합 테스트",
    "RG02_지식베이스": "단위·통합 테스트",
    "RG03_상권근거검색": "단위·통합 테스트",
    "RG04_지원정책규칙": "단위·통합 테스트",
    "RG05_종합가이드": "단위·통합 테스트",
    "RG06_오케스트레이션": "단위·통합 테스트",
    "RG08_RAG정량평가": "단위·통합 테스트",
    "AI01_FastAPI계약": "웹·API 테스트",
    "AI02_옵션조회": "웹·API 테스트",
    "AI03_진단파이프라인": "웹·API 테스트",
    "AI04_추천파이프라인": "웹·API 테스트",
    "BE03_진단HTTP": "웹·API 테스트",
    "BE04_추천HTTP": "웹·API 테스트",
    "FE01_공통라우팅": "웹·API 테스트",
    "FE02_진단입력UI": "웹·API 테스트",
    "FE03_진단결과UI": "웹·API 테스트",
    "FE04_추천UI": "웹·API 테스트",
    "FE05_HTTP클라이언트": "웹·API 테스트",
    "RG01_RAG_HTTP": "웹·API 테스트",
    "BE05_AI연동예외": "보안·품질 검사",
    "BE06_전역예외": "보안·품질 검사",
    "QA01_보안비기능": "보안·품질 검사",
    "QA02_문서추적회귀": "보안·품질 검사",
    "RG07_보안하네스": "보안·품질 검사",
    "OPS1_Docker연결": "인프라·배포 검사",
    "OPS2_GitHubCI": "인프라·배포 검사",
    "OPS3_배포스크립트": "인프라·배포 검사",
}

# 게이트 검사 → (영역, 섹션)
CHECK_TO_SECTION: dict[str, tuple[str, str]] = {
    "record": ("보안·품질 검사", "QA02_문서추적회귀"),
    "security": ("보안·품질 검사", "QA01_보안비기능"),
    "front": ("웹·API 테스트", "FE01_공통라우팅"),
    "python": ("단위·통합 테스트", "DE05_결측치이상치"),
    "java": ("단위·통합 테스트", "BE01_진단요청DTO"),
    "regression": ("단위·통합 테스트", "DE05_결측치이상치"),
}


def resolve_area_section(section: str, area: str = "") -> tuple[str, str]:
    if area and section:
        return area, section
    mapped = SECTION_TO_AREA.get(section)
    if not mapped:
        raise ValueError(f"unknown QA section: {section}")
    return mapped, section
