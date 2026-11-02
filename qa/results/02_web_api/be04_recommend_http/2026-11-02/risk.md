# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE04-001 | 옵션·추천 HTTP | 옵션 GET | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-002 | 옵션·추천 HTTP | 추천 POST | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-003 | 옵션·추천 HTTP | 추천 district 누락 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-004 | 옵션·추천 HTTP | 추천 district 공백 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-005 | 옵션·추천 HTTP | 추천 dong 누락 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-006 | 옵션·추천 HTTP | 추천 dong 공백 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-007 | 옵션·추천 HTTP | 추천 JSON 오류 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-008 | 옵션·추천 HTTP | 추천 잘못된 지역 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-009 | 옵션·추천 HTTP | GET /api/options 후 응답 null | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-010 | 옵션·추천 HTTP | 옵션 응답 형태 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-011 | 옵션·추천 HTTP | 추천 응답 전체 업종 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-012 | 옵션·추천 HTTP | 추천 top5 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-013 | 옵션·추천 HTTP | 추천 실패 DB 비저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-014 | 옵션·추천 HTTP | POST 동시 요청 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-015 | 옵션·추천 HTTP | 옵션 GET 오류 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE04-017 | 옵션·추천 HTTP | 불필요한 필드 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |

## BE04-001 옵션 GET
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GET /api/options는 200. districts/dongs/industries JSON이 스텁한 AI 본문과 동일했다.

## BE04-002 추천 POST
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST /api/recommendations 마포구/연남동은 200. AI 추천 JSON이 그대로 반환됐다.

## BE04-003 추천 district 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district 누락 추천 POST는 400, errorCode=VALIDATION_ERROR.

## BE04-004 추천 district 공백
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district가 공백인 추천 POST는 400, errorCode=VALIDATION_ERROR.

## BE04-005 추천 dong 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong 누락 추천 POST는 400, errorCode=VALIDATION_ERROR.

## BE04-006 추천 dong 공백
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong이 공백인 추천 POST는 400, errorCode=VALIDATION_ERROR.

## BE04-007 추천 JSON 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 깨진 추천 JSON은 400, errorCode=INVALID_JSON.

## BE04-008 추천 잘못된 지역
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: AI HTTP 404는 Spring 502로 변환됐다. body errorCode=AI_ERROR, message 필드가 있다.

## BE04-009 GET /api/options 후 응답 null
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: options용 RestTemplate이 null을 반환하면 200 빈 본문이 아니라 502, errorCode=AI_ERROR.

## BE04-010 옵션 응답 형태
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GET /api/options 200. districts 2개, dongs.마포구 두 번째 값이 성산동으로 배열 구조가 유지됐다.

## BE04-011 추천 응답 전체 업종
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: all_industries 순서는 한식(score 2.0, status stable) 다음 카페. 필드와 순서가 보존됐다.

## BE04-012 추천 top5
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: recommendations 길이는 5이고 업종1부터 업종5 순서가 유지됐다.

## BE04-013 추천 실패 DB 비저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 추천 AI 404는 4xx/5xx이고 전후 diagnosis 행 수가 같았다. 추천 전용 저장은 없다.

## BE04-014 POST 동시 요청
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마포구/연남동, 강남구/역삼동, 종로구/청운효자동, 용산구/이태원동 병렬 POST가 각각 200이고 응답 지역이 요청과 같았다.

## BE04-015 옵션 GET 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: options Read timed out은 502. errorCode=AI_ERROR, message가 있고 본문에 SocketTimeoutException은 없다.

## BE04-017 불필요한 필드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industry를 추가한 추천 요청은 200. AI로 전달된 Map 키는 district, dong뿐이었다.
