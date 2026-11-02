# PASS

## 20261103-010421

- 실행 시각: 2026-11-03T01:04:21+0900
- Git Commit: 16c28b4-dirty
### TC-UNIT-PY-001 ETL 전처리

- 실행 시각: 2026-11-03T01:04:21+0900
- Git Commit: 16c28b4-dirty
- 영역: 단위·통합 테스트
- 섹션: DE05_결측치이상치
- 테스트 종류: unit
- 검증 목적: 정상값·빈 값·예외 문자·NULL과 매출 단위 변환을 pytest와 독립 오라클로 교차
- 도구 A: pytest / 결과 PASS
- 도구 A 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pytest data/tests -q`
- 도구 B: regression_oracle / 결과 PASS
- 도구 B 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 qa/runner/tools/regression_oracle.py`
- 최종 상태: PASS
- 기대 결과: pytest data/tests 통과이고 오라클 경계값 통과
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] .....                                                                    [100%]
5 passed in 8.41s || B[PASS] oracle PASS to_number 빈값·NULL·예외, clean_sales 100000000원=10000만원
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -

## 20261103-015837

- 실행 시각: 2026-11-03T01:58:37+0900
- Git Commit: fdfdce7-dirty
### TC-UNIT-PY-001 ETL 전처리

- 실행 시각: 2026-11-03T01:58:37+0900
- Git Commit: fdfdce7-dirty
- 영역: 01_unit_integration
- 섹션: de05_missing_outlier
- 테스트 종류: unit
- 검증 목적: 정상값·빈 값·예외 문자·NULL과 매출 단위 변환을 pytest와 독립 오라클로 교차
- 도구 A: pytest / 결과 PASS
- 도구 A 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pytest data/tests -q`
- 도구 B: regression_oracle / 결과 PASS
- 도구 B 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 qa/runner/tools/regression_oracle.py`
- 최종 상태: PASS
- 기대 결과: pytest data/tests 통과이고 오라클 경계값 통과
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] .....                                                                    [100%]
5 passed in 9.29s || B[PASS] oracle PASS to_number 빈값·NULL·예외, clean_sales 100000000원=10000만원
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
