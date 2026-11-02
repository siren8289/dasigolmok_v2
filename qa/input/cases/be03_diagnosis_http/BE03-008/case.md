# BE03-008 단건 id 너무 큼

| 항목 | 내용 |
| --- | --- |
| TC ID | BE03-008 |
| 분야 | BE03_진단HTTP |
| 세부 기능 | Spring 진단 HTTP 계약 |
| 원자 검증 항목 | 단건 id 너무 큼 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/diagnosis/controller/DiagnosisController.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/diagnosis/controller/DiagnosisController.java |

## 검증 목적

Spring 진단 HTTP 계약에서 '단건 id 너무 큼' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

Spring 진단 HTTP 계약 모듈 준비; 입력 사례 '단건 id 너무 큼'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

GET /api/diagnoses/99999999999999999999

## 실행 절차

1. GET /api/diagnoses/99999999999999999999 준비
2. Spring 진단 HTTP 계약의 '단건 id 너무 큼' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

400

## 판정 기준

PASS: 400 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | GET /api/diagnoses/99999999999999999999는 Long 범위를 넘지만 400이 아니라 500 INTERNAL_ERROR. |
| 결함 ID (Q) | DEF-BE03-008 |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
