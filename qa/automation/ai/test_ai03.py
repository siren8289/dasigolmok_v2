"""AI03 상권 진단 오케스트레이션."""
import json
import math
import time

from helpers import note, patch_diagnose, request_for, stat_row
from src.features import FEATURE_COLUMNS
from src.service import diagnose
import src.dong_stats as ds


def test_AI03_001():
    matches = [
        row for row in ds.load_stats()
        if row["dong"] == "연남동" and row["industry"] == "한식음식점"
    ]
    result = diagnose({"district": "마포구", "dong": "연남동", "industry": "한식음식점"})
    evidence = (
        f"매칭행={len(matches)} error={result.get('error')} "
        f"close_rate={result.get('close_rate')} store={result.get('store_count')} "
        f"quarter={result.get('quarter')}"
    )
    note("AI03-001", evidence)
    assert len(matches) == 1 and "error" not in result, evidence
    assert result["close_rate"] == matches[0]["close_rate"], evidence
    assert result["store_count"] == matches[0]["store_count"], evidence
    assert result["quarter"] == matches[0]["quarter"], evidence


def test_AI03_002():
    result = diagnose({"district": "마포구", "dong": "연남동", "industry": "없는업종QA"})
    evidence = f"없는 업종 결과={result}"
    note("AI03-002", evidence)
    assert result.get("error"), evidence


def test_AI03_003():
    result = diagnose({"district": "마포구", "dong": "없는동QA", "industry": "한식음식점"})
    evidence = f"없는 동 결과={result}"
    note("AI03-003", evidence)
    assert result.get("error"), evidence


def test_AI03_004():
    result = diagnose({"district": "강남구", "dong": "연남동", "industry": "한식음식점"})
    evidence = (
        f"입력 district=강남구 결과 district={result.get('district')} "
        f"error={result.get('error')}"
    )
    note("AI03-004", evidence)
    assert result.get("error"), evidence


def test_AI03_005(monkeypatch):
    capture = {}
    row = stat_row(store_count=10, open_rate=2.2, franchise_ratio=0.15, foot_traffic=35000, operate_months=50)
    patch_diagnose(monkeypatch, row, capture=capture)
    diagnose(request_for(row))
    frame = capture["frame"]
    evidence = f"입력 열 columns={list(frame.columns)} shape={tuple(frame.shape)} store_count={frame.loc[0, 'store_count']}"
    note("AI03-005", evidence)
    assert list(frame.columns) == FEATURE_COLUMNS, evidence
    assert frame.shape == (1, 8), evidence
    assert frame.loc[0, "store_count"] == 10, evidence


def test_AI03_006(monkeypatch):
    row = stat_row()
    patch_diagnose(monkeypatch, row, ml=[3.33], dl=[450.0])
    result = diagnose(request_for(row))
    evidence = f"예측 폐업률 ml_close_rate={result.get('ml_close_rate')}"
    note("AI03-006", evidence)
    assert result["ml_close_rate"] == 3.33, evidence


def test_AI03_007(monkeypatch):
    row = stat_row()
    patch_diagnose(monkeypatch, row, ml=[3.33], dl=[450.0])
    result = diagnose(request_for(row))
    evidence = f"예측 매출 dl_sales_per_store={result.get('dl_sales_per_store')}"
    note("AI03-007", evidence)
    assert result["dl_sales_per_store"] == 450.0, evidence


def test_AI03_008(monkeypatch):
    row = stat_row(close_rate=9.2, change_code="HH")
    patch_diagnose(monkeypatch, row)
    result = diagnose(request_for(row))
    evidence = f"고폐업 판정 close_rate=9.2 status={result.get('status')} is_danger={result.get('is_danger')}"
    note("AI03-008", evidence)
    assert result["status"] == "danger" and result["is_danger"] is True, evidence


def test_AI03_009(monkeypatch):
    row = stat_row(close_rate=2, change_code="HH")
    patch_diagnose(monkeypatch, row, ml=[9], dl=[100])
    result = diagnose(request_for(row))
    evidence = (
        f"실제 close_rate={result.get('close_rate')} ml={result.get('ml_close_rate')} "
        f"status={result.get('status')}"
    )
    note("AI03-009", evidence)
    assert result["status"] == "stable" and result["ml_close_rate"] == 9, evidence


def test_AI03_010(monkeypatch):
    row = stat_row(close_rate=1, change_code="HL", change_name="상권축소")
    patch_diagnose(monkeypatch, row, ml=[1])
    result = diagnose(request_for(row))
    evidence = f"상권축소 판정 close_rate=1 change=HL status={result.get('status')} is_danger={result.get('is_danger')}"
    note("AI03-010", evidence)
    assert result["status"] == "danger" and result["is_danger"] is True, evidence


def _passthrough(monkeypatch, **fields):
    row = stat_row(**fields)
    patch_diagnose(monkeypatch, row, ml=[1.5], dl=[80.0])
    return diagnose(request_for(row)), row


def test_AI03_011(monkeypatch):
    result, row = _passthrough(monkeypatch, quarter=20244)
    evidence = f"quarter 입력={row['quarter']} 출력={result.get('quarter')}"
    note("AI03-011", evidence)
    assert result["quarter"] == 20244, evidence


def test_AI03_012(monkeypatch):
    result, _row = _passthrough(monkeypatch, store_count=12)
    evidence = f"점포수 store_count={result.get('store_count')}"
    note("AI03-012", evidence)
    assert result["store_count"] == 12, evidence


def test_AI03_013(monkeypatch):
    result, _row = _passthrough(monkeypatch, open_rate=2.2)
    evidence = f"개업률 open_rate={result.get('open_rate')}"
    note("AI03-013", evidence)
    assert result["open_rate"] == 2.2, evidence


