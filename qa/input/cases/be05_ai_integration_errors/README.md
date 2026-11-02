# BE05_AI연동예외

- 세부 기능: RestTemplate 연동·오류
- 케이스: 20
- 코드: `back/src/main/java/com/dasigolmok/ai/AiClient.java`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [BE05-001](./BE05-001/case.md) | 옵션 URL | P1 | 구현기반 | PASS | — |
| [BE05-002](./BE05-002/case.md) | 진단 URL | P1 | 구현기반 | PASS | — |
| [BE05-003](./BE05-003/case.md) | 추천 URL | P1 | 구현기반 | PASS | — |
| [BE05-004](./BE05-004/case.md) | AI 옵션 정상 | P1 | 구현기반 | PASS | — |
| [BE05-005](./BE05-005/case.md) | AI 진단 정상 | P1 | 구현기반 | PASS | — |
| [BE05-006](./BE05-006/case.md) | AI 추천 정상 | P1 | 구현기반 | PASS | — |
| [BE05-007](./BE05-007/case.md) | AI null 응답 | P1 | 구현기반 | PASS | — |
| [BE05-008](./BE05-008/case.md) | 연결거부 | P1 | 구현기반 | PASS | — |
| [BE05-009](./BE05-009/case.md) | DNS 실패 | P1 | 구현기반 | PASS | — |
| [BE05-010](./BE05-010/case.md) | AI Timeout | P1 | 구현기반 | PASS | — |
| [BE05-011](./BE05-011/case.md) | AI 404 | P1 | 개선제안 | FAIL | DEF-BE05-011 |
| [BE05-012](./BE05-012/case.md) | AI 422 | P1 | 개선제안 | FAIL | DEF-BE05-012 |
| [BE05-013](./BE05-013/case.md) | AI 500 | P1 | 구현기반 | PASS | — |
| [BE05-014](./BE05-014/case.md) | AI 빈 JSON | P1 | 개선제안 | FAIL | DEF-BE05-014 |
| [BE05-015](./BE05-015/case.md) | AI HTML 응답 | P1 | 구현기반 | FAIL | DEF-BE05-015 |
| [BE05-016](./BE05-016/case.md) | 재시도 여부 | P1 | 개선제안 | FAIL | DEF-BE05-016 |
| [BE05-017](./BE05-017/case.md) | 동시 요청 pool | P1 | 개선제안 | PASS | — |
| [BE05-018](./BE05-018/case.md) | AI 잘못된 주소 | P0 | 구현기반 | FAIL | DEF-BE05-018 |
| [BE05-019](./BE05-019/case.md) | 비밀 값 마스킹 | P1 | 개선제안 | FAIL | DEF-BE05-019 |
| [BE05-020](./BE05-020/case.md) | 고의 무한대기 서버 | P1 | 개선제안 | PASS | — |
