# RG08-014 종료 정책 오안내 1건

| 항목 | 내용 |
| --- | --- |
| TC ID | RG08-014 |
| 분야 | RG08_RAG정량평가 |
| 세부 기능 | RAG 품질 지표·평가 |
| 원자 검증 항목 | 종료 정책 오안내 1건 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/harness/runtime.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/harness/runtime.py |

## 검증 목적

RAG 품질 지표·평가에서 '종료 정책 오안내 1건' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RAG 품질 지표·평가 모듈 준비; 입력 사례 '종료 정책 오안내 1건'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

closed is_open=True 1건

## 실행 절차

1. closed is_open=True 1건 준비
2. RAG 품질 지표·평가의 '종료 정책 오안내 1건' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

오안내율 1/N

## 판정 기준

PASS: 오안내율 1/N 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | closed 인데 is_open=True 가 1건이면 오안내율은 1/N 이다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
