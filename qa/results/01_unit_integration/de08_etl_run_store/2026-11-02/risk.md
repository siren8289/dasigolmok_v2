# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE08-001 | 데이터 수집→전처리→아티팩트 | 전체 실행 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-002 | 데이터 수집→전처리→아티팩트 | 캐시 실행 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-003 | 데이터 수집→전처리→아티팩트 | 캐시 없을 때 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-004 | 데이터 수집→전처리→아티팩트 | SEMAS API 실패 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-006 | 데이터 수집→전처리→아티팩트 | 서울 매출 API 실패 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-007 | 데이터 수집→전처리→아티팩트 | 서울 유동인구 실패 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-008 | 데이터 수집→전처리→아티팩트 | 서울 상권변화 실패 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-009 | 데이터 수집→전처리→아티팩트 | 저장 processed/train | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-010 | 데이터 수집→전처리→아티팩트 | 저장 processed/dong_stats | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-011 | 데이터 수집→전처리→아티팩트 | 저장 processed/options | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-012 | 데이터 수집→전처리→아티팩트 | 원본 저장 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-015 | 데이터 수집→전처리→아티팩트 | JSON 인코딩 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-016 | 데이터 수집→전처리→아티팩트 | 파일 쓰기 실패 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-019 | 데이터 수집→전처리→아티팩트 | ETL 멱등성 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-020 | 데이터 수집→전처리→아티팩트 | ETL 원본 공개 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE08-021 | 데이터 수집→전처리→아티팩트 | 서버 CI 범위 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |

## DE08-001 전체 실행
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: mock 수집으로 run() stdout에 [1/3] 수집, [2/3] 전처리, [3/3] 저장이 모두 있음.

## DE08-002 캐시 실행
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: --skip-download이고 raw 4파일이 있으면 fetch 호출 0, 로그 '캐시 사용' 4회.

## DE08-003 캐시 없을 때
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: --skip-download인데 raw가 없으면 fetch 순서가 store,sales,pop,change.

## DE08-004 SEMAS API 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 업종 API RuntimeError 후 '건너뜁니다'. semas_dong_count=0, semas_upjong_count=0, [3/3] 저장까지 진행.

## DE08-006 서울 매출 API 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: sales 예외 시 raw/store.csv는 생기고 train.csv, dong_stats.csv, options.json은 없음.

## DE08-007 서울 유동인구 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: pop 단계에서 RuntimeError '유동인구 수집 실패'가 전파되고 train.csv는 없음.

## DE08-008 서울 상권변화 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change 단계에서 RuntimeError '상권변화 수집 실패'가 전파되고 options.json은 없음.

## DE08-009 저장 processed/train
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: processed/train.csv가 생성되고 행은 1행 이상, sales_per_store 컬럼이 있음.

## DE08-010 저장 processed/dong_stats
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: processed/dong_stats.csv가 생성되고 행은 1행 이상, median_close_rate 컬럼이 있음.

## DE08-011 저장 processed/options
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: processed/options.json에 districts, dongs, industries가 있음.

## DE08-012 원본 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 최초 수집 후 raw/store.csv, sales.csv, pop.csv, change.csv 4개 모두 크기 >0.

## DE08-015 JSON 인코딩
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: options.json을 utf-8로 읽으면 '연남동'이 있고 \\u 이스케이프는 없음.

## DE08-016 파일 쓰기 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: processed 디렉터리 권한 0o555에서 save_processed는 PermissionError. train.csv는 생기지 않음.

## DE08-019 ETL 멱등성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 raw로 2회 실행한 train.csv 바이트가 같고 duplicated 행은 0.

## DE08-020 ETL 원본 공개
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: raw 4개 CSV에 DATA_GO_KR_KEY, 주민, 전화번호, 이메일, 010-가 없음. store 헤더에 점포_수가 있음.

## DE08-021 서버 CI 범위
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: pytest data/tests 종료 코드 0. 기존 전처리 테스트가 통과.
