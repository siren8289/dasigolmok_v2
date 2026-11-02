# AI01-002 진단 API

| 항목 | 내용 |
| --- | --- |
| TC ID | AI01-002 |
| 분야 | AI01_FastAPI계약 |
| 세부 기능 | FastAPI 엔드포인트·스키마 |
| 원자 검증 항목 | 진단 API |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/main.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/main.py |

## 검증 목적

FastAPI 엔드포인트·스키마에서 '진단 API' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

FastAPI 엔드포인트·스키마 모듈 준비; 입력 사례 '진단 API'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

POST /api/v1/diagnose 유효 body

## 실행 절차

1. POST /api/v1/diagnose 유효 body 준비
2. FastAPI 엔드포인트·스키마의 '진단 API' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

200 진단 결과

## 판정 기준

PASS: 200 진단 결과 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | POST /api/v1/diagnose status=200 dong=연남동 status_field=warning ml=3.17 dl=4902.2 source=basic |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
