# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE01-017 | 진단 DTO 유효성 | JSON Content-Type 누락 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE01-019 | 진단 DTO 유효성 | 10000자 district | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE01-020 | 진단 DTO 유효성 | 스크립트 동 이름 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE01-021 | 진단 DTO 유효성 | SQL 문장 업종 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE01-023 | 진단 DTO 유효성 | 지역·동 불일치 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |

## BE01-017 JSON Content-Type 누락
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 415 또는 400 일관 정책
- 실제: text/plain POST /api/diagnoses가 415 또는 400이 아니라 500. body={"errorCode":"INTERNAL_ERROR","message":"서버 오류가 발생했습니다."}. HttpMediaTypeNotSupportedException이 공통 Exception 핸들러에 흡수됨.
- 결함ID: DEF-BE01-017
- 코드: back/src/main/java/com/dasigolmok/diagnosis/dto/DiagnosisRequest.java

## BE01-019 10000자 district
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 입력 길이 제한과 안전한 응답 검증
- 실제: district 10000자를 AI 응답에 실어 저장하자 400/413/422나 255자 절단이 아니라 500 INTERNAL_ERROR. @NotBlank 외 길이 제한이 없고 DB 단계에서 실패.
- 결함ID: DEF-BE01-019
- 코드: back/src/main/java/com/dasigolmok/diagnosis/dto/DiagnosisRequest.java

## BE01-020 스크립트 동 이름
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: HTML 실행 없이 안전한 오류·데이터 반환
- 실제: dong=<script>alert(1)</script>가 거절되지 않고 201. 응답 dong에 script 태그가 그대로 있음. application/json이지만 살균·입력 거절 없음.
- 결함ID: DEF-BE01-020
- 코드: back/src/main/java/com/dasigolmok/diagnosis/dto/DiagnosisRequest.java

## BE01-021 SQL 문장 업종
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: DB 인젝션 없이 입력 거절·안전처리
- 실제: industry="; DROP TABLE diagnosis;--"가 400/422로 거절되지 않고 201. diagnosis COUNT=1로 행이 생성됨. 테이블 조회는 되나 입력 거절은 없음.
- 결함ID: DEF-BE01-021
- 코드: back/src/main/java/com/dasigolmok/diagnosis/dto/DiagnosisRequest.java

## BE01-023 지역·동 불일치
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 상위 계층에서 조합 검증 필요
- 실제: 마포구/역삼동 POST가 400이 아니라 201. 응답 district=마포구, dong=역삼동으로 저장됨. 지역·동 조합 검증 없음.
- 결함ID: DEF-BE01-023
- 코드: back/src/main/java/com/dasigolmok/diagnosis/dto/DiagnosisRequest.java
