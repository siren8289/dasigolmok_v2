# OPS1_Docker연결

- 세부 기능: Docker Compose 4서비스
- 케이스: 26
- 코드: `compose.yaml`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [OPS1-001](./OPS1-001/case.md) | compose config | P1 | 구현기반 | PASS | — |
| [OPS1-002](./OPS1-002/case.md) | DB_PASSWORD 미설정 | P1 | 구현기반 | PASS | — |
| [OPS1-003](./OPS1-003/case.md) | 서비스 4개 | P1 | 구현기반 | PASS | — |
| [OPS1-004](./OPS1-004/case.md) | Postgres 16 pgvector | P1 | 구현기반 | PASS | — |
| [OPS1-005](./OPS1-005/case.md) | DB named volume | P1 | 구현기반 | PASS | — |
| [OPS1-006](./OPS1-006/case.md) | DB 자격 | P1 | 구현기반 | PASS | — |
| [OPS1-007](./OPS1-007/case.md) | DB 헬스 | P1 | 구현기반 | PASS | — |
| [OPS1-008](./OPS1-008/case.md) | DB 다운 | P1 | 구현기반 | PASS | — |
| [OPS1-009](./OPS1-009/case.md) | AI 서비스명 | P1 | 구현기반 | PASS | — |
| [OPS1-010](./OPS1-010/case.md) | DB 서비스명 | P1 | 구현기반 | PASS | — |
| [OPS1-011](./OPS1-011/case.md) | AI depends_on | P1 | 구현기반 | PASS | — |
| [OPS1-012](./OPS1-012/case.md) | Back depends_on | P1 | 구현기반 | PASS | — |
| [OPS1-013](./OPS1-013/case.md) | AI started≠healthy | P1 | 개선제안 | FAIL | DEF-OPS1-013 |
| [OPS1-014](./OPS1-014/case.md) | Nginx proxy | P1 | 구현기반 | PASS | — |
| [OPS1-015](./OPS1-015/case.md) | Host 80 노출 | P1 | 구현기반 | PASS | — |
| [OPS1-016](./OPS1-016/case.md) | AI 호스트 비공개 | P1 | 구현기반 | PASS | — |
| [OPS1-017](./OPS1-017/case.md) | Back 호스트 비공개 | P1 | 구현기반 | PASS | — |
| [OPS1-018](./OPS1-018/case.md) | DB 호스트 비공개 | P1 | 구현기반 | PASS | — |
| [OPS1-019](./OPS1-019/case.md) | V1~V9 initdb | P1 | 구현기반 | PASS | — |
| [OPS1-020](./OPS1-020/case.md) | 상태 Up 의미 | P1 | 구현기반 | RISK | — |
| [OPS1-021](./OPS1-021/case.md) | ENV 문자열 | P1 | 구현기반 | PASS | — |
| [OPS1-022](./OPS1-022/case.md) | 로그 확인 | P1 | 구현기반 | PASS | — |
| [OPS1-023](./OPS1-023/case.md) | front nginx upstream | P1 | 구현기반 | PASS | — |
| [OPS1-024](./OPS1-024/case.md) | 컨테이너 메모리 | P1 | 개선제안 | FAIL | DEF-OPS1-024 |
| [OPS1-025](./OPS1-025/case.md) | 리빌드 후 데이터 | P1 | 구현기반 | PASS | — |
| [OPS1-026](./OPS1-026/case.md) | 동시 배포 | P1 | 개선제안 | FAIL | DEF-OPS1-026 |
