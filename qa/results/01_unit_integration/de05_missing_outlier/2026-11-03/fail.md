# FAIL

## 20261103-010421

- 실행 시각: 2026-11-03T01:04:21+0900
- Git Commit: 16c28b4-dirty
### TC-REG-DE05-001 결측·이상치 회귀

- 실행 시각: 2026-11-03T01:04:21+0900
- Git Commit: 16c28b4-dirty
- 영역: 단위·통합 테스트
- 섹션: DE05_결측치이상치
- 테스트 종류: regression
- 검증 목적: 기존 DE05 경계 테스트와 독립 오라클이 서로 맞는지 확인
- 도구 A: pytest / 결과 FAIL
- 도구 A 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pytest qa/automation/de/test_de05.py -q`
- 도구 B: regression_oracle / 결과 PASS
- 도구 B 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 qa/runner/tools/regression_oracle.py`
- 최종 상태: FAIL
- 기대 결과: DE05 pytest와 오라클이 모두 통과
- 실제 결과: A=FAIL, B=PASS, final=FAIL
- 근거: A[FAIL] thon3.11/site-packages/pandas/core/reshape/concat.py:808: ValueError
=========================== short test summary info ============================
FAILED qa/automation/de/test_de05.py::test_DE05_007 - AssertionError: 전체 Na...
FAILED qa/automation/de/test_de05.py::test_DE05_013 - TypeError: dtype 'str' ...
FAILED qa/automation/de/test_de05.py::test_DE05_016 - AssertionError: industr...
FAILED qa/automation/de/test_de05.py::test_DE05_017 - ValueError: No objects ...
4 failed, 15 passed in 3.56s || B[PASS] oracle PASS to_number 빈값·NULL·예외, clean_sales 100000000원=10000만원
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
- 입력값: -
- 오류 메시지: , 10_000_000.0]})
>       out = remove_outliers(df, "v", "industry")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

qa/automation/de/test_de05.py:136: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
data/etl/transform.py:117: in remove_outliers
    return pd.concat(kept, ignore_index=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/pandas/core/reshape/concat.py:407: in concat
    objs, keys, ndims = _clean_keys_and_objs(objs, keys)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

objs = [], keys = None

    def _clean_keys_and_objs(
        objs: Iterable[Series | DataFrame] | Mapping[HashableT, Series | DataFrame],
        keys,
    ) -> tuple[list[Series | DataFrame], Index | None, set[int]]:
        """
        Returns
        -------
        clean_objs : list[Series | DataFrame]
            List of DataFrame and Series with Nones removed.
        keys : Index | None
            None if keys was None
            Index if objs was a Mapping or keys was not None. Filtered where objs was None.
        ndim : set[int]
            Unique .ndim attribute of obj encountered.
        """
        if isinstance(objs, abc.Mapping):
            if keys is None:
                keys = objs.keys()
            objs = [objs[k] for k in keys]
        elif isinstance(objs, (ABCSeries, ABCDataFrame)) or is_scalar(objs):
            raise TypeError(
                "first argument must be an iterable of pandas "
                f'objects, you passed an object of type "{type(objs).__name__}"'
            )
        elif not isinstance(objs, abc.Sized):
            objs = list(objs)
    
        if len(objs) == 0:
>           raise ValueError("No objects to concatenate")
E           ValueError: No objects to concatenate

/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/pandas/core/reshape/concat.py:808: ValueError
=========================== short test summary info ============================
FAILED qa/automation/de/test_de05.py::test_DE05_007 - AssertionError: 전체 Na...
FAILED qa/automation/de/test_de05.py::test_DE05_013 - TypeError: dtype 'str' ...
FAILED qa/automation/de/test_de05.py::test_DE05_016 - AssertionError: industr...
FAILED qa/automation/de/test_de05.py::test_DE05_017 - ValueError: No objects ...
4 failed, 15 passed in 3.56s
- 재현 방법: /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pytest qa/automation/de/test_de05.py -q
- 원인 분석: 도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다.
- 수정 코드 위치: 아직 수정하지 않음
- 재검증: 아직 재검증하지 않음

## 20261103-015837

- 실행 시각: 2026-11-03T01:58:37+0900
- Git Commit: fdfdce7-dirty
### TC-REG-DE05-001 결측·이상치 회귀

- 실행 시각: 2026-11-03T01:58:37+0900
- Git Commit: fdfdce7-dirty
- 영역: 01_unit_integration
- 섹션: de05_missing_outlier
- 테스트 종류: regression
- 검증 목적: 기존 DE05 경계 테스트와 독립 오라클이 서로 맞는지 확인
- 도구 A: pytest / 결과 FAIL
- 도구 A 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pytest qa/automation/de/test_de05.py -q`
- 도구 B: regression_oracle / 결과 PASS
- 도구 B 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 qa/runner/tools/regression_oracle.py`
- 최종 상태: FAIL
- 기대 결과: DE05 pytest와 오라클이 모두 통과
- 실제 결과: A=FAIL, B=PASS, final=FAIL
- 근거: A[FAIL] thon3.11/site-packages/pandas/core/reshape/concat.py:808: ValueError
=========================== short test summary info ============================
FAILED qa/automation/de/test_de05.py::test_DE05_007 - AssertionError: 전체 Na...
FAILED qa/automation/de/test_de05.py::test_DE05_013 - TypeError: dtype 'str' ...
FAILED qa/automation/de/test_de05.py::test_DE05_016 - AssertionError: industr...
FAILED qa/automation/de/test_de05.py::test_DE05_017 - ValueError: No objects ...
4 failed, 15 passed in 8.41s || B[PASS] oracle PASS to_number 빈값·NULL·예외, clean_sales 100000000원=10000만원
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
- 입력값: -
- 오류 메시지: , 10_000_000.0]})
>       out = remove_outliers(df, "v", "industry")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

