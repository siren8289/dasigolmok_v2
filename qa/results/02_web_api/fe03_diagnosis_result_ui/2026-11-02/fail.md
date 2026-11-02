# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| FE03-021 | 진단 결과 렌더링 | 필수 수치 누락 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| FE03-022 | 진단 결과 렌더링 | 다른 ID 순차 조회 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |

## FE03-021 필수 수치 누락
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: NaN/런타임 오류 없이 결측치 안내가 제공되어야 한다
- 실제: 결측 안내 없음. 본문=마포구 연남동 · 한식음식점폐업률 %안정 · 상권축소규칙: 폐업률 8% 이상 또는 상권축소면 위험 / 4% 이상 또는 다이나믹이면 주의AI 예측ML 예상 폐업률7.34%DL 예상 점포당 매출650.2만원점포 30개 · 개업률 2.1% · 유동인구 1,100명AI 설명 (기본 문장)한 줄
- 결함ID: DEF-FE03-021
- 코드: front/src/pages/ResultPage.tsx

## FE03-022 다른 ID 순차 조회
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: ID별 최신 결과만 표출된다
- 실제: expected <p …(1)></p> to be null
- 결함ID: DEF-FE03-022
- 코드: front/src/pages/ResultPage.tsx
