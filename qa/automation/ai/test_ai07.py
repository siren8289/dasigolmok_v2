"""AI07 RandomForest 폐업률 예측."""
import math
import time
import tracemalloc
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import pytest

from helpers import note
from src.features import make_input_frame
import src.ml_model as ml


def _frame(n=1, **overrides):
    rows = []
    for index in range(n):
        values = dict(
            district="마포구",
            industry="한식음식점",
            change_code="HH",
            store_count=10 + index,
            open_rate=1.1,
            franchise_ratio=0.2,
            foot_traffic=10000 + index * 100,
            operate_months=24,
        )
        values.update(overrides)
        if n > 1 and "store_count" not in overrides:
            values["store_count"] = 10 + index
        rows.append(values)
    return pd.DataFrame(rows)


def _one(**overrides):
    return make_input_frame(
        overrides.get("district", "마포구"),
        overrides.get("industry", "한식음식점"),
        overrides.get("change_code", "HH"),
        overrides.get("store_count", 10),
        overrides.get("open_rate", 1.1),
        overrides.get("franchise_ratio", 0.2),
        overrides.get("foot_traffic", 10000),
        overrides.get("operate_months", 24),
    )


class _FixedModel:
    def __init__(self, values):
        self.values = values

    def predict(self, frame):
        return np.array(self.values, dtype=float)


def test_AI07_001(monkeypatch):
    calls = {"n": 0}
    real = ml.joblib.load

    def wrapped(path):
        calls["n"] += 1
        return real(path)

    saved = ml._model
    ml._model = None
    monkeypatch.setattr(ml.joblib, "load", wrapped)
    try:
        model = ml.load_ml_model()
        evidence = f"joblib.load 호출={calls['n']} model={type(model).__name__} path={ml.MODEL_PATH.name}"
        note("AI07-001", evidence)
        assert calls["n"] == 1, evidence
        assert hasattr(model, "predict"), evidence
    finally:
        if ml._model is None:
            ml._model = saved


def test_AI07_002(monkeypatch):
    calls = {"n": 0}
    real = ml.joblib.load

    def wrapped(path):
        calls["n"] += 1
        return real(path)

    saved = ml._model
    ml._model = None
    monkeypatch.setattr(ml.joblib, "load", wrapped)
    try:
        first = ml.load_ml_model()
        second = ml.load_ml_model()
        evidence = f"2회 호출 load횟수={calls['n']} same={first is second}"
        note("AI07-002", evidence)
        assert calls["n"] == 1 and first is second, evidence
    finally:
        if ml._model is None:
            ml._model = saved


def test_AI07_003():
    predicted = ml.predict_ml(_one())
    evidence = f"1행 결과={predicted} types={[type(value).__name__ for value in predicted]}"
    note("AI07-003", evidence)
    assert isinstance(predicted, list) and len(predicted) == 1, evidence
    assert isinstance(predicted[0], float) and math.isfinite(predicted[0]), evidence


def test_AI07_004():
    batch = ml.predict_ml(_frame(3))
    singles = [
        ml.predict_ml(_one(store_count=10 + index, foot_traffic=10000 + index * 100))[0]
        for index in range(3)
    ]
    evidence = f"일괄과 단건 batch={batch} singles={singles}"
    note("AI07-004", evidence)
    assert batch == singles and len(batch) == 3, evidence


def test_AI07_005():
    saved = ml._model
    ml._model = _FixedModel([4.125])
    try:
        predicted = ml.predict_ml(_one())
        evidence = f"모델출력 4.125 → {predicted} round(4.125,2)={round(4.125, 2)}"
        note("AI07-005", evidence)
        assert predicted == [round(4.125, 2)] == [4.12], evidence
    finally:
        ml._model = saved


def test_AI07_006(tmp_path):
    saved = (ml._model, ml.MODEL_PATH)
    missing = tmp_path / "close_rf.joblib"
    ml._model = None
    ml.MODEL_PATH = missing
    try:
        with pytest.raises(FileNotFoundError) as caught:
            ml.load_ml_model()
        evidence = f"파일 없음 → {type(caught.value).__name__}: {caught.value}"
        note("AI07-006", evidence)
        assert missing.name in str(caught.value), evidence
    finally:
        ml._model, ml.MODEL_PATH = saved


