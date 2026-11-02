# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE03-001 | Spring 진단 HTTP 계약 | POST 상태 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE03-002 | Spring 진단 HTTP 계약 | POST 응답 id | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE03-003 | Spring 진단 HTTP 계약 | GET 단건 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE03-004 | Spring 진단 HTTP 계약 | GET 최근 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE03-006 | Spring 진단 HTTP 계약 | 단건 0 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE03-007 | Spring 진단 HTTP 계약 | 단건 음수 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE03-009 | Spring 진단 HTTP 계약 | Content-Type | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE03-011 | Spring 진단 HTTP 계약 | 다중 검증 실패 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE03-012 | Spring 진단 HTTP 계약 | 404 코드 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE03-013 | Spring 진단 HTTP 계약 | API 응답 한글 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |

## BE03-001 POST 상태
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 유효 진단 POST /api/diagnoses 응답 상태 201 Created.

## BE03-002 POST 응답 id
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: H2 identity를 10으로 재시작 후 POST 응답 JSON id=10.

## BE03-003 GET 단건
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: id=10 행을 넣은 뒤 GET /api/diagnoses/10은 200. district=마포구, dong=연남동, industry=한식.

## BE03-004 GET 최근
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GET /api/diagnoses는 200이고 본문은 JSON 배열이며 크기 1 이상.

## BE03-006 단건 0
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GET /api/diagnoses/0은 404.

## BE03-007 단건 음수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GET /api/diagnoses/-1은 404.

## BE03-009 Content-Type
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST JSON 응답 Content-Type에 application/json이 포함됐다.

## BE03-011 다중 검증 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district/dong/industry를 모두 빈 문자열로 보내면 400. message에 세 필드명이 모두 있다.

## BE03-012 404 코드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 없는 id GET /api/diagnoses/424242는 404이고 body에 errorCode=NOT_FOUND.

## BE03-013 API 응답 한글
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 201 응답 본문에 연남동과 기본 설명이 UTF-8로 그대로 있고 ??? 또는 占 깨짐은 없다.
