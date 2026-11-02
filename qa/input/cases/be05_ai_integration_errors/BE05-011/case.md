# BE05-011 AI 404

| 항목 | 내용 |
| --- | --- |
| TC ID | BE05-011 |
| 분야 | BE05_AI연동예외 |
| 세부 기능 | RestTemplate 연동·오류 |
| 원자 검증 항목 | AI 404 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/ai/AiClient.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/ai/AiClient.java |

## 검증 목적

RestTemplate 연동·오류에서 'AI 404' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RestTemplate 연동·오류 모듈 준비; 입력 사례 'AI 404'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

HTTP 404 응답

## 실행 절차

1. HTTP 404 응답 준비
2. RestTemplate 연동·오류의 'AI 404' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

의도된 Spring 에러코드로 변환·구분

## 판정 기준

PASS: 의도된 Spring 에러코드로 변환·구분 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | AI HTTP 404와 HTTP 500이 모두 ApiException errorCode=AI_ERROR, status 502. 404 전용 코드로 구분되지 않음. |
| 결함 ID (Q) | DEF-BE05-011 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
