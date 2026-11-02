# DE05_결측치이상치

- 세부 기능: 중앙값 결측·이상치 1%
- 케이스: 19
- 코드: `data/etl/transform.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [DE05-001](./DE05-001/case.md) | 소수 쉼표 | P1 | 구현기반 | PASS | — |
| [DE05-002](./DE05-002/case.md) | 빈 문자열 숫자 | P1 | 구현기반 | PASS | — |
| [DE05-003](./DE05-003/case.md) | 잘못된 문자열 숫자 | P0 | 구현기반 | PASS | — |
| [DE05-004](./DE05-004/case.md) | 전체 중앙값 대체 | P1 | 구현기반 | PASS | — |
| [DE05-005](./DE05-005/case.md) | 업종 중앙값 대체 | P1 | 구현기반 | PASS | — |
| [DE05-006](./DE05-006/case.md) | 업종 외 값 유지 | P1 | 구현기반 | PASS | — |
| [DE05-007](./DE05-007/case.md) | 모든 값 NaN | P1 | 개선제안 | FAIL | DEF-DE05-007 |
| [DE05-008](./DE05-008/case.md) | 업종 하나만 | P1 | 구현기반 | PASS | — |
| [DE05-009](./DE05-009/case.md) | 업종 100행 | P1 | 구현기반 | PASS | — |
| [DE05-010](./DE05-010/case.md) | 상위 극단값 | P1 | 구현기반 | PASS | — |
| [DE05-011](./DE05-011/case.md) | 하위 극단값 | P1 | 구현기반 | PASS | — |
| [DE05-012](./DE05-012/case.md) | 중앙값 일관성 | P1 | 구현기반 | PASS | — |
| [DE05-013](./DE05-013/case.md) | 중앙값 dtype | P1 | 개선제안 | FAIL | DEF-DE05-013 |
| [DE05-014](./DE05-014/case.md) | 업종별 독립 제거 | P1 | 구현기반 | PASS | — |
| [DE05-015](./DE05-015/case.md) | 결측 열 이름 오타 | P1 | 구현기반 | PASS | — |
| [DE05-016](./DE05-016/case.md) | 그룹 key NaN | P1 | 개선제안 | FAIL | DEF-DE05-016 |
| [DE05-017](./DE05-017/case.md) | outlier 결과 빈 그룹 | P1 | 개선제안 | FAIL | DEF-DE05-017 |
| [DE05-018](./DE05-018/case.md) | 상하위 같은 값 | P1 | 구현기반 | PASS | — |
| [DE05-019](./DE05-019/case.md) | NaN quantile | P1 | 구현기반 | PASS | — |
