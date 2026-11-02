# BE06-007 사용자 오류 로그 수준

| 항목 | 내용 |
| --- | --- |
| TC ID | BE06-007 |
| 분야 | BE06_전역예외 |
| 세부 기능 | Spring 에러 표준화·로그 |
| 원자 검증 항목 | 사용자 오류 로그 수준 |
| 우선순위 | P0 |
| 테스트 구분 | 경계/예외 |
| 근거 분류 | 구현기반 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/global/exception/GlobalExceptionHandler.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/global/exception/GlobalExceptionHandler.java |

## 검증 목적

Spring 에러 표준화·로그에서 '사용자 오류 로그 수준' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

Spring 에러 표준화·로그 모듈 준비; 입력 사례 '사용자 오류 로그 수준'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

ApiException 4xx

## 실행 절차

1. ApiException 4xx 준비
2. Spring 에러 표준화·로그의 '사용자 오류 로그 수준' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

불필요한 스택 로그 제한

## 판정 기준

PASS: 불필요한 스택 로그 제한 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 4xx NOT_FOUND 처리 시 GlobalExceptionHandler ERROR 로그와 throwable이 없었다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
