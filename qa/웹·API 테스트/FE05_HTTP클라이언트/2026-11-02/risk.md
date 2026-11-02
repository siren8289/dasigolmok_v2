# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| FE05-001 | 프론트 fetch API 계약 | baseURL 기본값 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-002 | 프론트 fetch API 계약 | baseURL 상대 경로 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-003 | 프론트 fetch API 계약 | 옵션 URL | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-004 | 프론트 fetch API 계약 | 진단 URL | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-005 | 프론트 fetch API 계약 | 결과 조회 URL | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-006 | 프론트 fetch API 계약 | 추천 URL | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-007 | 프론트 fetch API 계약 | JSON 헤더 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-008 | 프론트 fetch API 계약 | 문자열 JSON 직렬화 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-009 | 프론트 fetch API 계약 | HTTP 200 JSON | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-010 | 프론트 fetch API 계약 | HTTP 201 JSON | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-011 | 프론트 fetch API 계약 | 400 message 우선 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-012 | 프론트 fetch API 계약 | 422 detail 대체 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-013 | 프론트 fetch API 계약 | 500 비JSON | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE05-014 | 프론트 fetch API 계약 | 네트워크 실패 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |

## FE05-001 baseURL 기본값
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: VITE_API_URL 미설정 시 fetch URL이 http://localhost:8080/api/options 이다.

## FE05-002 baseURL 상대 경로
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: VITE_API_URL='' 이면 상대 경로 /api/options 로 현재 origin에 요청한다.

## FE05-003 옵션 URL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: getOptions()는 GET /api/options 이다.

## FE05-004 진단 URL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: createDiagnosis()는 POST /api/diagnoses 이다.

## FE05-005 결과 조회 URL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: getDiagnosis('17')는 GET /api/diagnoses/17 이다.

## FE05-006 추천 URL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: getRecommendations()는 POST /api/recommendations 이다.

## FE05-007 JSON 헤더
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST 두 건 모두 Content-Type application/json 이다.

## FE05-008 문자열 JSON 직렬화
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한글 district/dong/industry가 JSON 문자열에 그대로 들어간다.

## FE05-009 HTTP 200 JSON
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: HTTP 200 JSON이 호출자에게 그대로 반환된다.

## FE05-010 HTTP 201 JSON
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: HTTP 201 JSON도 ok로 보고 data를 반환한다.

## FE05-011 400 message 우선
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 400 body.message '오류'가 Error message로 전달된다.

## FE05-012 422 detail 대체
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: message가 없으면 detail '검증 실패'를 쓴다.

## FE05-013 500 비JSON
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: HTML 500은 기본 문구 '요청에 실패했습니다.'다.

## FE05-014 네트워크 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: fetch reject는 호출자 catch로 그대로 전파된다.
