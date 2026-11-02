# RG06-024 빈 질문

| 항목 | 내용 |
| --- | --- |
| TC ID | RG06-024 |
| 분야 | RG06_오케스트레이션 |
| 세부 기능 | RAG 의도분류·분기 |
| 원자 검증 항목 | 빈 질문 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/orchestration/workflow.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/orchestration/workflow.py |

## 검증 목적

RAG 의도분류·분기에서 '빈 질문' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RAG 의도분류·분기 모듈 준비; 입력 사례 '빈 질문'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

question=''

## 실행 절차

1. question='' 준비
2. RAG 의도분류·분기의 '빈 질문' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

명확한 입력 오류 안내

## 판정 기준

PASS: 명확한 입력 오류 안내 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | 빈 질문이 intent=hybrid로 처리되고 입력 오류 안내가 없음 |
| 결함 ID (Q) | DEF-RG06-024 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
