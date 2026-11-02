# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE02-022 | 진단 서비스·저장 | 숫자 문자열 혼입 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE02-023 | 진단 서비스·저장 | AI 필수 키 누락 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE02-024 | 진단 서비스·저장 | 설명 2000자 초과 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |

## BE02-022 숫자 문자열 혼입
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 잘못된 숫자는 null 처리되고 결측치 보완/거절 검증
- 실제: close_rate 문자열 "5.0"은 Double로 파싱되지 않고 closeRate=null인 채 저장됨(id 부여, 예외 없음). 결측 보완이나 거절이 없다.
- 결함ID: DEF-BE02-022
- 코드: back/src/main/java/com/dasigolmok/diagnosis/service/DiagnosisService.java

## BE02-023 AI 필수 키 누락
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 0/빈값으로 성공 저장하지 않도록 스키마 검증
- 실제: AI 응답 {}를 스키마 검증 없이 성공 저장. 관측값 status='', closeRate=null, danger=false이고 id가 발급됨.
- 결함ID: DEF-BE02-023
- 코드: back/src/main/java/com/dasigolmok/diagnosis/service/DiagnosisService.java

## BE02-024 설명 2000자 초과
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: DB 길이 초과 전에 명확한 검증·절단 처리
- 실제: explanation 4000자에서 사전 검증·절단 없이 DataIntegrityViolationException. H2 메시지: Value too long for column EXPLANATION CHARACTER VARYING(2000).
- 결함ID: DEF-BE02-024
- 코드: back/src/main/java/com/dasigolmok/diagnosis/service/DiagnosisService.java
