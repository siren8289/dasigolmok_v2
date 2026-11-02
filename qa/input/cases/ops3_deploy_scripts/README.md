# OPS3_배포스크립트

- 세부 기능: CD SSH·Compose 자동배포
- 케이스: 27
- 코드: `.github/workflows/deploy.yml`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [OPS3-001](./OPS3-001/case.md) | main 푸시 | P1 | 구현기반 | PASS | — |
| [OPS3-002](./OPS3-002/case.md) | 수동 배포 | P1 | 구현기반 | PASS | — |
| [OPS3-003](./OPS3-003/case.md) | 누락 SSH 키 | P0 | 구현기반 | PASS | — |
| [OPS3-004](./OPS3-004/case.md) | 누락 EC2_HOST | P0 | 구현기반 | PASS | — |
| [OPS3-005](./OPS3-005/case.md) | SSH 키 권한 | P1 | 구현기반 | PASS | — |
| [OPS3-006](./OPS3-006/case.md) | SSH 디렉터리 권한 | P1 | 구현기반 | PASS | — |
| [OPS3-007](./OPS3-007/case.md) | SSH key parse | P1 | 구현기반 | PASS | — |
| [OPS3-008](./OPS3-008/case.md) | SSH host fingerprint | P1 | 구현기반 | PASS | — |
| [OPS3-009](./OPS3-009/case.md) | SSH ConnectTimeout | P1 | 구현기반 | PASS | — |
| [OPS3-010](./OPS3-010/case.md) | 서버 경로 첫 후보 | P1 | 구현기반 | PASS | — |
| [OPS3-011](./OPS3-011/case.md) | 서버 경로 HOME | P1 | 구현기반 | PASS | — |
| [OPS3-012](./OPS3-012/case.md) | 서버 경로 없음 | P1 | 구현기반 | PASS | — |
| [OPS3-013](./OPS3-013/case.md) | git fetch | P1 | 구현기반 | PASS | — |
| [OPS3-014](./OPS3-014/case.md) | git pull ff only | P1 | 구현기반 | PASS | — |
| [OPS3-015](./OPS3-015/case.md) | 환경파일 없음 | P1 | 구현기반 | PASS | — |
| [OPS3-016](./OPS3-016/case.md) | compose config 오류 | P0 | 구현기반 | PASS | — |
| [OPS3-017](./OPS3-017/case.md) | compose up | P1 | 구현기반 | PASS | — |
| [OPS3-018](./OPS3-018/case.md) | 배포 ps | P1 | 구현기반 | PASS | — |
| [OPS3-019](./OPS3-019/case.md) | Front health curl | P1 | 구현기반 | PASS | — |
| [OPS3-020](./OPS3-020/case.md) | AI health 미검증 | P1 | 개선제안 | FAIL | DEF-OPS3-020 |
| [OPS3-021](./OPS3-021/case.md) | BE health 미검증 | P1 | 개선제안 | FAIL | DEF-OPS3-021 |
| [OPS3-022](./OPS3-022/case.md) | rollback 없음 | P1 | 개선제안 | FAIL | DEF-OPS3-022 |
| [OPS3-023](./OPS3-023/case.md) | main push 배포 실패 | P1 | 개선제안 | FAIL | DEF-OPS3-023 |
| [OPS3-024](./OPS3-024/case.md) | 동시 배포 제한 | P1 | 구현기반 | PASS | — |
| [OPS3-025](./OPS3-025/case.md) | SSH 호스트 신뢰 | P1 | 구현기반 | PASS | — |
| [OPS3-026](./OPS3-026/case.md) | 오류 로그 수집 | P1 | 개선제안 | FAIL | DEF-OPS3-026 |
| [OPS3-027](./OPS3-027/case.md) | 앱 헬스 실사용 | P1 | 개선제안 | FAIL | DEF-OPS3-027 |
