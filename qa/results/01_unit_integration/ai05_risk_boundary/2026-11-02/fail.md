# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI05-017 | classify 규칙·경계 | 음수 폐업률 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI05-018 | classify 규칙·경계 | 폐업률 120% | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI05-020 | classify 규칙·경계 | NaN 폐업률 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## AI05-017 음수 폐업률
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 범위 오류가 별도로 검증돼야 함
- 실제: classify(-1,'HH')=('stable', False) (기대: 범위 오류)
- 결함ID: DEF-AI05-017
- 코드: ai/src/risk.py

## AI05-018 폐업률 120%
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 100% 초과 데이터 오류 감지 필요
- 실제: classify(120,'HH')=('danger', True) (기대: 100% 초과 오류)
- 결함ID: DEF-AI05-018
- 코드: ai/src/risk.py

## AI05-020 NaN 폐업률
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: unknown 등 안전한 상태로 처리
- 실제: 결측 폐업률 classify(nan,'HH')=('stable', False)
- 결함ID: DEF-AI05-020
- 코드: ai/src/risk.py
