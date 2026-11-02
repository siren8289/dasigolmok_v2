# FAIL

## 20261102-201533

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty
### TC-REG-DE05-001 결측·이상치 회귀

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: regression
- 검증 목적: 기존 DE05 경계 테스트와 독립 오라클이 서로 맞는지 확인
- 도구 A: pytest / 결과 FAIL
- 도구 A 명령: `/private/tmp/qa-venv/bin/python -m pytest qa/automation/de/test_de05.py -q`
- 도구 B: regression_oracle / 결과 PASS
- 도구 B 명령: `/private/tmp/qa-venv/bin/python qa/runner/tools/regression_oracle.py`
- 최종 상태: FAIL
- 기대 결과: DE05 pytest와 오라클이 모두 통과
- 실제 결과: A=FAIL, B=PASS, final=FAIL
- 근거: A[FAIL] ://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED qa/automation/de/test_de05.py::test_DE05_007 - AssertionError: 전체 Na...
FAILED qa/automation/de/test_de05.py::test_DE05_013 - TypeError: agg function...
FAILED qa/automation/de/test_de05.py::test_DE05_016 - AssertionError: industr...
FAILED qa/automation/de/test_de05.py::test_DE05_017 - ValueError: No objects ...
4 failed, 15 passed, 1 warning in 0.62s || B[PASS] oracle PASS to_number 빈값·NULL·예외, clean_sales 100000000원=10000만원
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
- 입력값: -
- 오류 메시지: _______ test_DE05_017 _________________________________

    def test_DE05_017():
        df = pd.DataFrame({"industry": [None, None], "v": [1.0, 10_000_000.0]})
>       out = remove_outliers(df, "v", "industry")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

