# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE05-001 | RestTemplate 연동·오류 | 옵션 URL | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-002 | RestTemplate 연동·오류 | 진단 URL | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-003 | RestTemplate 연동·오류 | 추천 URL | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-004 | RestTemplate 연동·오류 | AI 옵션 정상 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-005 | RestTemplate 연동·오류 | AI 진단 정상 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-006 | RestTemplate 연동·오류 | AI 추천 정상 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-007 | RestTemplate 연동·오류 | AI null 응답 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-008 | RestTemplate 연동·오류 | 연결거부 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-009 | RestTemplate 연동·오류 | DNS 실패 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-010 | RestTemplate 연동·오류 | AI Timeout | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-013 | RestTemplate 연동·오류 | AI 500 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-017 | RestTemplate 연동·오류 | 동시 요청 pool | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE05-020 | RestTemplate 연동·오류 | 고의 무한대기 서버 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |

## BE05-001 옵션 URL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: baseUrl http://ai:8000에서 options()가 GET http://ai:8000/api/v1/options를 호출했다.

## BE05-002 진단 URL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: diagnose()가 POST http://ai:8000/api/v1/diagnose를 호출했다.

## BE05-003 추천 URL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: recommend()가 POST http://ai:8000/api/v1/recommend를 호출했다.

## BE05-004 AI 옵션 정상
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: options() 200 JSON 스텁이 JsonNode로 그대로 반환됐다. districts=[마포구].

## BE05-005 AI 진단 정상
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: diagnose()가 스텁 JsonNode {status:stable}를 반환했다.

## BE05-006 AI 추천 정상
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: recommend()가 스텁 JsonNode {recommendations:[]}를 반환했다.

## BE05-007 AI null 응답
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: getForObject가 null이면 ApiException errorCode=AI_ERROR, HTTP 502.

## BE05-008 연결거부
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: Connection refused를 감싼 ResourceAccessException이 AI_ERROR 502로 변환됐다.

## BE05-009 DNS 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: UnknownHostException을 cause로 둔 ResourceAccessException이 AI_ERROR로 변환됐다.

## BE05-010 AI Timeout
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: Read timed out ResourceAccessException이 AI_ERROR, HTTP 502로 변환됐다.

## BE05-013 AI 500
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: AI 500 본문의 IllegalStateException, com.internal, Model.java가 ApiException 메시지와 핸들러 응답 JSON에 없었다.

## BE05-017 동시 요청 pool
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 동시 20건 options()가 5초 안에 모두 JsonNode를 반환. 빈 RestTemplate 팩토리 connectTimeout=3000, readTimeout=40000.

## BE05-020 고의 무한대기 서버
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 운영 RestTemplate 요청 팩토리는 SimpleClientHttpRequestFactory. connectTimeout=3000, readTimeout=40000.
