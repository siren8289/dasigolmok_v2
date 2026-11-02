# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI03-004 | 상권 진단 오케스트레이션 | 입력 district 오타 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI03-022 | 상권 진단 오케스트레이션 | 모델 결과 빈 배열 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI03-023 | 상권 진단 오케스트레이션 | 모델 비정상 NaN | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI03-024 | 상권 진단 오케스트레이션 | 모델 타임아웃 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## AI03-004 입력 district 오타
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 실제 stat의 district와 입력 불일치 감지
- 실제: 입력 district=강남구 결과 district=마포구 error=None
- 결함ID: DEF-AI03-004
- 코드: ai/src/service.py

## AI03-022 모델 결과 빈 배열
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: IndexError가 아닌 명확한 실패 처리
- 실제: 빈 예측목록 predict_ml=[] → IndexError: list index out of range
- 결함ID: DEF-AI03-022
- 코드: ai/src/service.py

## AI03-023 모델 비정상 NaN
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: NaN이 API JSON에 포함되지 않도록 차단
- 실제: 비정상 매출 dl_sales_per_store=nan json_fail:Out of range float values are not JSON compliant snippet=
- 결함ID: DEF-AI03-023
- 코드: ai/src/service.py

## AI03-024 모델 타임아웃
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 실패/시간제한 안내
- 실제: predict_ml 2초 지연 elapsed=2.01s error=None
- 결함ID: DEF-AI03-024
- 코드: ai/src/service.py
