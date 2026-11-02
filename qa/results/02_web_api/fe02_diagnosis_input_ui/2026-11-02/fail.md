# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| FE02-007 | 진단 페이지 입력·셀렉트 | 옵션 빈 목록 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| FE02-021 | 진단 페이지 입력·셀렉트 | 빈 지역 제출 방어 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |

## FE02-007 옵션 빈 목록
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 선택 상태를 안전하게 표시하고 실패 요청을 피한다
- 실제: 빈 목록 안내 없음. 본문=골목 상권 진단행정동과 업종을 고르면, 폐업률(ML)·점포당 매출(DL)·쉬운 설명(LLM)을 보여 줍니다.자치구행정동연남동업종진단하기: expected null not to be null
- 결함ID: DEF-FE02-007
- 코드: front/src/pages/DiagnosePage.tsx

## FE02-021 빈 지역 제출 방어
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 유효하지 않은 선택값은 제출 전 차단되어야 한다
- 실제: 빈 자치구 제출이 차단되지 않음. POST 1건: expected false to be truthy
- 결함ID: DEF-FE02-021
- 코드: front/src/pages/DiagnosePage.tsx
