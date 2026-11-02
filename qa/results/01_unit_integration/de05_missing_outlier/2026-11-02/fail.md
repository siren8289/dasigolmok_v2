# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE05-007 | 중앙값 결측·이상치 1% | 모든 값 NaN | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE05-013 | 중앙값 결측·이상치 1% | 중앙값 dtype | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE05-016 | 중앙값 결측·이상치 1% | 그룹 key NaN | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE05-017 | 중앙값 결측·이상치 1% | outlier 결과 빈 그룹 | pytest | FAIL | fixture | NOT_RUN | FAIL |

## DE05-007 모든 값 NaN
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: NaN 유지; 후속 품질검사 필요
- 실제: 업종 두 행 모두 NaN이면 fill_missing 결과도 [nan, nan]. 후속 품질검사 속성은 없음.
- 결함ID: DEF-DE05-007
- 코드: data/etl/transform.py

## DE05-013 중앙값 dtype
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 사전 숫자화 필요
- 실제: v=['1','2',None,'4'] 문자열 열에 fill_missing 호출 시 TypeError: median dtype=object. 사전 숫자 변환이 없음.
- 결함ID: DEF-DE05-013
- 코드: data/etl/transform.py

## DE05-016 그룹 key NaN
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 그룹 결측치 정책 확인
- 실제: industry=None 행의 v가 한식 1과 3의 중앙값 2.0으로 채워짐. 그룹키 결측 정책이 따로 없음.
- 결함ID: DEF-DE05-016
- 코드: data/etl/transform.py

## DE05-017 outlier 결과 빈 그룹
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: pd.concat(empty) 예외 방어
- 실제: industry=None 2행 remove_outliers가 ValueError 'No objects to concatenate'. 빈 그룹 방어가 없음.
- 결함ID: DEF-DE05-017
- 코드: data/etl/transform.py
