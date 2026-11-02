# DB01-018 실수 특수 값

| 항목 | 내용 |
| --- | --- |
| TC ID | DB01-018 |
| 분야 | DB01_진단영속성 |
| 세부 기능 | JPA 엔터티·Repository |
| 원자 검증 항목 | 실수 특수 값 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/diagnosis/entity/Diagnosis.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/diagnosis/entity/Diagnosis.java |

## 검증 목적

JPA 엔터티·Repository에서 '실수 특수 값' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

JPA 엔터티·Repository 모듈 준비; 입력 사례 '실수 특수 값'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

Float NaN/Inf

## 실행 절차

1. Float NaN/Inf 준비
2. JPA 엔터티·Repository의 '실수 특수 값' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

DB 직렬화 허용 여부·응답 안전성 검증

## 판정 기준

PASS: DB 직렬화 허용 여부·응답 안전성 검증 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | PostgreSQL float8이 NaN과 Infinity를 저장·재조회한다. Diagnosis Double 필드에는 거절이나 안전 직렬화 가드가 없어 DB 직렬화 허용 여부가 열려 있고 응답 안전성이 보장되지 않는다. |
| 결함 ID (Q) | DEF-DB01-018 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
