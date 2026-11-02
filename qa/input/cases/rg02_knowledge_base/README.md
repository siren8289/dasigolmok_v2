# RG02_지식베이스

- 세부 기능: 상권 문서 청킹·임베딩
- 케이스: 26
- 코드: `ai/src/features/commercial_rag_001/market_knowledge/service.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [RG02-001](./RG02-001/case.md) | 지식 문서 로드 | P1 | 구현기반 | PASS | — |
| [RG02-002](./RG02-002/case.md) | 문서 종류 분류 | P1 | 구현기반 | PASS | — |
| [RG02-003](./RG02-003/case.md) | 행정동 메타데이터 | P1 | 구현기반 | PASS | — |
| [RG02-004](./RG02-004/case.md) | 업종 메타데이터 | P1 | 구현기반 | PASS | — |
| [RG02-005](./RG02-005/case.md) | 분기 메타데이터 | P1 | 구현기반 | PASS | — |
| [RG02-006](./RG02-006/case.md) | 출처 URL | P1 | 구현기반 | PASS | — |
| [RG02-007](./RG02-007/case.md) | 공고 날짜 | P1 | 구현기반 | PASS | — |
| [RG02-008](./RG02-008/case.md) | 짧은 문서 청킹 | P1 | 구현기반 | PASS | — |
| [RG02-009](./RG02-009/case.md) | 경계 딱 맞는 문서 | P0 | 구현기반 | PASS | — |
| [RG02-010](./RG02-010/case.md) | 긴 문서 청킹 | P1 | 구현기반 | PASS | — |
| [RG02-011](./RG02-011/case.md) | 중첩량 보존 | P1 | 구현기반 | PASS | — |
| [RG02-012](./RG02-012/case.md) | 0글자 문서 | P1 | 개선제안 | FAIL | DEF-RG02-012 |
| [RG02-013](./RG02-013/case.md) | chunk_size=overlap | P1 | 개선제안 | FAIL | DEF-RG02-013 |
| [RG02-014](./RG02-014/case.md) | chunk_size 음수 | P1 | 개선제안 | FAIL | DEF-RG02-014 |
| [RG02-015](./RG02-015/case.md) | 청크 출처 보존 | P1 | 구현기반 | PASS | — |
| [RG02-016](./RG02-016/case.md) | 문서 ID 유일 | P1 | 구현기반 | PASS | — |
| [RG02-017](./RG02-017/case.md) | 오프라인 임베딩 | P1 | 구현기반 | PASS | — |
| [RG02-018](./RG02-018/case.md) | 외부 API 임베딩 | P1 | 구현기반 | PASS | — |
| [RG02-019](./RG02-019/case.md) | Gemini 오류 fallback | P0 | 구현기반 | PASS | — |
| [RG02-020](./RG02-020/case.md) | 빈 문자열 임베딩 | P1 | 구현기반 | PASS | — |
| [RG02-021](./RG02-021/case.md) | 벡터 유사도 자기일치 | P1 | 구현기반 | PASS | — |
| [RG02-022](./RG02-022/case.md) | 벡터 유사도 영벡터 | P1 | 구현기반 | PASS | — |
| [RG02-023](./RG02-023/case.md) | 다차원 불일치 | P0 | 개선제안 | FAIL | DEF-RG02-023 |
| [RG02-024](./RG02-024/case.md) | 임베딩 차원 DB 일치 | P1 | 개선제안 | FAIL | DEF-RG02-024 |
| [RG02-025](./RG02-025/case.md) | 실제 공개 자료 여부 | P1 | 개선제안 | FAIL | DEF-RG02-025 |
| [RG02-026](./RG02-026/case.md) | 지식 문서 갱신 | P1 | 개선제안 | FAIL | DEF-RG02-026 |
