# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| FE05-015 | 프론트 fetch API 계약 | 빈 응답 body | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| FE05-016 | 프론트 fetch API 계약 | API 경로 이중 슬래시 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| FE05-017 | 프론트 fetch API 계약 | 민감정보 에러 반사 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| FE05-018 | 프론트 fetch API 계약 | 조회 ID 인코딩 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |

## FE05-015 빈 응답 body
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: JSON 파싱 오류를 의미 있게 처리해야 한다
- 실제: 빈 200 body는 의미 있는 오류 문구로 바뀌어야 한다: expected [Function] to throw error including '요청에 실패했습니다.' but got 'Unexpected end of JSON input'
- 결함ID: DEF-FE05-015
- 코드: front/src/api/api.ts

## FE05-016 API 경로 이중 슬래시
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: //api 중복 처리 확인
- 실제: 실제 URL https://host//api/options: expected 'https://host//api/options' not to contain '//api'
- 결함ID: DEF-FE05-016
- 코드: front/src/api/api.ts

## FE05-017 민감정보 에러 반사
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 사용자 노출 전 민감정보 제거
- 실제: 실제 메시지에 토큰이 남아 있다: token=SECRET-TOKEN-123 failed: expected 'token=SECRET-TOKEN-123 failed' not to contain 'SECRET-TOKEN-123'
- 결함ID: DEF-FE05-017
- 코드: front/src/api/api.ts

## FE05-018 조회 ID 인코딩
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 경로 삽입을 검증하고 서버 400 처리
- 실제: 실제 URL http://localhost:8080/api/diagnoses/1/../../: expected 'http://localhost:8080/api/diagnoses/1…' not to contain '/../'
- 결함ID: DEF-FE05-018
- 코드: front/src/api/api.ts