qa/automation/de/test_de05.py:136: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
data/etl/transform.py:117: in remove_outliers
    return pd.concat(kept, ignore_index=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/private/tmp/qa-venv/lib/python3.11/site-packages/pandas/core/reshape/concat.py:382: in concat
    op = _Concatenator(
/private/tmp/qa-venv/lib/python3.11/site-packages/pandas/core/reshape/concat.py:445: in __init__
    objs, keys = self._clean_keys_and_objs(objs, keys)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <pandas.core.reshape.concat._Concatenator object at 0x105dda510>
objs = [], keys = None

    def _clean_keys_and_objs(
        self,
        objs: Iterable[Series | DataFrame] | Mapping[HashableT, Series | DataFrame],
        keys,
    ) -> tuple[list[Series | DataFrame], Index | None]:
        if isinstance(objs, abc.Mapping):
            if keys is None:
                keys = list(objs.keys())
            objs_list = [objs[k] for k in keys]
        else:
            objs_list = list(objs)
    
        if len(objs_list) == 0:
>           raise ValueError("No objects to concatenate")
E           ValueError: No objects to concatenate

/private/tmp/qa-venv/lib/python3.11/site-packages/pandas/core/reshape/concat.py:507: ValueError
=============================== warnings summary ===============================
qa/automation/de/test_de05.py::test_DE05_007
  /private/tmp/qa-venv/lib/python3.11/site-packages/numpy/lib/_nanfunctions_impl.py:1213: RuntimeWarning: Mean of empty slice
    return np.nanmean(a, axis, out=out, keepdims=keepdims)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED qa/automation/de/test_de05.py::test_DE05_007 - AssertionError: 전체 Na...
FAILED qa/automation/de/test_de05.py::test_DE05_013 - TypeError: agg function...
FAILED qa/automation/de/test_de05.py::test_DE05_016 - AssertionError: industr...
FAILED qa/automation/de/test_de05.py::test_DE05_017 - ValueError: No objects ...
4 failed, 15 passed, 1 warning in 0.62s
- 재현 방법: /private/tmp/qa-venv/bin/python -m pytest qa/automation/de/test_de05.py -q
- 원인 분석: 도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다.
- 수정 코드 위치: 아직 수정하지 않음
- 재검증: 아직 재검증하지 않음

## 20261102-221207

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
### TC-REG-DE05-001 결측·이상치 회귀

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: regression
- 검증 목적: 기존 DE05 경계 테스트와 독립 오라클이 서로 맞는지 확인
- 도구 A: pytest / 결과 FAIL
- 도구 A 명령: `/private/tmp/qa-venv/bin/python -m pytest qa/automation/de/test_de05.py -q`
- 도구 B: regression_oracle / 결과 PASS
- 도구 B 명령: `/private/tmp/qa-venv/bin/python qa/runner/tools/regression_oracle.py`
- 최종 상태: FAIL
- 기대 결과: DE05 pytest와 오라클이 모두 통과
- 실제 결과: A=FAIL, B=PASS, final=FAIL
- 근거: A[FAIL] ://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED qa/automation/de/test_de05.py::test_DE05_007 - AssertionError: 전체 Na...
FAILED qa/automation/de/test_de05.py::test_DE05_013 - TypeError: agg function...
FAILED qa/automation/de/test_de05.py::test_DE05_016 - AssertionError: industr...
FAILED qa/automation/de/test_de05.py::test_DE05_017 - ValueError: No objects ...
4 failed, 15 passed, 1 warning in 1.26s || B[PASS] oracle PASS to_number 빈값·NULL·예외, clean_sales 100000000원=10000만원
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
- 입력값: -
- 오류 메시지: _______ test_DE05_017 _________________________________

    def test_DE05_017():
        df = pd.DataFrame({"industry": [None, None], "v": [1.0, 10_000_000.0]})
>       out = remove_outliers(df, "v", "industry")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

qa/automation/de/test_de05.py:136: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
data/etl/transform.py:117: in remove_outliers
    return pd.concat(kept, ignore_index=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/private/tmp/qa-venv/lib/python3.11/site-packages/pandas/core/reshape/concat.py:382: in concat
    op = _Concatenator(
/private/tmp/qa-venv/lib/python3.11/site-packages/pandas/core/reshape/concat.py:445: in __init__
    objs, keys = self._clean_keys_and_objs(objs, keys)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <pandas.core.reshape.concat._Concatenator object at 0x1024d86d0>
objs = [], keys = None

    def _clean_keys_and_objs(
        self,
        objs: Iterable[Series | DataFrame] | Mapping[HashableT, Series | DataFrame],
        keys,
    ) -> tuple[list[Series | DataFrame], Index | None]:
        if isinstance(objs, abc.Mapping):
            if keys is None:
                keys = list(objs.keys())
            objs_list = [objs[k] for k in keys]
        else:
            objs_list = list(objs)
    
        if len(objs_list) == 0:
>           raise ValueError("No objects to concatenate")
E           ValueError: No objects to concatenate

/private/tmp/qa-venv/lib/python3.11/site-packages/pandas/core/reshape/concat.py:507: ValueError
=============================== warnings summary ===============================
qa/automation/de/test_de05.py::test_DE05_007
  /private/tmp/qa-venv/lib/python3.11/site-packages/numpy/lib/_nanfunctions_impl.py:1213: RuntimeWarning: Mean of empty slice
    return np.nanmean(a, axis, out=out, keepdims=keepdims)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED qa/automation/de/test_de05.py::test_DE05_007 - AssertionError: 전체 Na...
FAILED qa/automation/de/test_de05.py::test_DE05_013 - TypeError: agg function...
FAILED qa/automation/de/test_de05.py::test_DE05_016 - AssertionError: industr...
FAILED qa/automation/de/test_de05.py::test_DE05_017 - ValueError: No objects ...
4 failed, 15 passed, 1 warning in 1.26s
- 재현 방법: /private/tmp/qa-venv/bin/python -m pytest qa/automation/de/test_de05.py -q
- 원인 분석: 도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다.
- 수정 코드 위치: 아직 수정하지 않음
- 재검증: 아직 재검증하지 않음
