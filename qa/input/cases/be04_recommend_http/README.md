# BE04_추천HTTP

- 세부 기능: 옵션·추천 HTTP
- 케이스: 18
- 코드: `back/src/main/java/com/dasigolmok/recommend/controller/RecommendController.java`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [BE04-001](./BE04-001/case.md) | 옵션 GET | P1 | 구현기반 | PASS | — |
| [BE04-002](./BE04-002/case.md) | 추천 POST | P1 | 구현기반 | PASS | — |
| [BE04-003](./BE04-003/case.md) | 추천 district 누락 | P0 | 구현기반 | PASS | — |
| [BE04-004](./BE04-004/case.md) | 추천 district 공백 | P1 | 구현기반 | PASS | — |
| [BE04-005](./BE04-005/case.md) | 추천 dong 누락 | P0 | 구현기반 | PASS | — |
| [BE04-006](./BE04-006/case.md) | 추천 dong 공백 | P1 | 구현기반 | PASS | — |
| [BE04-007](./BE04-007/case.md) | 추천 JSON 오류 | P0 | 구현기반 | PASS | — |
| [BE04-008](./BE04-008/case.md) | 추천 잘못된 지역 | P0 | 구현기반 | PASS | — |
| [BE04-009](./BE04-009/case.md) | GET /api/options 후 응답 null | P1 | 구현기반 | PASS | — |
| [BE04-010](./BE04-010/case.md) | 옵션 응답 형태 | P1 | 구현기반 | PASS | — |
| [BE04-011](./BE04-011/case.md) | 추천 응답 전체 업종 | P1 | 구현기반 | PASS | — |
| [BE04-012](./BE04-012/case.md) | 추천 top5 | P1 | 구현기반 | PASS | — |
| [BE04-013](./BE04-013/case.md) | 추천 실패 DB 비저장 | P1 | 구현기반 | PASS | — |
| [BE04-014](./BE04-014/case.md) | POST 동시 요청 | P1 | 구현기반 | PASS | — |
| [BE04-015](./BE04-015/case.md) | 옵션 GET 오류 | P0 | 구현기반 | PASS | — |
| [BE04-016](./BE04-016/case.md) | API 메서드 방어 | P1 | 구현기반 | FAIL | DEF-BE04-016 |
| [BE04-017](./BE04-017/case.md) | 불필요한 필드 | P1 | 구현기반 | PASS | — |
| [BE04-018](./BE04-018/case.md) | 지역·동 일치 | P1 | 개선제안 | FAIL | DEF-BE04-018 |
