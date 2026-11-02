# AI05-009 폐업률 4% HL

| 항목 | 내용 |
| --- | --- |
| TC ID | AI05-009 |
| 분야 | AI05_위험판정경계 |
| 세부 기능 | classify 규칙·경계 |
| 원자 검증 항목 | 폐업률 4% HL |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/risk.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/risk.py |

## 검증 목적

classify 규칙·경계에서 '폐업률 4% HL' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

classify 규칙·경계 모듈 준비; 입력 사례 '폐업률 4% HL'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

4,HL

## 실행 절차

1. 4,HL 준비
2. classify 규칙·경계의 '폐업률 4% HL' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

danger,true

## 판정 기준

PASS: danger,true 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | classify(4,'HL')=('danger', True) 기대=('danger',True) |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
