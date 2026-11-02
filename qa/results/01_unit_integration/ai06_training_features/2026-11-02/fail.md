# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI06-013 | ML·DL 피처 공통 | 음수 점포수 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI06-016 | ML·DL 피처 공통 | 혼합 dtype | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## AI06-013 음수 점포수
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 비정상 입력 사전검증 필요
- 실제: store_count=-1 → 반환 store_count=np.int64(-1)
- 결함ID: DEF-AI06-013
- 코드: ai/src/features.py

## AI06-016 혼합 dtype
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 학습/추론 타입 불일치 방어
- 실제: 문자 점포수 store_count='10' dtype=object value='10'
- 결함ID: DEF-AI06-016
- 코드: ai/src/features.py