def test_AI07_007(tmp_path, monkeypatch):
    saved = (ml._model, ml.MODEL_PATH)
    broken = tmp_path / "broken.joblib"
    broken.write_bytes(b"this is not a joblib file")
    ml._model = None
    ml.MODEL_PATH = broken
    logs = []
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: logs.append(" ".join(map(str, args))))
    try:
        try:
            ml.load_ml_model()
            outcome = "반환됨"
        except Exception as error:
            outcome = f"{type(error).__name__}: {error}"
        evidence = f"손상 joblib 결과={outcome[:180]} 로그={logs}"
        note("AI07-007", evidence)
        assert logs and any(("실패" in line) or ("error" in line.lower()) for line in logs), evidence
    finally:
        ml._model, ml.MODEL_PATH = saved


def test_AI07_008():
    frame = _one().drop(columns=["open_rate"])
    with pytest.raises(Exception) as caught:
        ml.predict_ml(frame)
    evidence = f"open_rate 누락 → {type(caught.value).__name__}: {caught.value}"
    note("AI07-008", evidence)
    assert "open_rate" in str(caught.value), evidence


def test_AI07_009():
    model = ml.load_ml_model()
    encoder = model.named_steps["preprocess"].named_transformers_["category"]
    predicted = ml.predict_ml(_one(industry="완전신규업종QA"))
    evidence = (
        f"신규 industry 예측={predicted} handle_unknown={encoder.handle_unknown!r}"
    )
    note("AI07-009", evidence)
    assert encoder.handle_unknown == "ignore", evidence
    assert len(predicted) == 1 and math.isfinite(predicted[0]), evidence


def test_AI07_010():
    saved = ml._model
    ml._model = _FixedModel([-2])
    try:
        predicted = ml.predict_ml(_one())
        evidence = f"음수 예측 model output=-2 → {predicted}"
        note("AI07-010", evidence)
        assert predicted[0] >= 0, evidence
    finally:
        ml._model = saved


def test_AI07_011():
    saved = ml._model
    ml._model = _FixedModel([105])
    try:
        predicted = ml.predict_ml(_one())
        evidence = f"백 초과 예측 model output=105 → {predicted}"
        note("AI07-011", evidence)
        assert predicted[0] <= 100, evidence
    finally:
        ml._model = saved


def test_AI07_012():
    saved = ml._model
    ml._model = _FixedModel([float("nan")])
    try:
        predicted = ml.predict_ml(_one())
        evidence = f"결측 예측 output=NaN → {predicted}"
        note("AI07-012", evidence)
        assert math.isfinite(predicted[0]), evidence
    finally:
        ml._model = saved


def test_AI07_013():
    frame = _frame(2)
    before = frame.copy(deep=True)
    ml.predict_ml(frame)
    evidence = f"예측 후 원본 동일={frame.equals(before)} columns={list(frame.columns)}"
    note("AI07-013", evidence)
    pd.testing.assert_frame_equal(frame, before)


def test_AI07_014():
    batch = ml.predict_ml(_frame(5))
    singles = [
        ml.predict_ml(_one(store_count=10 + index, foot_traffic=10000 + index * 100))[0]
        for index in range(5)
    ]
    evidence = f"5행 batch={batch} singles={singles}"
    note("AI07-014", evidence)
    assert batch == singles and len(batch) == 5, evidence


def test_AI07_015():
    empty = _one().iloc[0:0]
    try:
        predicted = ml.predict_ml(empty)
        outcome = predicted
    except Exception as error:
        outcome = f"{type(error).__name__}: {error}"
    evidence = f"0행 프레임 → {outcome}"
    note("AI07-015", evidence)
    assert outcome == [] or (isinstance(outcome, str) and "0 sample" in outcome), evidence


def test_AI07_016():
    frame = _frame(10_000)
    tracemalloc.start()
    started = time.perf_counter()
    predicted = ml.predict_ml(frame)
    elapsed = time.perf_counter() - started
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    evidence = (
        f"10000행 결과={len(predicted)} latency={elapsed:.3f}s peak_memory={peak / 1024 / 1024:.1f}MB"
    )
    note("AI07-016", evidence)
    assert len(predicted) == 10_000, evidence
    assert elapsed < 60, evidence
    assert peak < 1024 * 1024 * 1024, evidence


def test_AI07_017():
    frames = [_one(store_count=10 + index, foot_traffic=1000 * (index + 1)) for index in range(10)]
    sequential = [ml.predict_ml(frame) for frame in frames]
    with ThreadPoolExecutor(max_workers=10) as pool:
        parallel = list(pool.map(ml.predict_ml, frames))
    evidence = f"순차={sequential} 병렬={parallel}"
    note("AI07-017", evidence)
    assert parallel == sequential, evidence


def test_AI07_018():
    frame = _one(store_count=17, foot_traffic=22222)
    first = ml.predict_ml(frame)
    second = ml.predict_ml(frame.copy())
    evidence = f"1회={first} 2회={second}"
    note("AI07-018", evidence)
    assert first == second, evidence
