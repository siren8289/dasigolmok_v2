# RG05_종합가이드

- 세부 기능: 상권 진단·출처 결합 설명
- 케이스: 26
- 코드: `ai/src/features/commercial_rag_001/commercial_guidance/service.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [RG05-001](./RG05-001/case.md) | 진단 동·업종 있음 | P1 | 구현기반 | PASS | — |
| [RG05-002](./RG05-002/case.md) | 진단 업종 없음 | P1 | 구현기반 | PASS | — |
| [RG05-003](./RG05-003/case.md) | 진단 동 없음 | P1 | 구현기반 | PASS | — |
| [RG05-004](./RG05-004/case.md) | 진단에 오류 | P0 | 구현기반 | PASS | — |
| [RG05-005](./RG05-005/case.md) | 기본 자치구 fallback | P1 | 구현기반 | PASS | — |
| [RG05-006](./RG05-006/case.md) | 상권 stable 설명 | P1 | 구현기반 | PASS | — |
| [RG05-007](./RG05-007/case.md) | 상권 warning 설명 | P1 | 구현기반 | PASS | — |
| [RG05-008](./RG05-008/case.md) | 상권 danger 설명 | P1 | 구현기반 | PASS | — |
| [RG05-009](./RG05-009/case.md) | 상권 수치 인용 | P1 | 구현기반 | PASS | — |
| [RG05-010](./RG05-010/case.md) | 상권 변화명 | P1 | 구현기반 | PASS | — |
| [RG05-011](./RG05-011/case.md) | 보고서 있는 경우 | P1 | 구현기반 | PASS | — |
| [RG05-012](./RG05-012/case.md) | 보고서 없는 경우 | P1 | 구현기반 | FAIL | DEF-RG05-012 |
| [RG05-013](./RG05-013/case.md) | 지원사업 open | P1 | 구현기반 | PASS | — |
| [RG05-014](./RG05-014/case.md) | 지원사업 마감 | P1 | 구현기반 | PASS | — |
| [RG05-015](./RG05-015/case.md) | 지원사업 없음 | P1 | 구현기반 | FAIL | DEF-RG05-015 |
| [RG05-016](./RG05-016/case.md) | 보고서 citation | P1 | 구현기반 | PASS | — |
| [RG05-017](./RG05-017/case.md) | 정책 citation | P1 | 구현기반 | PASS | — |
| [RG05-018](./RG05-018/case.md) | 근거 120자 초과 | P0 | 구현기반 | PASS | — |
| [RG05-019](./RG05-019/case.md) | 키 없음 fallback | P1 | 구현기반 | PASS | — |
| [RG05-020](./RG05-020/case.md) | Gemini 정상 | P1 | 구현기반 | PASS | — |
| [RG05-021](./RG05-021/case.md) | Gemini 에러 fallback | P1 | 구현기반 | PASS | — |
| [RG05-022](./RG05-022/case.md) | 필수 추정치 경고 | P1 | 구현기반 | PASS | — |
| [RG05-023](./RG05-023/case.md) | 현장 실사 문구 | P1 | 구현기반 | PASS | — |
| [RG05-024](./RG05-024/case.md) | Gemini 오안내 | P1 | 개선제안 | FAIL | DEF-RG05-024 |
| [RG05-025](./RG05-025/case.md) | 출처 위조 | P1 | 개선제안 | FAIL | DEF-RG05-025 |
| [RG05-026](./RG05-026/case.md) | 비밀키 유출 시도 | P0 | 개선제안 | FAIL | DEF-RG05-026 |
