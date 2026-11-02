# DB03_pgvector전용

- 세부 기능: RAG 데이터베이스 스키마
- 케이스: 19
- 코드: `db/migration/V9__commercial_rag_pgvector.sql`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [DB03-001](./DB03-001/case.md) | vector 확장 존재 | P1 | 구현기반 | PASS | — |
| [DB03-002](./DB03-002/case.md) | 청크 ID 기본키 | P1 | 구현기반 | PASS | — |
| [DB03-003](./DB03-003/case.md) | title NOT NULL | P1 | 구현기반 | PASS | — |
| [DB03-004](./DB03-004/case.md) | content NOT NULL | P1 | 구현기반 | PASS | — |
| [DB03-005](./DB03-005/case.md) | doc_type NOT NULL | P1 | 구현기반 | PASS | — |
| [DB03-006](./DB03-006/case.md) | source optional | P1 | 구현기반 | PASS | — |
| [DB03-007](./DB03-007/case.md) | region 필터 인덱스 | P1 | 구현기반 | PASS | — |
| [DB03-008](./DB03-008/case.md) | dong 필터 인덱스 | P1 | 구현기반 | PASS | — |
| [DB03-009](./DB03-009/case.md) | industry 필터 인덱스 | P1 | 구현기반 | PASS | — |
| [DB03-010](./DB03-010/case.md) | embedding 64차원 | P1 | 구현기반 | PASS | — |
| [DB03-011](./DB03-011/case.md) | embedding 512차원 | P1 | 구현기반 | PASS | — |
| [DB03-012](./DB03-012/case.md) | HNSW 인덱스 | P1 | 구현기반 | PASS | — |
| [DB03-013](./DB03-013/case.md) | 메타데이터 JSONB | P1 | 구현기반 | PASS | — |
| [DB03-014](./DB03-014/case.md) | 마감 정책 테이블 | P1 | 구현기반 | PASS | — |
| [DB03-015](./DB03-015/case.md) | DB 정책 실시간 소스 | P1 | 개선제안 | FAIL | DEF-DB03-015 |
| [DB03-016](./DB03-016/case.md) | 정책 날짜 CHECK | P1 | 개선제안 | FAIL | DEF-DB03-016 |
| [DB03-017](./DB03-017/case.md) | 정책 source_url 검증 | P1 | 개선제안 | FAIL | DEF-DB03-017 |
| [DB03-018](./DB03-018/case.md) | 외부 연결 차단 | P0 | 구현기반 | PASS | — |
| [DB03-019](./DB03-019/case.md) | 정책 갱신/삭제 | P1 | 개선제안 | FAIL | DEF-DB03-019 |
