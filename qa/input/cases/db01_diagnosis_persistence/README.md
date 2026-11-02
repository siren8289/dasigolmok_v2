# DB01_진단영속성

- 세부 기능: JPA 엔터티·Repository
- 케이스: 20
- 코드: `back/src/main/java/com/dasigolmok/diagnosis/entity/Diagnosis.java`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [DB01-001](./DB01-001/case.md) | 기본키 자동생성 | P1 | 구현기반 | PASS | — |
| [DB01-002](./DB01-002/case.md) | 한글 지역 저장 | P1 | 구현기반 | PASS | — |
| [DB01-003](./DB01-003/case.md) | 한글 동 저장 | P1 | 구현기반 | PASS | — |
| [DB01-004](./DB01-004/case.md) | 한글 업종 저장 | P1 | 구현기반 | PASS | — |
| [DB01-005](./DB01-005/case.md) | 분기 저장 | P1 | 구현기반 | PASS | — |
| [DB01-006](./DB01-006/case.md) | 저장/조회 일치 | P1 | 구현기반 | PASS | — |
| [DB01-007](./DB01-007/case.md) | Double null | P1 | 구현기반 | PASS | — |
| [DB01-008](./DB01-008/case.md) | 위험 boolean false | P1 | 구현기반 | PASS | — |
| [DB01-009](./DB01-009/case.md) | 위험 boolean true | P1 | 구현기반 | PASS | — |
| [DB01-010](./DB01-010/case.md) | 설명 길이 2000 | P1 | 구현기반 | PASS | — |
| [DB01-011](./DB01-011/case.md) | 설명 길이 2001 | P1 | 구현기반 | PASS | — |
| [DB01-012](./DB01-012/case.md) | 설명 특수문자 | P1 | 구현기반 | PASS | — |
| [DB01-013](./DB01-013/case.md) | 생성 시각 | P1 | 구현기반 | PASS | — |
| [DB01-014](./DB01-014/case.md) | 최근 10건 조회 | P0 | 구현기반 | PASS | — |
| [DB01-015](./DB01-015/case.md) | 단건 삭제 후 조회 | P1 | 구현기반 | PASS | — |
| [DB01-016](./DB01-016/case.md) | 동시 저장 | P1 | 구현기반 | PASS | — |
| [DB01-017](./DB01-017/case.md) | 재시작 후 데이터 유지 | P1 | 구현기반 | PASS | — |
| [DB01-018](./DB01-018/case.md) | 실수 특수 값 | P1 | 개선제안 | FAIL | DEF-DB01-018 |
| [DB01-019](./DB01-019/case.md) | 트랜잭션 AI 실패 | P1 | 구현기반 | PASS | — |
| [DB01-020](./DB01-020/case.md) | 데이터 접근 경계 | P1 | 개선제안 | FAIL | DEF-DB01-020 |
