# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE03-005 | Spring 진단 HTTP 계약 | 단건 잘못된 ID | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE03-008 | Spring 진단 HTTP 계약 | 단건 id 너무 큼 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE03-010 | Spring 진단 HTTP 계약 | 메서드 허용 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE03-014 | Spring 진단 HTTP 계약 | 조회 ID 타인 데이터 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |

## BE03-005 단건 잘못된 ID
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 400 type mismatch
- 실제: GET /api/diagnoses/abc는 400 type mismatch가 아니라 500. body errorCode=INTERNAL_ERROR, message=서버 오류가 발생했습니다.
- 결함ID: DEF-BE03-005
- 코드: back/src/main/java/com/dasigolmok/diagnosis/controller/DiagnosisController.java

## BE03-008 단건 id 너무 큼
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 400
- 실제: GET /api/diagnoses/99999999999999999999는 Long 범위를 넘지만 400이 아니라 500 INTERNAL_ERROR.
- 결함ID: DEF-BE03-008
- 코드: back/src/main/java/com/dasigolmok/diagnosis/controller/DiagnosisController.java

## BE03-010 메서드 허용
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 405
- 실제: DELETE /api/diagnoses/1은 405가 아니라 500 INTERNAL_ERROR. 허용되지 않은 메서드가 공통 Exception 핸들러로 떨어짐.
- 결함ID: DEF-BE03-010
- 코드: back/src/main/java/com/dasigolmok/diagnosis/controller/DiagnosisController.java

## BE03-014 조회 ID 타인 데이터
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 접근제어/프라이버시 정책 확인
- 실제: Authorization 없는 GET /api/diagnoses/{id}가 401/403이 아니라 200. 저장 진단 JSON(마포구/연남동/한식)이 그대로 반환됨.
- 결함ID: DEF-BE03-014
- 코드: back/src/main/java/com/dasigolmok/diagnosis/controller/DiagnosisController.java
