# BE01_진단요청DTO

- 세부 기능: 진단 DTO 유효성
- 케이스: 24
- 코드: `back/src/main/java/com/dasigolmok/diagnosis/dto/DiagnosisRequest.java`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [BE01-001](./BE01-001/case.md) | 정상 3필드 | P1 | 구현기반 | PASS | — |
| [BE01-002](./BE01-002/case.md) | district 누락 | P0 | 구현기반 | PASS | — |
| [BE01-003](./BE01-003/case.md) | district null | P1 | 구현기반 | PASS | — |
| [BE01-004](./BE01-004/case.md) | district 빈 문자열 | P1 | 구현기반 | PASS | — |
| [BE01-005](./BE01-005/case.md) | district 공백만 | P1 | 구현기반 | PASS | — |
| [BE01-006](./BE01-006/case.md) | dong 누락 | P0 | 구현기반 | PASS | — |
| [BE01-007](./BE01-007/case.md) | dong null | P1 | 구현기반 | PASS | — |
| [BE01-008](./BE01-008/case.md) | dong 빈 문자열 | P1 | 구현기반 | PASS | — |
| [BE01-009](./BE01-009/case.md) | dong 공백만 | P1 | 구현기반 | PASS | — |
| [BE01-010](./BE01-010/case.md) | industry 누락 | P0 | 구현기반 | PASS | — |
| [BE01-011](./BE01-011/case.md) | industry null | P1 | 구현기반 | PASS | — |
| [BE01-012](./BE01-012/case.md) | industry 빈 문자열 | P1 | 구현기반 | PASS | — |
| [BE01-013](./BE01-013/case.md) | industry 공백만 | P1 | 구현기반 | PASS | — |
| [BE01-014](./BE01-014/case.md) | 필드 타입 숫자 | P1 | 구현기반 | PASS | — |
| [BE01-015](./BE01-015/case.md) | 객체 대신 배열 | P1 | 구현기반 | PASS | — |
| [BE01-016](./BE01-016/case.md) | 깨진 JSON | P1 | 구현기반 | PASS | — |
| [BE01-017](./BE01-017/case.md) | JSON Content-Type 누락 | P0 | 구현기반 | FAIL | DEF-BE01-017 |
| [BE01-018](./BE01-018/case.md) | 키 대소문자 오류 | P0 | 구현기반 | PASS | — |
| [BE01-019](./BE01-019/case.md) | 10000자 district | P1 | 개선제안 | FAIL | DEF-BE01-019 |
| [BE01-020](./BE01-020/case.md) | 스크립트 동 이름 | P1 | 개선제안 | FAIL | DEF-BE01-020 |
| [BE01-021](./BE01-021/case.md) | SQL 문장 업종 | P1 | 개선제안 | FAIL | DEF-BE01-021 |
| [BE01-022](./BE01-022/case.md) | 추가 필드 | P1 | 구현기반 | PASS | — |
| [BE01-023](./BE01-023/case.md) | 지역·동 불일치 | P0 | 개선제안 | FAIL | DEF-BE01-023 |
| [BE01-024](./BE01-024/case.md) | 예외 메시지 구성 | P1 | 구현기반 | PASS | — |
