# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE03-013 | 점포 통계 clean_store | 프랜차이즈 결측 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE03-017 | 점포 통계 clean_store | 선행 영점 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE03-018 | 점포 통계 clean_store | 동이 빈 문자열 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE03-019 | 점포 통계 clean_store | 폐업률 120% | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE03-020 | 점포 통계 clean_store | 점포수 소수 | pytest | FAIL | fixture | NOT_RUN | FAIL |

## DE03-013 프랜차이즈 결측
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: NaN 후처리 필요
- 실제: franchise_count=None, store_count=10일 때 franchise_ratio=nan. NaN 후처리가 없음.
- 결함ID: DEF-DE03-013
- 코드: data/etl/transform.py

## DE03-017 선행 영점
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 자치구 코드 보존 확인
- 실제: 행정동 코드 float 11440740.0이 dong_code '11440740.0'으로 저장됨. district는 마포구로 맞지만 코드 문자열이 달라짐.
- 결함ID: DEF-DE03-017
- 코드: data/etl/transform.py

## DE03-018 동이 빈 문자열
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 잘못된 지역 엔트리 배제 필요
- 실제: dong='' 이고 코드 11440740·점포 10인 행이 1건 남음. 빈 동 이름이 걸러지지 않음.
- 결함ID: DEF-DE03-018
- 코드: data/etl/transform.py

## DE03-019 폐업률 120%
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 0~100 데이터 정합성 검증
- 실제: close_rate=120이 클리핑·제외 없이 1행으로 통과.
- 결함ID: DEF-DE03-019
- 코드: data/etl/transform.py

## DE03-020 점포수 소수
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 정수로 검증하거나 사유 문서화
- 실제: store_count=2.5가 정수 검증 없이 1행으로 통과.
- 결함ID: DEF-DE03-020
- 코드: data/etl/transform.py
