# RG03_상권근거검색

- 세부 기능: 하이브리드 검색·재순위화
- 케이스: 27
- 코드: `ai/src/features/commercial_rag_001/market_search/service.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [RG03-001](./RG03-001/case.md) | 보고서만 검색 | P1 | 구현기반 | PASS | — |
| [RG03-002](./RG03-002/case.md) | 지역 일치 필터 | P1 | 구현기반 | PASS | — |
| [RG03-003](./RG03-003/case.md) | 지역 다름 배제 | P1 | 구현기반 | PASS | — |
| [RG03-004](./RG03-004/case.md) | 행정동 선택 | P1 | 구현기반 | PASS | — |
| [RG03-005](./RG03-005/case.md) | 구 선택 | P1 | 구현기반 | PASS | — |
| [RG03-006](./RG03-006/case.md) | 업종 선택 | P1 | 구현기반 | PASS | — |
| [RG03-007](./RG03-007/case.md) | 키워드 일치 | P1 | 구현기반 | PASS | — |
| [RG03-008](./RG03-008/case.md) | 유사도 원본 | P1 | 구현기반 | PASS | — |
| [RG03-009](./RG03-009/case.md) | rerank 정렬 | P1 | 구현기반 | PASS | — |
| [RG03-010](./RG03-010/case.md) | top_k 1 | P1 | 구현기반 | PASS | — |
| [RG03-011](./RG03-011/case.md) | top_k 3 | P1 | 구현기반 | PASS | — |
| [RG03-012](./RG03-012/case.md) | top_k 20 | P1 | 구현기반 | PASS | — |
| [RG03-013](./RG03-013/case.md) | 중복 문서 | P1 | 개선제안 | FAIL | DEF-RG03-013 |
| [RG03-014](./RG03-014/case.md) | 없는 자치구 | P1 | 구현기반 | PASS | — |
| [RG03-015](./RG03-015/case.md) | 없는 자치구 fallback 교차오염 | P1 | 개선제안 | FAIL | DEF-RG03-015 |
| [RG03-016](./RG03-016/case.md) | 동 매칭 불일치 | P0 | 개선제안 | FAIL | DEF-RG03-016 |
| [RG03-017](./RG03-017/case.md) | 업종 불일치 | P0 | 개선제안 | FAIL | DEF-RG03-017 |
| [RG03-018](./RG03-018/case.md) | 분기 조건 | P1 | 개선제안 | FAIL | DEF-RG03-018 |
| [RG03-019](./RG03-019/case.md) | 시점 최신성 | P1 | 개선제안 | FAIL | DEF-RG03-019 |
| [RG03-020](./RG03-020/case.md) | 문서 캐시 재사용 | P1 | 구현기반 | PASS | — |
| [RG03-021](./RG03-021/case.md) | 임베딩 캐시 재사용 | P1 | 구현기반 | PASS | — |
| [RG03-022](./RG03-022/case.md) | pgvector SQL | P1 | 구현기반 | PASS | — |
| [RG03-023](./RG03-023/case.md) | pgvector SQL 파라미터 | P1 | 구현기반 | PASS | — |
| [RG03-024](./RG03-024/case.md) | pgvector 연결 실패 | P1 | 구현기반 | PASS | — |
| [RG03-025](./RG03-025/case.md) | pgvector 임베딩 차원 | P1 | 개선제안 | FAIL | DEF-RG03-025 |
| [RG03-026](./RG03-026/case.md) | pgvector 백엔드 미연결 | P1 | 개선제안 | FAIL | DEF-RG03-026 |
| [RG03-027](./RG03-027/case.md) | 콘텐츠 타입 비정상 | P1 | 개선제안 | FAIL | DEF-RG03-027 |
