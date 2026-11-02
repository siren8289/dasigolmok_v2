# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG06-020 | RAG 의도분류·분기 | 검색 타임아웃 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG06-021 | RAG 의도분류·분기 | 검색 예외 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG06-024 | RAG 의도분류·분기 | 빈 질문 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG06-025 | RAG 의도분류·분기 | 질문 10만자 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## RG06-020 검색 타임아웃
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 전체 실패 아닌 부분적 degraded 안내
- 실제: 상권 검색 TimeoutError 가 워크플로우 전체로 전파되고 부분 안내가 없음
- 결함ID: DEF-RG06-020
- 코드: ai/src/features/commercial_rag_001/orchestration/workflow.py

## RG06-021 검색 예외
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 다른 결과 유지·경고 전파
- 실제: 정책 검색 예외가 상권 결과까지 폐기함
- 결함ID: DEF-RG06-021
- 코드: ai/src/features/commercial_rag_001/orchestration/workflow.py

## RG06-024 빈 질문
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 명확한 입력 오류 안내
- 실제: 빈 질문이 intent=hybrid로 처리되고 입력 오류 안내가 없음
- 결함ID: DEF-RG06-024
- 코드: ai/src/features/commercial_rag_001/orchestration/workflow.py

## RG06-025 질문 10만자
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 입력 제한, API 비용 통제
- 실제: 10만 자 질문이 길이 제한 없이 수용됨
- 결함ID: DEF-RG06-025
- 코드: ai/src/features/commercial_rag_001/orchestration/workflow.py
