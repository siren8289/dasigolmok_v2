# RG06-011 진단정보 누락

| 항목 | 내용 |
| --- | --- |
| TC ID | RG06-011 |
| 분야 | RG06_오케스트레이션 |
| 세부 기능 | RAG 의도분류·분기 |
| 원자 검증 항목 | 진단정보 누락 |
| 우선순위 | P0 |
| 테스트 구분 | 경계/예외 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/orchestration/workflow.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/orchestration/workflow.py |

## 검증 목적

RAG 의도분류·분기에서 '진단정보 누락' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RAG 의도분류·분기 모듈 준비; 입력 사례 '진단정보 누락'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

dong만 제공

## 실행 절차

1. dong만 제공 준비
2. RAG 의도분류·분기의 '진단정보 누락' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

안전하게 진단 생략

## 판정 기준

PASS: 안전하게 진단 생략 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | dong 만 있고 industry 가 없으면 진단을 생략한다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
