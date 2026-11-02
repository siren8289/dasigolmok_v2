# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE06-011 | Spring 에러 표준화·로그 | NULL 오류 메시지 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE06-013 | Spring 에러 표준화·로그 | HTTP 405 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE06-014 | Spring 에러 표준화·로그 | 타입 변환 오류 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |

## BE06-011 NULL 오류 메시지
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: Map.of NULL 처리 예외 추가 방지
- 실제: message=null인 ApiException을 처리하다 Map.of가 NullPointerException. errorCode/message JSON으로 막지 못함.
- 결함ID: DEF-BE06-011
- 코드: back/src/main/java/com/dasigolmok/global/exception/GlobalExceptionHandler.java

## BE06-013 HTTP 405
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 405 상태 확인
- 실제: DELETE /api/options는 405가 아니라 500. body errorCode=INTERNAL_ERROR, message=서버 오류가 발생했습니다.
- 결함ID: DEF-BE06-013
- 코드: back/src/main/java/com/dasigolmok/global/exception/GlobalExceptionHandler.java

## BE06-014 타입 변환 오류
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 400/공통 JSON 포맷 적용
- 실제: GET /api/diagnoses/abc는 400이 아니라 500. Content-Type은 application/json이고 errorCode=INTERNAL_ERROR. 공통 포맷이나 상태코드가 400이 아님.
- 결함ID: DEF-BE06-014
- 코드: back/src/main/java/com/dasigolmok/global/exception/GlobalExceptionHandler.java
