# BE06_전역예외

- 세부 기능: Spring 에러 표준화·로그
- 케이스: 14
- 코드: `back/src/main/java/com/dasigolmok/global/exception/GlobalExceptionHandler.java`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [BE06-001](./BE06-001/case.md) | ApiException 404 | P1 | 구현기반 | PASS | — |
| [BE06-002](./BE06-002/case.md) | ApiException 502 | P1 | 구현기반 | PASS | — |
| [BE06-003](./BE06-003/case.md) | Bean Validation | P1 | 구현기반 | PASS | — |
| [BE06-004](./BE06-004/case.md) | JSON 문법 오류 | P0 | 구현기반 | PASS | — |
| [BE06-005](./BE06-005/case.md) | 알 수 없는 예외 | P1 | 구현기반 | PASS | — |
| [BE06-006](./BE06-006/case.md) | 서버 오류 로깅 | P0 | 구현기반 | PASS | — |
| [BE06-007](./BE06-007/case.md) | 사용자 오류 로그 수준 | P0 | 구현기반 | PASS | — |
| [BE06-008](./BE06-008/case.md) | 예외 스택 마스킹 | P1 | 구현기반 | PASS | — |
| [BE06-009](./BE06-009/case.md) | 동시 실패 10건 | P0 | 구현기반 | PASS | — |
| [BE06-010](./BE06-010/case.md) | 다중 필드 검증 | P1 | 구현기반 | PASS | — |
| [BE06-011](./BE06-011/case.md) | NULL 오류 메시지 | P1 | 개선제안 | FAIL | DEF-BE06-011 |
| [BE06-012](./BE06-012/case.md) | CORS 실패 | P1 | 구현기반 | PASS | — |
| [BE06-013](./BE06-013/case.md) | HTTP 405 | P1 | 구현기반 | FAIL | DEF-BE06-013 |
| [BE06-014](./BE06-014/case.md) | 타입 변환 오류 | P1 | 개선제안 | FAIL | DEF-BE06-014 |
