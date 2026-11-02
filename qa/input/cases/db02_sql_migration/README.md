# DB02_SQL마이그레이션

- 세부 기능: SQL 스키마 버전·무결성
- 케이스: 24
- 코드: `db/migration/V1__init_schema.sql`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [DB02-001](./DB02-001/case.md) | V1 사용자 테이블 | P1 | 구현기반 | PASS | — |
| [DB02-002](./DB02-002/case.md) | V1 장소 테이블 | P1 | 구현기반 | PASS | — |
| [DB02-003](./DB02-003/case.md) | V1 지역 테이블 | P1 | 구현기반 | PASS | — |
| [DB02-004](./DB02-004/case.md) | V1 스토리 테이블 | P1 | 구현기반 | PASS | — |
| [DB02-005](./DB02-005/case.md) | V1 외래키 관계 | P1 | 구현기반 | PASS | — |
| [DB02-006](./DB02-006/case.md) | V1 유니크 이메일 | P1 | 구현기반 | PASS | — |
| [DB02-007](./DB02-007/case.md) | V1 인덱스 | P1 | 구현기반 | FAIL | DEF-DB02-007 |
| [DB02-008](./DB02-008/case.md) | V6 이벤트 | P1 | 구현기반 | PASS | — |
| [DB02-009](./DB02-009/case.md) | V6 팩트 테이블 | P1 | 구현기반 | PASS | — |
| [DB02-010](./DB02-010/case.md) | V6 KPI 스냅샷 | P1 | 구현기반 | PASS | — |
| [DB02-011](./DB02-011/case.md) | V8 낙관잠금 | P1 | 구현기반 | PASS | — |
| [DB02-012](./DB02-012/case.md) | V1~V9 순서 | P1 | 구현기반 | PASS | — |
| [DB02-013](./DB02-013/case.md) | 기존 DB 재실행 | P1 | 구현기반 | PASS | — |
| [DB02-014](./DB02-014/case.md) | 마이그레이션 별도 앱 | P1 | 개선제안 | FAIL | DEF-DB02-014 |
| [DB02-015](./DB02-015/case.md) | 레거시 스키마와 현재 JPA | P0 | 개선제안 | FAIL | DEF-DB02-015 |
| [DB02-016](./DB02-016/case.md) | V4 시드 개발 데이터 | P1 | 개선제안 | FAIL | DEF-DB02-016 |
| [DB02-017](./DB02-017/case.md) | V6 MV 존재 | P1 | 개선제안 | FAIL | DEF-DB02-017 |
| [DB02-018](./DB02-018/case.md) | V9 extension | P1 | 구현기반 | PASS | — |
| [DB02-019](./DB02-019/case.md) | V9 인덱스 | P1 | 구현기반 | PASS | — |
| [DB02-020](./DB02-020/case.md) | V9 정책 테이블 | P1 | 구현기반 | PASS | — |
| [DB02-021](./DB02-021/case.md) | V9 의존 플래그 | P1 | 구현기반 | PASS | — |
| [DB02-022](./DB02-022/case.md) | V9 트랜잭션 롤백 | P1 | 개선제안 | FAIL | DEF-DB02-022 |
| [DB02-023](./DB02-023/case.md) | 정적 SQL 실패 리포트 | P1 | 구현기반 | PASS | — |
| [DB02-024](./DB02-024/case.md) | 마이그레이션 히스토리 | P1 | 개선제안 | FAIL | DEF-DB02-024 |
