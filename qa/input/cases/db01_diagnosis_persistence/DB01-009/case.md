# DB01-009 위험 boolean true

| 항목 | 내용 |
| --- | --- |
| TC ID | DB01-009 |
| 분야 | DB01_진단영속성 |
| 세부 기능 | JPA 엔터티·Repository |
| 원자 검증 항목 | 위험 boolean true |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/diagnosis/entity/Diagnosis.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/diagnosis/entity/Diagnosis.java |

## 검증 목적

JPA 엔터티·Repository에서 '위험 boolean true' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

JPA 엔터티·Repository 모듈 준비; 입력 사례 '위험 boolean true'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

is_danger=true

## 실행 절차

1. is_danger=true 준비
2. JPA 엔터티·Repository의 '위험 boolean true' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

true 보존

## 판정 기준

PASS: true 보존 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | danger=true 가 false로 바뀌지 않고 true로 조회됐다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
