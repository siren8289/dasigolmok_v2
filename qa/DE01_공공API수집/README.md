# DE01_공공API수집

- 세부 기능: 소상공인 API·서울시 수집
- 케이스: 26
- 코드: `data/etl/fetch.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [DE01-001](./DE01-001/case.md) | 인증키 없음 | P1 | 구현기반 | PASS | — |
| [DE01-002](./DE01-002/case.md) | SEMAS 정상 resultCode | P1 | 구현기반 | PASS | — |
| [DE01-003](./DE01-003/case.md) | SEMAS 성공 코드 0 | P1 | 구현기반 | PASS | — |
| [DE01-004](./DE01-004/case.md) | SEMAS 성공 코드 000 | P1 | 구현기반 | PASS | — |
| [DE01-005](./DE01-005/case.md) | SEMAS 오류 코드 | P0 | 구현기반 | PASS | — |
| [DE01-006](./DE01-006/case.md) | SEMAS 타임아웃 | P1 | 구현기반 | PASS | — |
| [DE01-007](./DE01-007/case.md) | SEMAS HTTP 500 | P1 | 구현기반 | PASS | — |
| [DE01-008](./DE01-008/case.md) | 대분류와 중분류 | P1 | 구현기반 | PASS | — |
| [DE01-009](./DE01-009/case.md) | 자치구 목록 | P1 | 구현기반 | PASS | — |
| [DE01-010](./DE01-010/case.md) | 업소 샘플 페이지 1 | P1 | 구현기반 | PASS | — |
| [DE01-011](./DE01-011/case.md) | 업소 샘플 페이지 3 | P1 | 구현기반 | PASS | — |
| [DE01-012](./DE01-012/case.md) | 업소 totalCount 미달 | P1 | 구현기반 | PASS | — |
| [DE01-013](./DE01-013/case.md) | 업소 목록 빈 페이지 | P1 | 구현기반 | PASS | — |
| [DE01-014](./DE01-014/case.md) | 업소 전체 건수 충족 | P1 | 구현기반 | PASS | — |
| [DE01-015](./DE01-015/case.md) | 업소 max_pages=0 | P1 | 구현기반 | PASS | — |
| [DE01-016](./DE01-016/case.md) | 외부 API 429 | P1 | 개선제안 | FAIL | DEF-DE01-016 |
| [DE01-017](./DE01-017/case.md) | 비정상 JSON | P1 | 구현기반 | PASS | — |
| [DE01-018](./DE01-018/case.md) | 인증키 로그 | P0 | 개선제안 | FAIL | DEF-DE01-018 |
| [DE01-019](./DE01-019/case.md) | 서울시 ZIP 다운로드 | P1 | 구현기반 | PASS | — |
| [DE01-020](./DE01-020/case.md) | 서울시 Sheet 다운로드 | P1 | 구현기반 | PASS | — |
| [DE01-021](./DE01-021/case.md) | 서울시 ZIP 손상 | P1 | 구현기반 | FAIL | DEF-DE01-021 |
| [DE01-022](./DE01-022/case.md) | 다운로드 timeout | P1 | 구현기반 | PASS | — |
| [DE01-023](./DE01-023/case.md) | 서울시 표 연도 병합 | P1 | 구현기반 | PASS | — |
| [DE01-024](./DE01-024/case.md) | 없는 SEOUL_FILES key | P1 | 구현기반 | PASS | — |
| [DE01-025](./DE01-025/case.md) | 서울 외 데이터 | P1 | 구현기반 | PASS | — |
| [DE01-026](./DE01-026/case.md) | 응답 URL 변경 | P1 | 개선제안 | FAIL | DEF-DE01-026 |
