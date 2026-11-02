# BE02-015 점포당 매출 저장

| 항목 | 내용 |
| --- | --- |
| TC ID | BE02-015 |
| 분야 | BE02_진단CRUD |
| 세부 기능 | 진단 서비스·저장 |
| 원자 검증 항목 | 점포당 매출 저장 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/diagnosis/service/DiagnosisService.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/diagnosis/service/DiagnosisService.java |

## 검증 목적

진단 서비스·저장에서 '점포당 매출 저장' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

진단 서비스·저장 모듈 준비; 입력 사례 '점포당 매출 저장'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

sales_per_store=800.5

## 실행 절차

1. sales_per_store=800.5 준비
2. 진단 서비스·저장의 '점포당 매출 저장' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

Double=800.5 저장

## 판정 기준

PASS: Double=800.5 저장 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | sales_per_store=800.5가 Double 800.5로 저장됐다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
