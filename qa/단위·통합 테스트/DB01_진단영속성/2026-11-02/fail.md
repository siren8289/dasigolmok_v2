# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DB01-018 | JPA 엔터티·Repository | 실수 특수 값 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| DB01-020 | JPA 엔터티·Repository | 데이터 접근 경계 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |

## DB01-018 실수 특수 값
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: DB 직렬화 허용 여부·응답 안전성 검증
- 실제: PostgreSQL float8이 NaN과 Infinity를 저장·재조회한다. Diagnosis Double 필드에는 거절이나 안전 직렬화 가드가 없어 DB 직렬화 허용 여부가 열려 있고 응답 안전성이 보장되지 않는다.
- 결함ID: DEF-DB01-018
- 코드: back/src/main/java/com/dasigolmok/diagnosis/entity/Diagnosis.java

## DB01-020 데이터 접근 경계
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 개인정보/소유권 정책 검증
- 실제: 인증 없는 GET /api/diagnoses/{id}가 Diagnosis를 그대로 반환한다. build.gradle에 Spring Security가 없고 diagnosis에 user_id가 없어 소유권 검사를 할 수 없다. 개인정보/소유권 정책이 없다.
- 결함ID: DEF-DB01-020
- 코드: back/src/main/java/com/dasigolmok/diagnosis/entity/Diagnosis.java
