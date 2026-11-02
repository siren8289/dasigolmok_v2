# RG01_RAG_HTTP

- 세부 기능: 상권 RAG API
- 케이스: 20
- 코드: `ai/src/features/commercial_rag_001/router.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [RG01-001](./RG01-001/case.md) | RAG health | P1 | 구현기반 | PASS | — |
| [RG01-002](./RG01-002/case.md) | RAG ask 정상 | P1 | 구현기반 | PASS | — |
| [RG01-003](./RG01-003/case.md) | 시장 검색 정상 | P1 | 구현기반 | PASS | — |
| [RG01-004](./RG01-004/case.md) | 정책 검색 정상 | P1 | 구현기반 | PASS | — |
| [RG01-005](./RG01-005/case.md) | 평가 정상 | P1 | 구현기반 | PASS | — |
| [RG01-006](./RG01-006/case.md) | RAG ask question 누락 | P0 | 구현기반 | PASS | — |
| [RG01-007](./RG01-007/case.md) | RAG ask question null | P1 | 구현기반 | PASS | — |
| [RG01-008](./RG01-008/case.md) | RAG ask question 빈문자열 | P1 | 개선제안 | FAIL | DEF-RG01-008 |
| [RG01-009](./RG01-009/case.md) | 시장 검색 query 누락 | P0 | 구현기반 | PASS | — |
| [RG01-010](./RG01-010/case.md) | 정책 검색 입력 없음 | P1 | 구현기반 | PASS | — |
| [RG01-011](./RG01-011/case.md) | 지원 정책 top_k 음수 | P1 | 개선제안 | FAIL | DEF-RG01-011 |
| [RG01-012](./RG01-012/case.md) | 시장 검색 top_k=0 | P1 | 개선제안 | FAIL | DEF-RG01-012 |
| [RG01-013](./RG01-013/case.md) | 지원 정책 날짜 형식 | P1 | 개선제안 | FAIL | DEF-RG01-013 |
| [RG01-014](./RG01-014/case.md) | RAG ask 내부 예외 | P1 | 구현기반 | PASS | — |
| [RG01-015](./RG01-015/case.md) | 지원 정책 내부 예외 | P1 | 구현기반 | PASS | — |
| [RG01-016](./RG01-016/case.md) | 평가 내부 예외 | P1 | 구현기반 | PASS | — |
| [RG01-017](./RG01-017/case.md) | RAG 장애 정보 마스킹 | P0 | 개선제안 | FAIL | DEF-RG01-017 |
| [RG01-018](./RG01-018/case.md) | RAG JSON 응답 타입 | P1 | 구현기반 | PASS | — |
| [RG01-019](./RG01-019/case.md) | RAG 직접 공개 여부 | P1 | 개선제안 | FAIL | DEF-RG01-019 |
| [RG01-020](./RG01-020/case.md) | RAG 과도한 요청 | P1 | 개선제안 | FAIL | DEF-RG01-020 |
