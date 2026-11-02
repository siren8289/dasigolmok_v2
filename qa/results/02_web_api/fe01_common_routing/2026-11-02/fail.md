# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| FE01-008 | React 라우팅·공통 UX | 없는 경로 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| FE01-018 | React 라우팅·공통 UX | 404 검색엔진/접근성 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |

## FE01-008 없는 경로
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 오류나 빈 화면 대신 유효한 404 안내가 제공된다
- 실제: 실제 본문에는 404 안내가 없다: dasiGolmok골목 상권 진단업종 추천: expected null not to be null
- 결함ID: DEF-FE01-008
- 코드: front/src/App.tsx

## FE01-018 404 검색엔진/접근성
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 사용자용 오류 안내와 웹 접근성 검증 필요
- 실제: 알 수 없는 경로에 사용자용 오류 heading이 없다: expected null not to be null
- 결함ID: DEF-FE01-018
- 코드: front/src/App.tsx
