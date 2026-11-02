# BE05-018 AI 잘못된 주소

| 항목 | 내용 |
| --- | --- |
| TC ID | BE05-018 |
| 분야 | BE05_AI연동예외 |
| 세부 기능 | RestTemplate 연동·오류 |
| 원자 검증 항목 | AI 잘못된 주소 |
| 우선순위 | P0 |
| 테스트 구분 | 경계/예외 |
| 근거 분류 | 구현기반 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/ai/AiClient.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/ai/AiClient.java |

## 검증 목적

RestTemplate 연동·오류에서 'AI 잘못된 주소' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RestTemplate 연동·오류 모듈 준비; 입력 사례 'AI 잘못된 주소'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

APP_AI_BASE_URL=https://wrong

## 실행 절차

1. APP_AI_BASE_URL=https://wrong 준비
2. RestTemplate 연동·오류의 'AI 잘못된 주소' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

설정 오류 로그·안내

## 판정 기준

PASS: 설정 오류 로그·안내 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | baseUrl=https://wrong 실패 시 message=AI 서버 호출에 실패했습니다. 로그는 API error와 UnknownHost 스택뿐이고 설정/base-url 안내는 없음. |
| 결함 ID (Q) | DEF-BE05-018 |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
