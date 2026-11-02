# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG08-021 | RAG 품질 지표·평가 | 평가 품질 기준 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## RG08-021 평가 품질 기준
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 실제 운영품질 일반화 금지
- 실제: citation_accuracy=1.0 고정이고 표본/비운영 표시가 없어 운영품질로 일반화됨
- 결함ID: DEF-RG08-021
- 코드: ai/src/features/commercial_rag_001/harness/runtime.py
