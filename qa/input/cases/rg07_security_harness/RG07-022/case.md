# RG07-022 최대 재시도 초과

| 항목 | 내용 |
| --- | --- |
| TC ID | RG07-022 |
| 분야 | RG07_보안하네스 |
| 세부 기능 | RAG 입력 검증·가드레일 |
| 원자 검증 항목 | 최대 재시도 초과 |
| 우선순위 | P0 |
| 테스트 구분 | 경계/예외 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/harness/runtime.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/harness/runtime.py |

## 검증 목적

RAG 입력 검증·가드레일에서 '최대 재시도 초과' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RAG 입력 검증·가드레일 모듈 준비; 입력 사례 '최대 재시도 초과'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

항상 예외

## 실행 절차

1. 항상 예외 준비
2. RAG 입력 검증·가드레일의 '최대 재시도 초과' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

fallback value/실패 이유

## 판정 기준

PASS: fallback value/실패 이유 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 항상 예외이면 fallback 값과 최대 재시도 실패 이유를 반환한다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
