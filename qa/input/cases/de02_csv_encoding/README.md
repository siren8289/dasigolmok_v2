# DE02_CSV인코딩

- 세부 기능: ZIP·CSV 인코딩·형식
- 케이스: 18
- 코드: `data/etl/fetch.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [DE02-001](./DE02-001/case.md) | cp949 CSV | P1 | 구현기반 | PASS | — |
| [DE02-002](./DE02-002/case.md) | UTF8 BOM CSV | P1 | 구현기반 | PASS | — |
| [DE02-003](./DE02-003/case.md) | UTF8 일반 CSV | P1 | 구현기반 | PASS | — |
| [DE02-004](./DE02-004/case.md) | 깨진 한글 | P1 | 구현기반 | PASS | — |
| [DE02-005](./DE02-005/case.md) | 빈 CSV | P1 | 구현기반 | PASS | — |
| [DE02-006](./DE02-006/case.md) | CSV 헤더만 | P1 | 구현기반 | PASS | — |
| [DE02-007](./DE02-007/case.md) | ZIP 안 CSV 하나 | P1 | 구현기반 | PASS | — |
| [DE02-008](./DE02-008/case.md) | ZIP 안 CSV 여러개 | P1 | 구현기반 | PASS | — |
| [DE02-009](./DE02-009/case.md) | ZIP 안 CSV 없음 | P1 | 개선제안 | FAIL | DEF-DE02-009 |
| [DE02-010](./DE02-010/case.md) | ZIP 폴더 포함 | P1 | 구현기반 | PASS | — |
| [DE02-011](./DE02-011/case.md) | CSV 악성 수식 | P1 | 개선제안 | FAIL | DEF-DE02-011 |
| [DE02-012](./DE02-012/case.md) | CSV 쉼표 인용 | P1 | 구현기반 | PASS | — |
| [DE02-013](./DE02-013/case.md) | CSV 줄바꿈 인용 | P1 | 구현기반 | PASS | — |
| [DE02-014](./DE02-014/case.md) | 숫자 열 선행 0 | P1 | 개선제안 | FAIL | DEF-DE02-014 |
| [DE02-015](./DE02-015/case.md) | 빈 원본 ZIP | P1 | 구현기반 | FAIL | DEF-DE02-015 |
| [DE02-016](./DE02-016/case.md) | zip 폭탄 | P1 | 개선제안 | FAIL | DEF-DE02-016 |
| [DE02-017](./DE02-017/case.md) | CSV 컬럼명 변동 | P1 | 개선제안 | FAIL | DEF-DE02-017 |
| [DE02-018](./DE02-018/case.md) | 잘못된 파일 mime | P0 | 개선제안 | FAIL | DEF-DE02-018 |
