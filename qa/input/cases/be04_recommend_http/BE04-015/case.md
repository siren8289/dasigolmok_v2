# BE04-015 옵션 GET 오류

| 항목 | 내용 |
| --- | --- |
| TC ID | BE04-015 |
| 분야 | BE04_추천HTTP |
| 세부 기능 | 옵션·추천 HTTP |
| 원자 검증 항목 | 옵션 GET 오류 |
| 우선순위 | P0 |
| 테스트 구분 | 경계/예외 |
| 근거 분류 | 구현기반 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/recommend/controller/RecommendController.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/recommend/controller/RecommendController.java |

## 검증 목적

옵션·추천 HTTP에서 '옵션 GET 오류' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

옵션·추천 HTTP 모듈 준비; 입력 사례 '옵션 GET 오류'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

AI timeout

## 실행 절차

1. AI timeout 준비
2. 옵션·추천 HTTP의 '옵션 GET 오류' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

GlobalExceptionHandler를 거쳐 상태코드·메시지 통일

## 판정 기준

PASS: GlobalExceptionHandler를 거쳐 상태코드·메시지 통일 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | options Read timed out은 502. errorCode=AI_ERROR, message가 있고 본문에 SocketTimeoutException은 없다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
