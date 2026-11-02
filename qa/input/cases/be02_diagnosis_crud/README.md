# BE02_진단CRUD

- 세부 기능: 진단 서비스·저장
- 케이스: 30
- 코드: `back/src/main/java/com/dasigolmok/diagnosis/service/DiagnosisService.java`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [BE02-001](./BE02-001/case.md) | AI 요청 필드 매핑 | P1 | 구현기반 | PASS | — |
| [BE02-002](./BE02-002/case.md) | AI 응답 우선 지역 | P1 | 구현기반 | PASS | — |
| [BE02-003](./BE02-003/case.md) | AI 지역 누락 fallback | P0 | 구현기반 | PASS | — |
| [BE02-004](./BE02-004/case.md) | AI 동 누락 fallback | P0 | 구현기반 | PASS | — |
| [BE02-005](./BE02-005/case.md) | AI 업종 누락 fallback | P0 | 구현기반 | PASS | — |
| [BE02-006](./BE02-006/case.md) | 분기 필드 저장 | P1 | 구현기반 | PASS | — |
| [BE02-007](./BE02-007/case.md) | 점포 수 숫자 저장 | P1 | 구현기반 | PASS | — |
| [BE02-008](./BE02-008/case.md) | 개업률 숫자 저장 | P1 | 구현기반 | PASS | — |
| [BE02-009](./BE02-009/case.md) | 폐업률 숫자 저장 | P1 | 구현기반 | PASS | — |
| [BE02-010](./BE02-010/case.md) | 프랜차이즈 비율 저장 | P1 | 구현기반 | PASS | — |
| [BE02-011](./BE02-011/case.md) | 유동인구 저장 | P1 | 구현기반 | PASS | — |
| [BE02-012](./BE02-012/case.md) | 변화코드 저장 | P1 | 구현기반 | PASS | — |
| [BE02-013](./BE02-013/case.md) | 변화명 저장 | P1 | 구현기반 | PASS | — |
| [BE02-014](./BE02-014/case.md) | 영업기간 저장 | P1 | 구현기반 | PASS | — |
| [BE02-015](./BE02-015/case.md) | 점포당 매출 저장 | P1 | 구현기반 | PASS | — |
| [BE02-016](./BE02-016/case.md) | ML 예측 저장 | P1 | 구현기반 | PASS | — |
| [BE02-017](./BE02-017/case.md) | DL 예측 저장 | P1 | 구현기반 | PASS | — |
| [BE02-018](./BE02-018/case.md) | 상태 저장 | P1 | 구현기반 | PASS | — |
| [BE02-019](./BE02-019/case.md) | 위험불리언 저장 | P1 | 구현기반 | PASS | — |
| [BE02-020](./BE02-020/case.md) | 설명 저장 | P1 | 구현기반 | PASS | — |
| [BE02-021](./BE02-021/case.md) | 설명 출처 저장 | P1 | 구현기반 | PASS | — |
| [BE02-022](./BE02-022/case.md) | 숫자 문자열 혼입 | P1 | 개선제안 | FAIL | DEF-BE02-022 |
| [BE02-023](./BE02-023/case.md) | AI 필수 키 누락 | P0 | 개선제안 | FAIL | DEF-BE02-023 |
| [BE02-024](./BE02-024/case.md) | 설명 2000자 초과 | P1 | 개선제안 | FAIL | DEF-BE02-024 |
| [BE02-025](./BE02-025/case.md) | AI 장애 시 비저장 | P0 | 구현기반 | PASS | — |
| [BE02-026](./BE02-026/case.md) | ID 정상 조회 | P1 | 구현기반 | PASS | — |
| [BE02-027](./BE02-027/case.md) | ID 미등록 조회 | P0 | 구현기반 | PASS | — |
| [BE02-028](./BE02-028/case.md) | 최근 조회 정렬 | P1 | 구현기반 | PASS | — |
| [BE02-029](./BE02-029/case.md) | 동시 생성 | P1 | 구현기반 | PASS | — |
| [BE02-030](./BE02-030/case.md) | 존재하지 않는 지역 | P1 | 구현기반 | PASS | — |
