# AI09_LLM기본설명

- 세부 기능: Gemini 및 fallback 설명
- 케이스: 22
- 코드: `ai/src/llm_explain.py`

| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |
| --- | --- | --- | --- | --- | --- |
| [AI09-001](./AI09-001/case.md) | 안정 문구 | P1 | 구현기반 | PASS | — |
| [AI09-002](./AI09-002/case.md) | 주의 문구 | P1 | 구현기반 | PASS | — |
| [AI09-003](./AI09-003/case.md) | 위험 문구 | P1 | 구현기반 | PASS | — |
| [AI09-004](./AI09-004/case.md) | 판단 불가 문구 | P1 | 구현기반 | PASS | — |
| [AI09-005](./AI09-005/case.md) | 동 이름 보존 | P1 | 구현기반 | PASS | — |
| [AI09-006](./AI09-006/case.md) | 업종 보존 | P1 | 구현기반 | PASS | — |
| [AI09-007](./AI09-007/case.md) | 최근 폐업률 | P1 | 구현기반 | PASS | — |
| [AI09-008](./AI09-008/case.md) | ML 예상 폐업률 | P1 | 구현기반 | PASS | — |
| [AI09-009](./AI09-009/case.md) | DL 예상 매출 | P1 | 구현기반 | PASS | — |
| [AI09-010](./AI09-010/case.md) | 추정값 고지 | P1 | 구현기반 | PASS | — |
| [AI09-011](./AI09-011/case.md) | 키 없음 fallback | P1 | 구현기반 | PASS | — |
| [AI09-012](./AI09-012/case.md) | Gemini 정상 | P1 | 구현기반 | PASS | — |
| [AI09-013](./AI09-013/case.md) | Gemini API 오류 | P0 | 구현기반 | PASS | — |
| [AI09-014](./AI09-014/case.md) | Gemini 타임아웃 | P1 | 구현기반 | PASS | — |
| [AI09-015](./AI09-015/case.md) | Gemini 빈 텍스트 | P1 | 구현기반 | PASS | — |
| [AI09-016](./AI09-016/case.md) | Gemini 설명 검증 | P1 | 개선제안 | FAIL | DEF-AI09-016 |
| [AI09-017](./AI09-017/case.md) | 프롬프트 숫자 정확성 | P1 | 구현기반 | PASS | — |
| [AI09-018](./AI09-018/case.md) | 프롬프트 상권변화 | P1 | 구현기반 | PASS | — |
| [AI09-019](./AI09-019/case.md) | 프롬프트 3문장 | P1 | 구현기반 | PASS | — |
| [AI09-020](./AI09-020/case.md) | 프롬프트 주입 | P0 | 개선제안 | FAIL | DEF-AI09-020 |
| [AI09-021](./AI09-021/case.md) | API Key 로그 유출 | P1 | 개선제안 | PASS | — |
| [AI09-022](./AI09-022/case.md) | source 값 계약 | P1 | 구현기반 | PASS | — |
