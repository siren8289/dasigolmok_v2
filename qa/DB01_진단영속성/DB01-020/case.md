# DB01-020 데이터 접근 경계

| 항목 | 내용 |
| --- | --- |
| TC ID | DB01-020 |
| 분야 | DB01_진단영속성 |
| 세부 기능 | JPA 엔터티·Repository |
| 원자 검증 항목 | 데이터 접근 경계 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/diagnosis/entity/Diagnosis.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/diagnosis/entity/Diagnosis.java |

## 검증 목적

JPA 엔터티·Repository에서 '데이터 접근 경계' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

JPA 엔터티·Repository 모듈 준비; 입력 사례 '데이터 접근 경계'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

인증 없는 단건 GET

## 실행 절차

1. 인증 없는 단건 GET 준비
2. JPA 엔터티·Repository의 '데이터 접근 경계' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

개인정보/소유권 정책 검증

## 판정 기준

PASS: 개인정보/소유권 정책 검증 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | 인증 없는 GET /api/diagnoses/{id}가 Diagnosis를 그대로 반환한다. build.gradle에 Spring Security가 없고 diagnosis에 user_id가 없어 소유권 검사를 할 수 없다. 개인정보/소유권 정책이 없다. |
| 결함 ID (Q) | DEF-DB01-020 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
