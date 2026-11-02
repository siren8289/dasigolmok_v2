# QA01_보안비기능

- 세부 기능: 보안·성능·사용자 품질
- 케이스: 30
- 코드: `front/src/api/api.ts`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [QA01-001](./QA01-001/case.md) | SQL 인젝션 방어 | P1 | 개선제안 | PASS | — |
| [QA01-002](./QA01-002/case.md) | XSS React 렌더링 | P1 | 구현기반 | PASS | — |
| [QA01-003](./QA01-003/case.md) | RAG 프롬프트 주입 | P1 | 구현기반 | PASS | — |
| [QA01-004](./QA01-004/case.md) | 지역 데이터 분리 | P1 | 개선제안 | FAIL | DEF-QA01-004 |
| [QA01-005](./QA01-005/case.md) | 공고 종료 오안내 | P1 | 구현기반 | PASS | — |
| [QA01-006](./QA01-006/case.md) | 실존 공고 검증 | P1 | 개선제안 | FAIL | DEF-QA01-006 |
| [QA01-007](./QA01-007/case.md) | RAG 샘플 표시 | P1 | 개선제안 | FAIL | DEF-QA01-007 |
| [QA01-008](./QA01-008/case.md) | 접근제어 관리자 API | P1 | 개선제안 | FAIL | DEF-QA01-008 |
| [QA01-009](./QA01-009/case.md) | 민감정보 노출 | P1 | 구현기반 | PASS | — |
| [QA01-010](./QA01-010/case.md) | CORS Origin | P1 | 구현기반 | PASS | — |
| [QA01-011](./QA01-011/case.md) | CSRF POST | P1 | 개선제안 | FAIL | DEF-QA01-011 |
| [QA01-012](./QA01-012/case.md) | HTTP 헤더 | P1 | 개선제안 | FAIL | DEF-QA01-012 |
| [QA01-013](./QA01-013/case.md) | 보안 취약성 스캔 | P0 | 개선제안 | FAIL | DEF-QA01-013 |
| [QA01-014](./QA01-014/case.md) | 입력 최대 길이 | P1 | 개선제안 | FAIL | DEF-QA01-014 |
| [QA01-015](./QA01-015/case.md) | API 100동시 | P1 | 개선제안 | RISK | — |
| [QA01-016](./QA01-016/case.md) | ML 초기 로딩 | P1 | 개선제안 | FAIL | DEF-QA01-016 |
| [QA01-017](./QA01-017/case.md) | RAG 벡터 생성 | P1 | 개선제안 | PASS | — |
| [QA01-018](./QA01-018/case.md) | 데이터 최신성 | P1 | 구현기반 | FAIL | DEF-QA01-018 |
| [QA01-019](./QA01-019/case.md) | 모바일 접근성 | P1 | 구현기반 | FAIL | DEF-QA01-019 |
| [QA01-020](./QA01-020/case.md) | 키보드 사용 | P1 | 구현기반 | PASS | — |
| [QA01-021](./QA01-021/case.md) | 스크린리더 레이블 | P1 | 구현기반 | PASS | — |
| [QA01-022](./QA01-022/case.md) | 색상 대체정보 | P1 | 구현기반 | PASS | — |
| [QA01-023](./QA01-023/case.md) | 불확실성 설명 | P1 | 구현기반 | PASS | — |
| [QA01-024](./QA01-024/case.md) | 사용자 데이터 저장 고지 | P1 | 개선제안 | FAIL | DEF-QA01-024 |
| [QA01-025](./QA01-025/case.md) | 장애 후 복구 | P0 | 구현기반 | RISK | — |
| [QA01-026](./QA01-026/case.md) | 모니터링 알림 | P1 | 개선제안 | FAIL | DEF-QA01-026 |
| [QA01-027](./QA01-027/case.md) | 백업·복구 | P1 | 개선제안 | RISK | — |
| [QA01-028](./QA01-028/case.md) | 데이터 수정 추적 | P1 | 개선제안 | FAIL | DEF-QA01-028 |
| [QA01-029](./QA01-029/case.md) | 사용자 요청 end-to-end | P1 | 구현기반 | RISK | — |
| [QA01-030](./QA01-030/case.md) | 개선 지표 검증 | P1 | 개선제안 | FAIL | DEF-QA01-030 |
