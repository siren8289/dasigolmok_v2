# BE01-019 10000자 district

| 항목 | 내용 |
| --- | --- |
| TC ID | BE01-019 |
| 분야 | BE01_진단요청DTO |
| 세부 기능 | 진단 DTO 유효성 |
| 원자 검증 항목 | 10000자 district |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/diagnosis/dto/DiagnosisRequest.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/diagnosis/dto/DiagnosisRequest.java |

## 검증 목적

진단 DTO 유효성에서 '10000자 district' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

진단 DTO 유효성 모듈 준비; 입력 사례 '10000자 district'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

매우 긴 district

## 실행 절차

1. 매우 긴 district 준비
2. 진단 DTO 유효성의 '10000자 district' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

입력 길이 제한과 안전한 응답 검증

## 판정 기준

PASS: 입력 길이 제한과 안전한 응답 검증 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | district 10000자를 AI 응답에 실어 저장하자 400/413/422나 255자 절단이 아니라 500 INTERNAL_ERROR. @NotBlank 외 길이 제한이 없고 DB 단계에서 실패. |
| 결함 ID (Q) | DEF-BE01-019 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
