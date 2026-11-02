# AI08_매출DL추론

- 세부 기능: PyTorch MLP 매출 예측
- 케이스: 20
- 코드: `ai/src/dl_model.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [AI08-001](./AI08-001/case.md) | 전처리기 로드 | P1 | 구현기반 | PASS | — |
| [AI08-002](./AI08-002/case.md) | 가중치 로드 | P1 | 구현기반 | PASS | — |
| [AI08-003](./AI08-003/case.md) | model.eval | P1 | 구현기반 | PASS | — |
| [AI08-004](./AI08-004/case.md) | 모델 캐시 | P1 | 구현기반 | PASS | — |
| [AI08-005](./AI08-005/case.md) | 1행 매출 | P1 | 구현기반 | PASS | — |
| [AI08-006](./AI08-006/case.md) | 5행 매출 | P1 | 구현기반 | PASS | — |
| [AI08-007](./AI08-007/case.md) | 로그 역변환 | P1 | 구현기반 | PASS | — |
| [AI08-008](./AI08-008/case.md) | 음수 예측 방어 | P1 | 구현기반 | PASS | — |
| [AI08-009](./AI08-009/case.md) | 0 예측 | P1 | 구현기반 | PASS | — |
| [AI08-010](./AI08-010/case.md) | 소수 한 자리 | P1 | 구현기반 | PASS | — |
| [AI08-011](./AI08-011/case.md) | 입력 dtype | P1 | 구현기반 | PASS | — |
| [AI08-012](./AI08-012/case.md) | 배치 100행 | P1 | 구현기반 | PASS | — |
| [AI08-013](./AI08-013/case.md) | 모델 파일 누락 | P0 | 구현기반 | PASS | — |
| [AI08-014](./AI08-014/case.md) | 전처리기 누락 | P0 | 구현기반 | PASS | — |
| [AI08-015](./AI08-015/case.md) | state dict 불일치 | P0 | 구현기반 | PASS | — |
| [AI08-016](./AI08-016/case.md) | NaN 출력 | P1 | 개선제안 | FAIL | DEF-AI08-016 |
| [AI08-017](./AI08-017/case.md) | 무한대 출력 | P1 | 개선제안 | FAIL | DEF-AI08-017 |
| [AI08-018](./AI08-018/case.md) | 예측 재현성 | P1 | 구현기반 | PASS | — |
| [AI08-019](./AI08-019/case.md) | 메모리 누수 | P1 | 구현기반 | PASS | — |
| [AI08-020](./AI08-020/case.md) | 컨테이너 CPU 환경 | P1 | 구현기반 | PASS | — |
