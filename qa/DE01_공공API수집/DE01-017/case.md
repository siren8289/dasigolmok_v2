# DE01-017 비정상 JSON

| 항목 | 내용 |
| --- | --- |
| TC ID | DE01-017 |
| 분야 | DE01_공공API수집 |
| 세부 기능 | 소상공인 API·서울시 수집 |
| 원자 검증 항목 | 비정상 JSON |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/fixture + CSV검증 |
| 관련 코드 경로 | `data/etl/fetch.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/data/etl/fetch.py |

## 검증 목적

소상공인 API·서울시 수집에서 '비정상 JSON' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

소상공인 API·서울시 수집 모듈 준비; 입력 사례 '비정상 JSON'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

HTTP 200 HTML body

## 실행 절차

1. HTTP 200 HTML body 준비
2. 소상공인 API·서울시 수집의 '비정상 JSON' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

명확한 디코딩 실패

## 판정 기준

PASS: 명확한 디코딩 실패 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | HTTP 200 HTML 본문은 JSONDecodeError. 디코딩 실패가 전파됨. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
