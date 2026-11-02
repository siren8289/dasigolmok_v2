# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI04-021 | 행정동 업종 추천 | ML 예측 건수 불일치 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI04-022 | 행정동 업종 추천 | DL 음수 매출 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI04-023 | 행정동 업종 추천 | 동 이름만 조회 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI04-025 | 행정동 업종 추천 | limit=-1 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## AI04-021 ML 예측 건수 불일치
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: zip 잘림으로 누락되지 않게 오류 검증
- 실제: 3행·ML 2개 → error=None all=2 industries=['업종0', '업종1']
- 결함ID: DEF-AI04-021
- 코드: ai/src/service.py

## AI04-022 DL 음수 매출
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 부적절한 추천 점수 방어
- 실제: 예측 sales=-50 → sales=-50 score=-8.5 error=None
- 결함ID: DEF-AI04-022
- 코드: ai/src/service.py

## AI04-023 동 이름만 조회
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: district 필터 추가 필요
- 실제: 요청 district=강남구 반환 district=관악구 관악구전용업종유입=['모터사이클및부품', '모터사이클수리', '복권방', '자동차미용'] all=149
- 결함ID: DEF-AI04-023
- 코드: ai/src/service.py

## AI04-025 limit=-1
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 의도치 않은 항목 누락 방어
- 실제: limit=-1 → error=None rec=['업종0', '업종1'] all=['업종0', '업종1', '업종2']
- 결함ID: DEF-AI04-025
- 코드: ai/src/service.py