qa/automation/de/test_de05.py:136: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
data/etl/transform.py:117: in remove_outliers
    return pd.concat(kept, ignore_index=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/pandas/core/reshape/concat.py:407: in concat
    objs, keys, ndims = _clean_keys_and_objs(objs, keys)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

objs = [], keys = None

    def _clean_keys_and_objs(
        objs: Iterable[Series | DataFrame] | Mapping[HashableT, Series | DataFrame],
        keys,
    ) -> tuple[list[Series | DataFrame], Index | None, set[int]]:
        """
        Returns
        -------
        clean_objs : list[Series | DataFrame]
            List of DataFrame and Series with Nones removed.
        keys : Index | None
            None if keys was None
            Index if objs was a Mapping or keys was not None. Filtered where objs was None.
        ndim : set[int]
            Unique .ndim attribute of obj encountered.
        """
        if isinstance(objs, abc.Mapping):
            if keys is None:
                keys = objs.keys()
            objs = [objs[k] for k in keys]
        elif isinstance(objs, (ABCSeries, ABCDataFrame)) or is_scalar(objs):
            raise TypeError(
                "first argument must be an iterable of pandas "
                f'objects, you passed an object of type "{type(objs).__name__}"'
            )
        elif not isinstance(objs, abc.Sized):
            objs = list(objs)
    
        if len(objs) == 0:
>           raise ValueError("No objects to concatenate")
E           ValueError: No objects to concatenate

/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/pandas/core/reshape/concat.py:808: ValueError
=========================== short test summary info ============================
FAILED qa/automation/de/test_de05.py::test_DE05_007 - AssertionError: 전체 Na...
FAILED qa/automation/de/test_de05.py::test_DE05_013 - TypeError: dtype 'str' ...
FAILED qa/automation/de/test_de05.py::test_DE05_016 - AssertionError: industr...
FAILED qa/automation/de/test_de05.py::test_DE05_017 - ValueError: No objects ...
4 failed, 15 passed in 8.41s
- 재현 방법: /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pytest qa/automation/de/test_de05.py -q
- 원인 분석: 도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다.
- 수정 코드 위치: 아직 수정하지 않음
- 재검증: 아직 재검증하지 않음
