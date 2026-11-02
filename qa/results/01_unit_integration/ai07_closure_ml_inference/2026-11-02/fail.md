# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI07-007 | RandomForest 폐업률 예측 | joblib 손상 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI07-010 | RandomForest 폐업률 예측 | 예측 음수 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI07-011 | RandomForest 폐업률 예측 | 예측 100 초과 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI07-012 | RandomForest 폐업률 예측 | 모델 NaN | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## AI07-007 joblib 손상
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 오류 포착/장애 로그
- 실제: 손상 joblib 결과=IndexError: pop from empty list 로그=[]
- 결함ID: DEF-AI07-007
- 코드: ai/src/ml_model.py

## AI07-010 예측 음수
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 폐업률 0 미만 금지 후처리 검토
- 실제: 음수 예측 model output=-2 → [-2.0]
- 결함ID: DEF-AI07-010
- 코드: ai/src/ml_model.py

## AI07-011 예측 100 초과
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 폐업률 100 초과 금지 후처리 검토
- 실제: 백 초과 예측 model output=105 → [105.0]
- 결함ID: DEF-AI07-011
- 코드: ai/src/ml_model.py

## AI07-012 모델 NaN
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 응답 직전 NaN 방어
- 실제: 결측 예측 output=NaN → [nan]
- 결함ID: DEF-AI07-012
- 코드: ai/src/ml_model.py
