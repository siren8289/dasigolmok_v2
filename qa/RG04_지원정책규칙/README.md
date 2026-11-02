# RG04_지원정책규칙

- 세부 기능: 지원정책 기간·적합성
- 케이스: 32
- 코드: `ai/src/features/commercial_rag_001/support_policy/service.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [RG04-001](./RG04-001/case.md) | 모집 시작 전 | P1 | 구현기반 | PASS | — |
| [RG04-002](./RG04-002/case.md) | 모집 시작 당일 | P1 | 구현기반 | PASS | — |
| [RG04-003](./RG04-003/case.md) | 모집 중간 | P1 | 구현기반 | PASS | — |
| [RG04-004](./RG04-004/case.md) | 마감 당일 | P1 | 구현기반 | PASS | — |
| [RG04-005](./RG04-005/case.md) | 마감 다음날 | P1 | 구현기반 | PASS | — |
| [RG04-006](./RG04-006/case.md) | 과거 종료 지원 | P1 | 구현기반 | PASS | — |
| [RG04-007](./RG04-007/case.md) | 마감일 형식 오류 | P0 | 구현기반 | PASS | — |
| [RG04-008](./RG04-008/case.md) | 시작일 형식 오류 | P0 | 구현기반 | PASS | — |
| [RG04-009](./RG04-009/case.md) | 기준 날짜 잘못된 형식 | P0 | 개선제안 | FAIL | DEF-RG04-009 |
| [RG04-010](./RG04-010/case.md) | 기준 날짜 없는 경우 | P1 | 구현기반 | PASS | — |
| [RG04-011](./RG04-011/case.md) | 종료 정책 only_open | P1 | 구현기반 | PASS | — |
| [RG04-012](./RG04-012/case.md) | 종료 정책 포함 | P1 | 구현기반 | PASS | — |
| [RG04-013](./RG04-013/case.md) | 예정 정책 only_open | P1 | 구현기반 | PASS | — |
| [RG04-014](./RG04-014/case.md) | 지역 전역 정책 | P1 | 구현기반 | PASS | — |
| [RG04-015](./RG04-015/case.md) | 지역 지정 정책 | P1 | 구현기반 | PASS | — |
| [RG04-016](./RG04-016/case.md) | 타구 정책 배제 | P1 | 구현기반 | PASS | — |
| [RG04-017](./RG04-017/case.md) | 업종 전역 정책 | P1 | 구현기반 | PASS | — |
| [RG04-018](./RG04-018/case.md) | 음식점 대상 정책 | P1 | 구현기반 | PASS | — |
| [RG04-019](./RG04-019/case.md) | 비대상 업종 정책 | P1 | 구현기반 | PASS | — |
| [RG04-020](./RG04-020/case.md) | 맞춤 구 점수 | P1 | 구현기반 | PASS | — |
| [RG04-021](./RG04-021/case.md) | 맞춤 업종 점수 | P1 | 구현기반 | PASS | — |
| [RG04-022](./RG04-022/case.md) | 키워드 일치 점수 | P1 | 구현기반 | PASS | — |
| [RG04-023](./RG04-023/case.md) | 정렬 기준 | P1 | 구현기반 | PASS | — |
| [RG04-024](./RG04-024/case.md) | top_k=1 | P1 | 구현기반 | PASS | — |
| [RG04-025](./RG04-025/case.md) | top_k=5 | P1 | 구현기반 | PASS | — |
| [RG04-026](./RG04-026/case.md) | top_k=-1 | P1 | 개선제안 | FAIL | DEF-RG04-026 |
| [RG04-027](./RG04-027/case.md) | top_k=0 | P1 | 개선제안 | PASS | — |
| [RG04-028](./RG04-028/case.md) | 정책 원천 진위 | P1 | 개선제안 | FAIL | DEF-RG04-028 |
| [RG04-029](./RG04-029/case.md) | 소진 조기마감 | P1 | 개선제안 | FAIL | DEF-RG04-029 |
| [RG04-030](./RG04-030/case.md) | 날짜 범위 역전 | P1 | 개선제안 | FAIL | DEF-RG04-030 |
| [RG04-031](./RG04-031/case.md) | 정책 중복 제목 | P1 | 개선제안 | FAIL | DEF-RG04-031 |
| [RG04-032](./RG04-032/case.md) | today timezone | P1 | 개선제안 | FAIL | DEF-RG04-032 |
