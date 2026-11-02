# DE08_ETL실행저장

- 세부 기능: 데이터 수집→전처리→아티팩트
- 케이스: 23
- 코드: `data/etl/run.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [DE08-001](./DE08-001/case.md) | 전체 실행 | P1 | 구현기반 | PASS | — |
| [DE08-002](./DE08-002/case.md) | 캐시 실행 | P1 | 구현기반 | PASS | — |
| [DE08-003](./DE08-003/case.md) | 캐시 없을 때 | P1 | 구현기반 | PASS | — |
| [DE08-004](./DE08-004/case.md) | SEMAS API 실패 | P1 | 구현기반 | PASS | — |
| [DE08-005](./DE08-005/case.md) | 서울 점포 API 실패 | P1 | 구현기반 | FAIL | DEF-DE08-005 |
| [DE08-006](./DE08-006/case.md) | 서울 매출 API 실패 | P1 | 구현기반 | PASS | — |
| [DE08-007](./DE08-007/case.md) | 서울 유동인구 실패 | P1 | 구현기반 | PASS | — |
| [DE08-008](./DE08-008/case.md) | 서울 상권변화 실패 | P1 | 구현기반 | PASS | — |
| [DE08-009](./DE08-009/case.md) | 저장 processed/train | P1 | 구현기반 | PASS | — |
| [DE08-010](./DE08-010/case.md) | 저장 processed/dong_stats | P1 | 구현기반 | PASS | — |
| [DE08-011](./DE08-011/case.md) | 저장 processed/options | P1 | 구현기반 | PASS | — |
| [DE08-012](./DE08-012/case.md) | 원본 저장 | P1 | 구현기반 | PASS | — |
| [DE08-013](./DE08-013/case.md) | 불완전 데이터 | P1 | 개선제안 | FAIL | DEF-DE08-013 |
| [DE08-014](./DE08-014/case.md) | 최신 분기 데이터 지연 | P1 | 개선제안 | FAIL | DEF-DE08-014 |
| [DE08-015](./DE08-015/case.md) | JSON 인코딩 | P1 | 구현기반 | PASS | — |
| [DE08-016](./DE08-016/case.md) | 파일 쓰기 실패 | P1 | 구현기반 | PASS | — |
| [DE08-017](./DE08-017/case.md) | 저장 중 크래시 | P1 | 개선제안 | FAIL | DEF-DE08-017 |
| [DE08-018](./DE08-018/case.md) | 기존 모델 데이터 갱신 | P1 | 개선제안 | FAIL | DEF-DE08-018 |
| [DE08-019](./DE08-019/case.md) | ETL 멱등성 | P1 | 구현기반 | PASS | — |
| [DE08-020](./DE08-020/case.md) | ETL 원본 공개 | P1 | 구현기반 | PASS | — |
| [DE08-021](./DE08-021/case.md) | 서버 CI 범위 | P1 | 구현기반 | PASS | — |
| [DE08-022](./DE08-022/case.md) | 상세 로그 | P1 | 구현기반 | FAIL | DEF-DE08-022 |
| [DE08-023](./DE08-023/case.md) | 출처 자료 최신성 | P1 | 개선제안 | FAIL | DEF-DE08-023 |
