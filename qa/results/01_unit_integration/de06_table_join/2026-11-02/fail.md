# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE06-004 | 4종 표 join·파생 변수 | 기준 점포 유지 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE06-011 | 4종 표 join·파생 변수 | 점포 2개 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE06-016 | 4종 표 join·파생 변수 | 조인 중복 방지 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE06-021 | 4종 표 join·파생 변수 | 날짜 분기 문자열 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE06-024 | 4종 표 join·파생 변수 | 업종 정보 누락 | pytest | FAIL | fixture | NOT_RUN | FAIL |

## DE06-004 기준 점포 유지
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: left join으로 점포 정보 보존
- 실제: 매출 테이블 0행 left join 후 최종 0행. 점포(연남동·한식)가 sales_per_store NaN 이상치 제거에서 탈락.
- 결함ID: DEF-DE06-004
- 코드: data/etl/transform.py

## DE06-011 점포 2개
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 학습 데이터에서 제외
- 실제: store_count=2 단독 행은 제외 대상이나 remove_outliers가 빈 표에서 ValueError 'No objects to concatenate'. 빈 학습셋이 반환되지 않음.
- 결함ID: DEF-DE06-011
- 코드: data/etl/transform.py

## DE06-016 조인 중복 방지
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: row 개수 비정상 증식 감지
- 실제: 동일 quarter/dong_code 인구 2행을 붙이면 점포 1행이 결과 2행으로 늘어남. 중복 증식 감지 없음.
- 결함ID: DEF-DE06-016
- 코드: data/etl/transform.py

## DE06-021 날짜 분기 문자열
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 분기 정렬 유효 형식 검증
- 실제: quarter '20249'와 '202410'의 문자열 max는 '20249'. dong_stats 분기가 ['20249']이고 형식 검증 예외가 없음.
- 결함ID: DEF-DE06-021
- 코드: data/etl/transform.py

## DE06-024 업종 정보 누락
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 최종 모델 피처 오류 방어
- 실제: industry=None이면 ValueError 'No objects to concatenate'. 메시지에 업종/industry가 없어 피처 방어가 아님.
- 결함ID: DEF-DE06-024
- 코드: data/etl/transform.py
