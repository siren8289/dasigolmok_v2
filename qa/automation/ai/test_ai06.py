"""AI06 ML·DL 피처."""
import math

import pandas as pd
import pytest

from helpers import note
from src.features import (
    CATEGORY_COLUMNS,
    FEATURE_COLUMNS,
    NUMBER_COLUMNS,
    make_input_frame,
)
from src.ml_model import load_ml_model, predict_ml


def _frame(**overrides):
    values = dict(
        district="마포구",
        industry="한식음식점",
        change_code="HL",
        store_count=13,
        open_rate=1.1,
        franchise_ratio=0.33,
        foot_traffic=50000,
        operate_months=18,
    )
    values.update(overrides)
    return make_input_frame(**values)


def test_AI06_001():
    frame = _frame(district="마포구")
    evidence = f"columns={list(frame.columns)} district={frame.loc[0, 'district']!r} dtype={frame['district'].dtype}"
    note("AI06-001", evidence)
    assert "district" in frame.columns and frame.loc[0, "district"] == "마포구", evidence


def test_AI06_002():
    frame = _frame(industry="한식음식점")
    evidence = f"industry={frame.loc[0, 'industry']!r}"
    note("AI06-002", evidence)
    assert "industry" in frame.columns and frame.loc[0, "industry"] == "한식음식점", evidence


def test_AI06_003():
    frame = _frame(change_code="HL")
    evidence = f"변화코드 change_code={frame.loc[0, 'change_code']!r}"
    note("AI06-003", evidence)
    assert "change_code" in frame.columns and frame.loc[0, "change_code"] == "HL", evidence


def test_AI06_004():
    frame = _frame(store_count=13)
    evidence = f"점포수 store_count={frame.loc[0, 'store_count']!r}"
    note("AI06-004", evidence)
    assert frame.loc[0, "store_count"] == 13, evidence


def test_AI06_005():
    frame = _frame(open_rate=1.1)
    evidence = f"개업률 open_rate={frame.loc[0, 'open_rate']!r}"
    note("AI06-005", evidence)
    assert frame.loc[0, "open_rate"] == 1.1, evidence


def test_AI06_006():
    frame = _frame(franchise_ratio=0.33)
    evidence = f"가맹비율 franchise_ratio={frame.loc[0, 'franchise_ratio']!r}"
    note("AI06-006", evidence)
    assert frame.loc[0, "franchise_ratio"] == 0.33, evidence


def test_AI06_007():
    frame = _frame(foot_traffic=50000)
    evidence = f"유동인구 foot_traffic={frame.loc[0, 'foot_traffic']!r}"
    note("AI06-007", evidence)
    assert frame.loc[0, "foot_traffic"] == 50000, evidence


def test_AI06_008():
    frame = _frame(operate_months=18)
    evidence = f"운영개월 operate_months={frame.loc[0, 'operate_months']!r}"
    note("AI06-008", evidence)
    assert frame.loc[0, "operate_months"] == 18, evidence


def test_AI06_009():
    evidence = f"특성 순서 FEATURE={FEATURE_COLUMNS} CATEGORY+NUMBER={CATEGORY_COLUMNS + NUMBER_COLUMNS}"
    note("AI06-009", evidence)
    assert FEATURE_COLUMNS == CATEGORY_COLUMNS + NUMBER_COLUMNS, evidence
    assert list(_frame().columns) == FEATURE_COLUMNS, evidence


def test_AI06_010():
    frame = _frame()
    evidence = f"columns={list(frame.columns)} ML_TARGET/DL_TARGET 포함여부 close_rate={'close_rate' in frame.columns} sales={'sales_per_store' in frame.columns}"
    note("AI06-010", evidence)
    assert "close_rate" not in FEATURE_COLUMNS and "sales_per_store" not in FEATURE_COLUMNS, evidence
    assert "close_rate" not in frame.columns and "sales_per_store" not in frame.columns, evidence


def test_AI06_011():
    frame = _frame()
    evidence = f"단일 행 shape={tuple(frame.shape)}"
    note("AI06-011", evidence)
    assert frame.shape[0] == 1, evidence


def test_AI06_012():
    frame = _frame()
    evidence = f"열 구성 shape={tuple(frame.shape)} columns={list(frame.columns)}"
    note("AI06-012", evidence)
    assert frame.shape[1] == 8, evidence


def test_AI06_013():
    try:
        frame = make_input_frame("마포구", "한식음식점", "HH", -1, 1.1, 0.2, 1000, 12)
        outcome = f"반환 store_count={frame.loc[0, 'store_count']!r}"
    except ValueError as error:
        outcome = f"ValueError: {error}"
    evidence = f"store_count=-1 → {outcome}"
    note("AI06-013", evidence)
    assert outcome.startswith("ValueError"), evidence


def test_AI06_014():
    model = load_ml_model()
    encoder = model.named_steps["preprocess"].named_transformers_["category"]
    frame = _frame(industry="UNKNOWN")
    try:
        predicted = predict_ml(frame)
        outcome = f"pred={predicted} handle_unknown={encoder.handle_unknown!r}"
    except Exception as error:
        outcome = f"{type(error).__name__}: {error} handle_unknown={getattr(encoder, 'handle_unknown', None)!r}"
        predicted = None
    evidence = f"미등록 업종 industry=UNKNOWN → {outcome}"
    note("AI06-014", evidence)
    assert getattr(encoder, "handle_unknown", None) == "ignore", evidence
    assert predicted is not None and len(predicted) == 1 and math.isfinite(predicted[0]), evidence


def test_AI06_015():
    frame = make_input_frame("마포구", "한식음식점", "HH", 10, 1.1, 0.2, float("nan"), 18)
    try:
        predicted = predict_ml(frame)
        outcome = f"pred={predicted}"
    except ValueError as error:
        outcome = f"ValueError: {error}"
        predicted = None
    except Exception as error:
        outcome = f"{type(error).__name__}: {error}"
        predicted = None
    evidence = f"결측 유동인구 foot_traffic=NaN frame={frame.loc[0, 'foot_traffic']!r} → {str(outcome)[:220]}"
    note("AI06-015", evidence)
    assert predicted is None and "NaN" in outcome, evidence


def test_AI06_016():
    frame = make_input_frame("마포구", "한식음식점", "HH", "10", 1.1, 0.2, 50000, 18)
    dtype = frame["store_count"].dtype
    evidence = f"문자 점포수 store_count='10' dtype={dtype} value={frame.loc[0, 'store_count']!r}"
    note("AI06-016", evidence)
    assert pd.api.types.is_numeric_dtype(frame["store_count"]), evidence
    with pytest.raises((TypeError, ValueError)):
        predict_ml(frame)


def test_AI06_017():
    frames = [
        make_input_frame("마포구", "한식음식점", "HH", index, 1.1, 0.2, 1000, 12)
        for index in range(100)
    ]
    merged = pd.concat(frames, ignore_index=True)
    evidence = f"행 결합 rows={len(merged)} columns={list(merged.columns)}"
    note("AI06-017", evidence)
    assert len(merged) == 100, evidence
    assert list(merged.columns) == FEATURE_COLUMNS, evidence
    assert list(merged.columns) == CATEGORY_COLUMNS + NUMBER_COLUMNS, evidence


def test_AI06_018():
    frame = make_input_frame("마포구", "한식음식점", "HH", 10**9, 1.1, 0.2, 50000, 18)
    value = frame.loc[0, "store_count"]
    evidence = f"store_count=1e9 저장값={value!r} dtype={frame['store_count'].dtype}"
    note("AI06-018", evidence)
    assert int(value) == 1_000_000_000, evidence
