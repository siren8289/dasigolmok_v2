# RG08_RAG정량평가

- 세부 기능: RAG 품질 지표·평가
- 케이스: 22
- 코드: `ai/src/features/commercial_rag_001/harness/runtime.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [RG08-001](./RG08-001/case.md) | Recall 완전 | P1 | 구현기반 | PASS | — |
| [RG08-002](./RG08-002/case.md) | Recall 절반 | P1 | 구현기반 | PASS | — |
| [RG08-003](./RG08-003/case.md) | Recall 0 | P1 | 구현기반 | PASS | — |
| [RG08-004](./RG08-004/case.md) | Recall 기준 없음 | P1 | 구현기반 | PASS | — |
| [RG08-005](./RG08-005/case.md) | 인용 정확 100% | P1 | 구현기반 | PASS | — |
| [RG08-006](./RG08-006/case.md) | 인용 정확 50% | P1 | 구현기반 | PASS | — |
| [RG08-007](./RG08-007/case.md) | 인용 정확 0% | P1 | 구현기반 | PASS | — |
| [RG08-008](./RG08-008/case.md) | 인용 없음 | P1 | 구현기반 | PASS | — |
| [RG08-009](./RG08-009/case.md) | 지역 적합성 완전 | P1 | 구현기반 | PASS | — |
| [RG08-010](./RG08-010/case.md) | 지역 적합성 절반 | P1 | 구현기반 | PASS | — |
| [RG08-011](./RG08-011/case.md) | 타구 근거만 | P1 | 구현기반 | PASS | — |
| [RG08-012](./RG08-012/case.md) | 지역 선택 없음 | P1 | 구현기반 | PASS | — |
| [RG08-013](./RG08-013/case.md) | 종료 정책 오안내 없음 | P1 | 구현기반 | PASS | — |
| [RG08-014](./RG08-014/case.md) | 종료 정책 오안내 1건 | P1 | 구현기반 | PASS | — |
| [RG08-015](./RG08-015/case.md) | 마감 지원 없음 | P1 | 구현기반 | PASS | — |
| [RG08-016](./RG08-016/case.md) | 샘플 평가 | P1 | 구현기반 | PASS | — |
| [RG08-017](./RG08-017/case.md) | 지표 범위 | P1 | 구현기반 | PASS | — |
| [RG08-018](./RG08-018/case.md) | 자료 없음 분모 | P1 | 구현기반 | PASS | — |
| [RG08-019](./RG08-019/case.md) | 재현성 | P1 | 구현기반 | PASS | — |
| [RG08-020](./RG08-020/case.md) | 평가 결과 노출 | P1 | 구현기반 | PASS | — |
| [RG08-021](./RG08-021/case.md) | 평가 품질 기준 | P1 | 개선제안 | FAIL | DEF-RG08-021 |
| [RG08-022](./RG08-022/case.md) | 인용 위조 회귀 | P1 | 구현기반 | PASS | — |