def test_AI03_014(monkeypatch):
    result, _row = _passthrough(monkeypatch, close_rate=3.2, change_code="HH")
    evidence = f"폐업률 close_rate={result.get('close_rate')}"
    note("AI03-014", evidence)
    assert result["close_rate"] == 3.2, evidence


def test_AI03_015(monkeypatch):
    result, _row = _passthrough(monkeypatch, foot_traffic=35000)
    evidence = f"유동인구 foot_traffic={result.get('foot_traffic')}"
    note("AI03-015", evidence)
    assert result["foot_traffic"] == 35000, evidence


def test_AI03_016(monkeypatch):
    result, _row = _passthrough(monkeypatch, change_name="상권축소", change_code="HL")
    evidence = f"change_name={result.get('change_name')}"
    note("AI03-016", evidence)
    assert result["change_name"] == "상권축소", evidence


def test_AI03_017(monkeypatch):
    result, _row = _passthrough(monkeypatch, franchise_ratio=0.15)
    evidence = f"가맹비율 franchise_ratio={result.get('franchise_ratio')}"
    note("AI03-017", evidence)
    assert result["franchise_ratio"] == 0.15, evidence


def test_AI03_018(monkeypatch):
    result, _row = _passthrough(monkeypatch, operate_months=50)
    evidence = f"운영개월 operate_months={result.get('operate_months')}"
    note("AI03-018", evidence)
    assert result["operate_months"] == 50, evidence


def test_AI03_019(monkeypatch):
    result, _row = _passthrough(monkeypatch, sales_per_store=700)
    evidence = f"점포당매출 sales_per_store={result.get('sales_per_store')}"
    note("AI03-019", evidence)
    assert result["sales_per_store"] == 700, evidence


def test_AI03_020(monkeypatch):
    row = stat_row()
    patch_diagnose(monkeypatch, row, explanation=("text", "basic"))
    result = diagnose(request_for(row))
    evidence = f"설명 출처 explanation={result.get('explanation')!r} source={result.get('explanation_source')!r}"
    note("AI03-020", evidence)
    assert result["explanation"] == "text" and result["explanation_source"] == "basic", evidence


def test_AI03_021(monkeypatch):
    row = stat_row(close_rate=6, change_code="HH", store_count=10, sales_per_store=100)
    patch_diagnose(monkeypatch, row, ml=[7], dl=[100], explanation=None)
    result = diagnose(request_for(row))
    text = result.get("explanation", "")
    evidence = f"explanation={text}"
    note("AI03-021", evidence)
    assert "6%" in text and "7%" in text, evidence


def test_AI03_022(monkeypatch):
    row = stat_row()
    patch_diagnose(monkeypatch, row, ml=[], dl=[100.0], explanation=("text", "basic"))
    try:
        result = diagnose(request_for(row))
        outcome = f"반환 keys={sorted(result)} error={result.get('error')}"
    except Exception as error:
        outcome = f"{type(error).__name__}: {error}"
    evidence = f"빈 예측목록 predict_ml=[] → {outcome}"
    note("AI03-022", evidence)
    assert not outcome.startswith("IndexError"), evidence
    assert "error" in outcome or outcome.startswith("ValueError") or outcome.startswith("RuntimeError"), evidence


def test_AI03_023(monkeypatch):
    row = stat_row()
    patch_diagnose(monkeypatch, row, ml=[1.0], dl=[float("nan")], explanation=("text", "basic"))
    result = diagnose(request_for(row))
    value = result.get("dl_sales_per_store")
    try:
        encoded = json.dumps(result, allow_nan=False)
        encoded_state = "json_ok"
    except ValueError as error:
        encoded = ""
        encoded_state = f"json_fail:{error}"
    evidence = f"비정상 매출 dl_sales_per_store={value!r} {encoded_state} snippet={encoded[:80]}"
    note("AI03-023", evidence)
    assert not (isinstance(value, float) and math.isnan(value)), evidence
    assert encoded_state == "json_ok", evidence


def test_AI03_024(monkeypatch):
    row = stat_row()

    def slow(_frame):
        time.sleep(2)
        return [1.0]

    patch_diagnose(monkeypatch, row, explanation=("text", "basic"))
    monkeypatch.setattr("src.service.predict_ml", slow)
    started = time.perf_counter()
    try:
        result = diagnose(request_for(row))
        error = result.get("error")
    except Exception as exc:
        result = None
        error = f"{type(exc).__name__}: {exc}"
    elapsed = time.perf_counter() - started
    evidence = f"predict_ml 2초 지연 elapsed={elapsed:.2f}s error={error!r}"
    note("AI03-024", evidence)
    assert elapsed < 0.5 or (error and any(token in str(error) for token in ("시간", "timeout", "Timeout", "제한"))), evidence


def test_AI03_025(monkeypatch):
    row = stat_row(close_rate=3.2, store_count=12)
    before = json.dumps(row, ensure_ascii=False, sort_keys=True)
    patch_diagnose(monkeypatch, row, ml=[2.5], dl=[80.0])
    first = diagnose(request_for(row))
    second = diagnose(request_for(row))
    after = json.dumps(row, ensure_ascii=False, sort_keys=True)
    comparable = {key: first[key] for key in first if key != "explanation"}
    comparable2 = {key: second[key] for key in second if key != "explanation"}
    evidence = (
        f"동일호출={comparable == comparable2} 원본불변={before == after} "
        f"status={first.get('status')} ml={first.get('ml_close_rate')}"
    )
    note("AI03-025", evidence)
    assert comparable == comparable2, evidence
    assert before == after, evidence
