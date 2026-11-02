# FE05_HTTP클라이언트

- 세부 기능: 프론트 fetch API 계약
- 케이스: 18
- 코드: `front/src/api/api.ts`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [FE05-001](./FE05-001/case.md) | baseURL 기본값 | P1 | 구현기반 | PASS | — |
| [FE05-002](./FE05-002/case.md) | baseURL 상대 경로 | P1 | 구현기반 | PASS | — |
| [FE05-003](./FE05-003/case.md) | 옵션 URL | P1 | 구현기반 | PASS | — |
| [FE05-004](./FE05-004/case.md) | 진단 URL | P1 | 구현기반 | PASS | — |
| [FE05-005](./FE05-005/case.md) | 결과 조회 URL | P1 | 구현기반 | PASS | — |
| [FE05-006](./FE05-006/case.md) | 추천 URL | P1 | 구현기반 | PASS | — |
| [FE05-007](./FE05-007/case.md) | JSON 헤더 | P1 | 구현기반 | PASS | — |
| [FE05-008](./FE05-008/case.md) | 문자열 JSON 직렬화 | P1 | 구현기반 | PASS | — |
| [FE05-009](./FE05-009/case.md) | HTTP 200 JSON | P1 | 구현기반 | PASS | — |
| [FE05-010](./FE05-010/case.md) | HTTP 201 JSON | P1 | 구현기반 | PASS | — |
| [FE05-011](./FE05-011/case.md) | 400 message 우선 | P1 | 구현기반 | PASS | — |
| [FE05-012](./FE05-012/case.md) | 422 detail 대체 | P1 | 구현기반 | PASS | — |
| [FE05-013](./FE05-013/case.md) | 500 비JSON | P1 | 구현기반 | PASS | — |
| [FE05-014](./FE05-014/case.md) | 네트워크 실패 | P1 | 구현기반 | PASS | — |
| [FE05-015](./FE05-015/case.md) | 빈 응답 body | P1 | 개선제안 | FAIL | DEF-FE05-015 |
| [FE05-016](./FE05-016/case.md) | API 경로 이중 슬래시 | P1 | 개선제안 | FAIL | DEF-FE05-016 |
| [FE05-017](./FE05-017/case.md) | 민감정보 에러 반사 | P0 | 개선제안 | FAIL | DEF-FE05-017 |
| [FE05-018](./FE05-018/case.md) | 조회 ID 인코딩 | P1 | 개선제안 | FAIL | DEF-FE05-018 |
