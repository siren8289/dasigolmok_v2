# AI01_FastAPI계약

- 세부 기능: FastAPI 엔드포인트·스키마
- 케이스: 16
- 코드: `ai/src/main.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [AI01-001](./AI01-001/case.md) | 옵션 API | P1 | 구현기반 | PASS | — |
| [AI01-002](./AI01-002/case.md) | 진단 API | P1 | 구현기반 | PASS | — |
| [AI01-003](./AI01-003/case.md) | 추천 API | P1 | 구현기반 | PASS | — |
| [AI01-004](./AI01-004/case.md) | 헬스 API | P1 | 구현기반 | PASS | — |
| [AI01-005](./AI01-005/case.md) | RAG ask 연결 | P1 | 구현기반 | PASS | — |
| [AI01-006](./AI01-006/case.md) | RAG health 연결 | P1 | 구현기반 | PASS | — |
| [AI01-007](./AI01-007/case.md) | 진단 존재하지 않는 조합 | P1 | 구현기반 | PASS | — |
| [AI01-008](./AI01-008/case.md) | 추천 존재하지 않는 동 | P1 | 구현기반 | PASS | — |
| [AI01-009](./AI01-009/case.md) | 진단 JSON 누락 | P0 | 개선제안 | PASS | — |
| [AI01-010](./AI01-010/case.md) | 추천 JSON 누락 | P0 | 구현기반 | PASS | — |
| [AI01-011](./AI01-011/case.md) | 진단 숫자 타입 | P1 | 구현기반 | PASS | — |
| [AI01-012](./AI01-012/case.md) | 빈 문자열 | P1 | 개선제안 | FAIL | DEF-AI01-012 |
| [AI01-013](./AI01-013/case.md) | 최대 길이 | P1 | 개선제안 | FAIL | DEF-AI01-013 |
| [AI01-014](./AI01-014/case.md) | 응답 404 본문 | P1 | 구현기반 | PASS | — |
| [AI01-015](./AI01-015/case.md) | OPTIONS 요청 CORS | P1 | 개선제안 | FAIL | DEF-AI01-015 |
| [AI01-016](./AI01-016/case.md) | 프론트 경로 비공개 | P1 | 개선제안 | FAIL | DEF-AI01-016 |
