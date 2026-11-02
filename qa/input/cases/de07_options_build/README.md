# DE07_옵션생성

- 세부 기능: 선택 목록 옵션 생성
- 케이스: 16
- 코드: `data/etl/transform.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [DE07-001](./DE07-001/case.md) | 자치구 알파벳순 | P1 | 구현기반 | PASS | — |
| [DE07-002](./DE07-002/case.md) | 동 지역순 | P1 | 구현기반 | PASS | — |
| [DE07-003](./DE07-003/case.md) | 동 중복 제거 | P0 | 구현기반 | PASS | — |
| [DE07-004](./DE07-004/case.md) | 업종 정렬 | P1 | 구현기반 | PASS | — |
| [DE07-005](./DE07-005/case.md) | 업종 중복 제거 | P0 | 구현기반 | PASS | — |
| [DE07-006](./DE07-006/case.md) | 업종 코드 다름 | P1 | 구현기반 | PASS | — |
| [DE07-007](./DE07-007/case.md) | 지역 옵션 메타 | P1 | 구현기반 | PASS | — |
| [DE07-008](./DE07-008/case.md) | SEMAS 자치구 카운트 | P1 | 구현기반 | PASS | — |
| [DE07-009](./DE07-009/case.md) | SEMAS 업종 카운트 | P1 | 구현기반 | PASS | — |
| [DE07-010](./DE07-010/case.md) | SEMAS 누락 | P0 | 구현기반 | PASS | — |
| [DE07-011](./DE07-011/case.md) | 빈 데이터 train | P1 | 구현기반 | PASS | — |
| [DE07-012](./DE07-012/case.md) | train district null | P1 | 구현기반 | PASS | — |
| [DE07-013](./DE07-013/case.md) | 동 코드 앞자리 | P1 | 구현기반 | PASS | — |
| [DE07-014](./DE07-014/case.md) | 업종명 공백 | P1 | 개선제안 | FAIL | DEF-DE07-014 |
| [DE07-015](./DE07-015/case.md) | 옵션과 통계 일치 | P1 | 구현기반 | PASS | — |
| [DE07-016](./DE07-016/case.md) | 구 바꾸면 다른 구 동 | P1 | 구현기반 | PASS | — |
