# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE01-001 | 진단 DTO 유효성 | 정상 3필드 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-002 | 진단 DTO 유효성 | district 누락 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-003 | 진단 DTO 유효성 | district null | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-004 | 진단 DTO 유효성 | district 빈 문자열 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-005 | 진단 DTO 유효성 | district 공백만 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-006 | 진단 DTO 유효성 | dong 누락 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-007 | 진단 DTO 유효성 | dong null | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-008 | 진단 DTO 유효성 | dong 빈 문자열 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-009 | 진단 DTO 유효성 | dong 공백만 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-010 | 진단 DTO 유효성 | industry 누락 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-011 | 진단 DTO 유효성 | industry null | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-012 | 진단 DTO 유효성 | industry 빈 문자열 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-013 | 진단 DTO 유효성 | industry 공백만 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-014 | 진단 DTO 유효성 | 필드 타입 숫자 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-015 | 진단 DTO 유효성 | 객체 대신 배열 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-016 | 진단 DTO 유효성 | 깨진 JSON | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-018 | 진단 DTO 유효성 | 키 대소문자 오류 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-022 | 진단 DTO 유효성 | 추가 필드 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE01-024 | 진단 DTO 유효성 | 예외 메시지 구성 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |

## BE01-001 정상 3필드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST {district:마포구,dong:연남동,industry:한식}가 201 Created. 응답에 VALIDATION_ERROR가 없고 @Valid를 통과했다.

## BE01-002 district 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district 키를 뺀 POST는 400, body errorCode=VALIDATION_ERROR.

## BE01-003 district null
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district=null POST는 400, errorCode=VALIDATION_ERROR.

## BE01-004 district 빈 문자열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district="" POST는 400, errorCode=VALIDATION_ERROR.

## BE01-005 district 공백만
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district가 공백만인 POST는 400, errorCode=VALIDATION_ERROR.

## BE01-006 dong 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong 키를 뺀 POST는 400, errorCode=VALIDATION_ERROR.

## BE01-007 dong null
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong=null POST는 400, errorCode=VALIDATION_ERROR.

## BE01-008 dong 빈 문자열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong="" POST는 400, errorCode=VALIDATION_ERROR.

## BE01-009 dong 공백만
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong이 공백만인 POST는 400, errorCode=VALIDATION_ERROR.

## BE01-010 industry 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industry 키를 뺀 POST는 400, errorCode=VALIDATION_ERROR.

## BE01-011 industry null
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industry=null POST는 400, errorCode=VALIDATION_ERROR.

## BE01-012 industry 빈 문자열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industry="" POST는 400, errorCode=VALIDATION_ERROR.

## BE01-013 industry 공백만
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industry가 공백만인 POST는 400, errorCode=VALIDATION_ERROR.

## BE01-014 필드 타입 숫자
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industry=123은 400이 아니라 201. AiClient로 전달된 industry 값은 문자열 "123"으로 Jackson이 변환했다.

## BE01-015 객체 대신 배열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 본문 [] POST는 400, errorCode=INVALID_JSON.

## BE01-016 깨진 JSON
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 깨진 JSON {'district': POST는 400, errorCode=INVALID_JSON.

## BE01-018 키 대소문자 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 키 District/DOng은 바인딩되지 않아 400, errorCode=VALIDATION_ERROR.

## BE01-022 추가 필드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: extra=value를 추가한 정상 요청은 201. 응답 district/dong/industry는 원값이고 extra 속성은 없다.

## BE01-024 예외 메시지 구성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district와 dong을 동시에 빼면 400 VALIDATION_ERROR. message에 district와 dong이 함께 들어 있다.
