# BE03_진단HTTP

- 세부 기능: Spring 진단 HTTP 계약
- 케이스: 14
- 코드: `back/src/main/java/com/dasigolmok/diagnosis/controller/DiagnosisController.java`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [BE03-001](./BE03-001/case.md) | POST 상태 | P1 | 구현기반 | PASS | — |
| [BE03-002](./BE03-002/case.md) | POST 응답 id | P1 | 구현기반 | PASS | — |
| [BE03-003](./BE03-003/case.md) | GET 단건 | P1 | 구현기반 | PASS | — |
| [BE03-004](./BE03-004/case.md) | GET 최근 | P1 | 구현기반 | PASS | — |
| [BE03-005](./BE03-005/case.md) | 단건 잘못된 ID | P0 | 구현기반 | FAIL | DEF-BE03-005 |
| [BE03-006](./BE03-006/case.md) | 단건 0 | P1 | 구현기반 | PASS | — |
| [BE03-007](./BE03-007/case.md) | 단건 음수 | P1 | 구현기반 | PASS | — |
| [BE03-008](./BE03-008/case.md) | 단건 id 너무 큼 | P1 | 구현기반 | FAIL | DEF-BE03-008 |
| [BE03-009](./BE03-009/case.md) | Content-Type | P1 | 구현기반 | PASS | — |
| [BE03-010](./BE03-010/case.md) | 메서드 허용 | P1 | 구현기반 | FAIL | DEF-BE03-010 |
| [BE03-011](./BE03-011/case.md) | 다중 검증 실패 | P1 | 구현기반 | PASS | — |
| [BE03-012](./BE03-012/case.md) | 404 코드 | P1 | 구현기반 | PASS | — |
| [BE03-013](./BE03-013/case.md) | API 응답 한글 | P1 | 구현기반 | PASS | — |
| [BE03-014](./BE03-014/case.md) | 조회 ID 타인 데이터 | P1 | 개선제안 | FAIL | DEF-BE03-014 |
