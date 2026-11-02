# BE04-012 추천 top5

| 항목 | 내용 |
| --- | --- |
| TC ID | BE04-012 |
| 분야 | BE04_추천HTTP |
| 세부 기능 | 옵션·추천 HTTP |
| 원자 검증 항목 | 추천 top5 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/recommend/controller/RecommendController.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/recommend/controller/RecommendController.java |

## 검증 목적

옵션·추천 HTTP에서 '추천 top5' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

옵션·추천 HTTP 모듈 준비; 입력 사례 '추천 top5'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

recommendations[]

## 실행 절차

1. recommendations[] 준비
2. 옵션·추천 HTTP의 '추천 top5' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

최대 5개

## 판정 기준

PASS: 최대 5개 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | recommendations 길이는 5이고 업종1부터 업종5 순서가 유지됐다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
