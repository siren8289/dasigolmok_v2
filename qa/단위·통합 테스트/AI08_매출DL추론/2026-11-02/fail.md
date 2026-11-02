# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI08-016 | PyTorch MLP 매출 예측 | NaN 출력 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI08-017 | PyTorch MLP 매출 예측 | 무한대 출력 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## AI08-016 NaN 출력
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: NaN API 유출 방어
- 실제: 결측 복원 output=NaN → [nan]
- 결함ID: DEF-AI08-016
- 코드: ai/src/dl_model.py

## AI08-017 무한대 출력
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 가격 오버플로 방어
- 실제: 무한값 복원 output=+inf → [inf]
- 결함ID: DEF-AI08-017
- 코드: ai/src/dl_model.py
