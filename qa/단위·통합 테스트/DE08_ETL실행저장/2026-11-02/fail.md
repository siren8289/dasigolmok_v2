# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE08-005 | 데이터 수집→전처리→아티팩트 | 서울 점포 API 실패 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE08-013 | 데이터 수집→전처리→아티팩트 | 불완전 데이터 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE08-014 | 데이터 수집→전처리→아티팩트 | 최신 분기 데이터 지연 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE08-017 | 데이터 수집→전처리→아티팩트 | 저장 중 크래시 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE08-018 | 데이터 수집→전처리→아티팩트 | 기존 모델 데이터 갱신 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE08-022 | 데이터 수집→전처리→아티팩트 | 상세 로그 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE08-023 | 데이터 수집→전처리→아티팩트 | 출처 자료 최신성 | pytest | FAIL | fixture | NOT_RUN | FAIL |

## DE08-005 서울 점포 API 실패
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 실패 로그 후 종료
- 실제: store 수집 RuntimeError는 전파되고 train.csv는 없음. stdout은 '[1/3] 수집'과 소상공인 성공 로그만 있고 '실패'/'오류' 로그는 없음.
- 결함ID: DEF-DE08-005
- 코드: data/etl/run.py

## DE08-013 불완전 데이터
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 완료로 위장하지 않도록 품질 게이트 필요
- 실제: 매출 0행으로 run()이 예외 없이 반환. 완료로 위장하지 않는 품질 게이트가 없음.
- 결함ID: DEF-DE08-013
- 코드: data/etl/run.py

## DE08-014 최신 분기 데이터 지연
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: quarter 선택 정책 확인
- 실제: 20241은 3업종, 20242는 1업종인데 dong_stats 분기는 {'20242'} 1행. 부분 분기에 대한 선택 정책 표시가 없음.
- 결함ID: DEF-DE08-014
- 코드: data/etl/run.py

## DE08-017 저장 중 크래시
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 원자적 파일 교체 필요
- 실제: 기존 train.csv 'GOOD\n'이 쓰기 도중 'PARTIAL'로 덮인 뒤 RuntimeError. 원자적 교체가 아님.
- 결함ID: DEF-DE08-017
- 코드: data/etl/run.py

## DE08-018 기존 모델 데이터 갱신
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 모델/옵션 배포 싱크 확인
- 실제: ETL options에는 QA동기화업종이 생기지만 ai/models/options.json에는 없음. 모델 옵션 동기화 없음.
- 결함ID: DEF-DE08-018
- 코드: data/etl/run.py

## DE08-022 상세 로그
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 행 수·기간 기록
- 실제: 로그에 학습용 행 수는 있으나 분기 '20242'나 '분기' 문구는 없음.
- 결함ID: DEF-DE08-022
- 코드: data/etl/run.py

## DE08-023 출처 자료 최신성
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 데이터 기준일과 실제 처리일을 기록
- 실제: options 키는 districts,dongs,industries,semas_dong_count,semas_upjong_count 5개. 기준일·처리일 키가 없음.
- 결함ID: DEF-DE08-023
- 코드: data/etl/run.py
