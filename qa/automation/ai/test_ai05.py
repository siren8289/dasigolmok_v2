"""AI05 classify 규칙·경계."""
import math

from helpers import note, patch_diagnose, patch_recommend, request_for, stat_row
from src.risk import classify
from src.service import diagnose, recommend


def _expect(case_id, close_rate, change_code, status, danger):
    observed = classify(close_rate, change_code)
    evidence = f"classify({close_rate!r},{change_code!r})={observed} 기대=({status!r},{danger!r})"
    note(case_id, evidence)
    assert observed == (status, danger), evidence


def test_AI05_001():
    _expect("AI05-001", 3.99, "HH", "stable", False)


def test_AI05_002():
    _expect("AI05-002", 4.00, "HH", "warning", False)


def test_AI05_003():
    _expect("AI05-003", 4.01, "HH", "warning", False)


def test_AI05_004():
    _expect("AI05-004", 7.99, "HH", "warning", False)


def test_AI05_005():
    _expect("AI05-005", 8.00, "HH", "danger", True)


def test_AI05_006():
    _expect("AI05-006", 8.01, "HH", "danger", True)


def test_AI05_007():
    _expect("AI05-007", 0, "HH", "stable", False)


def test_AI05_008():
    _expect("AI05-008", 2, "HL", "danger", True)


def test_AI05_009():
    _expect("AI05-009", 4, "HL", "danger", True)


def test_AI05_010():
    _expect("AI05-010", 9, "HL", "danger", True)


def test_AI05_011():
    _expect("AI05-011", 2, "LL", "warning", False)


def test_AI05_012():
    _expect("AI05-012", 8, "LL", "danger", True)


def test_AI05_013():
    _expect("AI05-013", 2, "LH", "stable", False)


def test_AI05_014():
    _expect("AI05-014", 8, "LH", "danger", True)


def test_AI05_015():
    _expect("AI05-015", None, "HL", "unknown", False)


def test_AI05_016():
    _expect("AI05-016", 2, "XX", "stable", False)


def test_AI05_017():
    try:
        observed = classify(-1, "HH")
    except ValueError as error:
        observed = f"ValueError: {error}"
    evidence = f"classify(-1,'HH')={observed!r} (기대: 범위 오류)"
    note("AI05-017", evidence)
    assert isinstance(observed, str) and observed.startswith("ValueError"), evidence


def test_AI05_018():
    try:
        observed = classify(120, "HH")
    except ValueError as error:
        observed = f"ValueError: {error}"
    evidence = f"classify(120,'HH')={observed!r} (기대: 100% 초과 오류)"
    note("AI05-018", evidence)
    assert isinstance(observed, str) and observed.startswith("ValueError"), evidence


def test_AI05_019():
    try:
        observed = classify("5", "HH")
    except (TypeError, ValueError) as error:
        observed = f"{type(error).__name__}: {error}"
    evidence = f"문자열 폐업률 classify('5','HH')={observed!r}"
    note("AI05-019", evidence)
    assert isinstance(observed, str) and observed.split(":", 1)[0] in ("TypeError", "ValueError"), evidence


def test_AI05_020():
    try:
        observed = classify(float("nan"), "HH")
    except ValueError as error:
        observed = f"ValueError: {error}"
    evidence = f"결측 폐업률 classify(nan,'HH')={observed!r}"
    note("AI05-020", evidence)
    assert observed == ("unknown", False) or (
        isinstance(observed, str) and observed.startswith("ValueError")
    ), evidence
    if isinstance(observed, tuple):
        assert observed[0] == "unknown" and observed[1] is False, evidence
        assert not math.isnan(observed[0]) if isinstance(observed[0], float) else True


def test_AI05_021():
    _expect("AI05-021", 4, "HH", "warning", False)


def test_AI05_022():
    _expect("AI05-022", 3.999999, "HH", "stable", False)


def test_AI05_023(monkeypatch):
    row = stat_row(close_rate=2, change_code="HH", change_name="정체")
    patch_diagnose(monkeypatch, row, ml=[10], dl=[100], explanation=("text", "basic"))
    diagnosed = diagnose(request_for(row))
    patch_recommend(monkeypatch, [row], [10], [100])
    recommended = recommend({"district": row["district"], "dong": row["dong"]})
    item = recommended["all_industries"][0]
    evidence = (
        f"진단 status={diagnosed.get('status')} close_rate={diagnosed.get('close_rate')} "
        f"ml={diagnosed.get('ml_close_rate')} / 추천 status={item.get('status')} "
        f"close_rate={item.get('close_rate')} ml={item.get('ml_close_rate')}"
    )
    note("AI05-023", evidence)
    assert diagnosed["status"] == "stable" and diagnosed["close_rate"] == 2, evidence
    assert item["status"] == "danger" and item["ml_close_rate"] == 10, evidence
    assert item["close_rate"] == 2, evidence
