# PASS

## 20261102-201533

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty
### TC-UNIT-RECORD-001 QA 기록기

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: unit
- 검증 목적: 같은 날짜의 이전 RUN을 유지하고 미실행 종류 폴더를 만들지 않는지 확인
- 도구 A: pytest / 결과 PASS
- 도구 A 명령: `/private/tmp/qa-venv/bin/python -m pytest qa/runner/tests/test_record.py -q`
- 도구 B: python / 결과 PASS
- 도구 B 명령: `/private/tmp/qa-venv/bin/python qa/runner/tools/check_record.py`
- 최종 상태: PASS
- 기대 결과: 두 실행기 모두 누적 기록 검사를 통과
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] .                                                                        [100%]
1 passed in 0.01s || B[PASS] check_record PASS
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
### TC-UNIT-PY-001 ETL 전처리

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: unit
- 검증 목적: 정상값·빈 값·예외 문자·NULL과 매출 단위 변환을 pytest와 독립 오라클로 교차
- 도구 A: pytest / 결과 PASS
- 도구 A 명령: `/private/tmp/qa-venv/bin/python -m pytest data/tests -q`
- 도구 B: regression_oracle / 결과 PASS
- 도구 B 명령: `/private/tmp/qa-venv/bin/python qa/runner/tools/regression_oracle.py`
- 최종 상태: PASS
- 기대 결과: pytest data/tests 통과이고 오라클 경계값 통과
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] .....                                                                    [100%]
5 passed in 0.39s || B[PASS] oracle PASS to_number 빈값·NULL·예외, clean_sales 100000000원=10000만원
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -

## 20261102-201658

- 실행 시각: 2026-11-02T20:16:58+0900
- Git Commit: 4c28384-dirty
이 RUN에서 PASS는 없다.

## 20261102-201740

- 실행 시각: 2026-11-02T20:17:40+0900
- Git Commit: 4c28384-dirty
이 RUN에서 PASS는 없다.

## 20261102-221207

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
### TC-UNIT-RECORD-001 QA 기록기

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: unit
- 검증 목적: 같은 날짜의 이전 RUN을 유지하고 미실행 종류 폴더를 만들지 않는지 확인
- 도구 A: pytest / 결과 PASS
- 도구 A 명령: `/private/tmp/qa-venv/bin/python -m pytest qa/runner/tests/test_record.py -q`
- 도구 B: python / 결과 PASS
- 도구 B 명령: `/private/tmp/qa-venv/bin/python qa/runner/tools/check_record.py`
- 최종 상태: PASS
- 기대 결과: 두 실행기 모두 누적 기록 검사를 통과
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] .                                                                        [100%]
1 passed in 0.01s || B[PASS] check_record PASS
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
### TC-UNIT-PY-001 ETL 전처리

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: unit
- 검증 목적: 정상값·빈 값·예외 문자·NULL과 매출 단위 변환을 pytest와 독립 오라클로 교차
- 도구 A: pytest / 결과 PASS
- 도구 A 명령: `/private/tmp/qa-venv/bin/python -m pytest data/tests -q`
- 도구 B: regression_oracle / 결과 PASS
- 도구 B 명령: `/private/tmp/qa-venv/bin/python qa/runner/tools/regression_oracle.py`
- 최종 상태: PASS
- 기대 결과: pytest data/tests 통과이고 오라클 경계값 통과
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] .....                                                                    [100%]
5 passed in 0.48s || B[PASS] oracle PASS to_number 빈값·NULL·예외, clean_sales 100000000원=10000만원
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
