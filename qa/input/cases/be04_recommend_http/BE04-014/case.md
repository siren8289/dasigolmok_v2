# BE04-014 POST 동시 요청

| 항목 | 내용 |
| --- | --- |
| TC ID | BE04-014 |
| 분야 | BE04_추천HTTP |
| 세부 기능 | 옵션·추천 HTTP |
| 원자 검증 항목 | POST 동시 요청 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/recommend/controller/RecommendController.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/recommend/controller/RecommendController.java |

## 검증 목적

옵션·추천 HTTP에서 'POST 동시 요청' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

옵션·추천 HTTP 모듈 준비; 입력 사례 'POST 동시 요청'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

여러 지역 동시

## 실행 절차

1. 여러 지역 동시 준비
2. 옵션·추천 HTTP의 'POST 동시 요청' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

요청 간 데이터 섞이지 않음

## 판정 기준

PASS: 요청 간 데이터 섞이지 않음 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 마포구/연남동, 강남구/역삼동, 종로구/청운효자동, 용산구/이태원동 병렬 POST가 각각 200이고 응답 지역이 요청과 같았다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
