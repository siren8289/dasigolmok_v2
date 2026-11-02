# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| FE04-009 | 업종 추천 화면 | 추천 결과 빈 배열 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| FE04-020 | 업종 추천 화면 | 지역 변경 즉시 오래된 표 처리 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| FE04-021 | 업종 추천 화면 | 추천 상위 5와 전체 목록 차이 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| FE04-023 | 업종 추천 화면 | 중복 업종 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |

## FE04-009 추천 결과 빈 배열
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 빈 상태 안내가 제공되도록 확인
- 실제: 빈 all_industries에 대한 안내 문구가 없다: expected null not to be null
- 결함ID: DEF-FE04-009
- 코드: front/src/pages/RecommendPage.tsx

## FE04-020 지역 변경 즉시 오래된 표 처리
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 구 지역과 표 지역이 불일치하지 않게 결과 초기화
- 실제: 구를 바꿨는데 이전 동 결과 표가 그대로 남아 있다: expected <p class="font-bold mb-1"></p> to be null
- 결함ID: DEF-FE04-020
- 코드: front/src/pages/RecommendPage.tsx

## FE04-021 추천 상위 5와 전체 목록 차이
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 전체 표가 10개 렌더링되고 상위 추천 표시 여부 점검
- 실제: 10행은 렌더되지만 recommendations 5개를 구분하는 상위 추천 표시가 없다: expected null not to be null
- 결함ID: DEF-FE04-021
- 코드: front/src/pages/RecommendPage.tsx

## FE04-023 중복 업종
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: React key 중복 경고가 없도록 정책 확인
- 실제: Warning: Encountered two children with the same key, `%s`. Keys should be unique so that components maintain their identity across updates. Non-unique keys may cause children to be duplicated and/or omitted — the behavior is unsupported and could change in a future version.%s 한식음식점
- 결함ID: DEF-FE04-023
- 코드: front/src/pages/RecommendPage.tsx
