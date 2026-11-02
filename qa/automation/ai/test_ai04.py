"""AI04 행정동 업종 추천."""
from concurrent.futures import ThreadPoolExecutor

from helpers import note, patch_recommend, stat_row
from src.service import recommend
import src.dong_stats as ds


def _rows(n, **common):
    rows = []
    for index in range(n):
        rows.append(stat_row(industry=f"업종{index}", **common))
    return rows


def test_AI04_001(monkeypatch):
    rows = _rows(7)
    capture = {}
    patch_recommend(monkeypatch, rows, [1] * 7, [100] * 7, capture)
    result = recommend({"district": "마포구", "dong": "연남동"})
    evidence = (
        f"입력=7 ml_rows={capture.get('ml_rows')} dl_rows={capture.get('dl_rows')} "
        f"all={len(result.get('all_industries', []))} rec={len(result.get('recommendations', []))}"
    )
    note("AI04-001", evidence)
    assert capture.get("ml_rows") == 7 and capture.get("dl_rows") == 7, evidence
    assert len(result["all_industries"]) == 7, evidence


def test_AI04_002(monkeypatch):
    patch_recommend(monkeypatch, [], [], [])
    result = recommend({"district": "마포구", "dong": "없는동"})
    evidence = f"빈 동 결과={result}"
    note("AI04-002", evidence)
    assert result.get("error") and result.get("recommendations") == [], evidence


def test_AI04_003(monkeypatch):
    rows = _rows(3)
    capture = {}
    patch_recommend(monkeypatch, rows, [1, 2, 3], [10, 20, 30], capture)
    recommend({"district": "마포구", "dong": "연남동"})
    frame = capture["ml_frame"]
    evidence = f"ML/DL 입력 shape={tuple(frame.shape)} columns={list(frame.columns)}"
    note("AI04-003", evidence)
    assert frame.shape[0] == 3 and capture["dl_rows"] == 3, evidence


def test_AI04_004(monkeypatch):
    rows = _rows(3)
    patch_recommend(monkeypatch, rows, [3, 5, 8], [100, 100, 100])
    result = recommend({"district": "마포구", "dong": "연남동"})
    mapped = {item["industry"]: item["ml_close_rate"] for item in result["all_industries"]}
    evidence = f"ML 매핑={mapped}"
    note("AI04-004", evidence)
    assert mapped == {"업종0": 3, "업종1": 5, "업종2": 8}, evidence


def test_AI04_005(monkeypatch):
    rows = _rows(3)
    patch_recommend(monkeypatch, rows, [1, 1, 1], [1000, 800, 600])
    result = recommend({"district": "마포구", "dong": "연남동"})
    mapped = {item["industry"]: item["dl_sales_per_store"] for item in result["all_industries"]}
    evidence = f"DL 매핑={mapped}"
    note("AI04-005", evidence)
    assert mapped == {"업종0": 1000, "업종1": 800, "업종2": 600}, evidence


def test_AI04_006(monkeypatch):
    rows = _rows(1)
    patch_recommend(monkeypatch, rows, [3], [1000])
    result = recommend({"district": "마포구", "dong": "연남동"})
    score = result["all_industries"][0]["score"]
    evidence = f"sales=1000 close=3 score={score} 기대=-14.0"
    note("AI04-006", evidence)
    assert score == -14.0, evidence


def test_AI04_007(monkeypatch):
    rows = _rows(1)
    patch_recommend(monkeypatch, rows, [1], [1500])
    result = recommend({"district": "마포구", "dong": "연남동"})
    score = result["all_industries"][0]["score"]
    evidence = f"sales=1500 close=1 score={score} 기대=7.0"
    note("AI04-007", evidence)
    assert score == 7.0, evidence


def test_AI04_008(monkeypatch):
    rows = _rows(1)
    patch_recommend(monkeypatch, rows, [0], [0])
    result = recommend({"district": "마포구", "dong": "연남동"})
    score = result["all_industries"][0]["score"]
    evidence = f"영 입력 점수 sales=0 close=0 score={score}"
    note("AI04-008", evidence)
    assert score == 0.0, evidence


def test_AI04_009(monkeypatch):
    rows = _rows(1)
    patch_recommend(monkeypatch, rows, [3.33], [999.5])
    result = recommend({"district": "마포구", "dong": "연남동"})
    score = result["all_industries"][0]["score"]
    evidence = f"소수 반올림 sales=999.5 close=3.33 score={score} round1={round(999.5 / 100 - 3.33 * 8, 1)}"
    note("AI04-009", evidence)
    assert score == round(999.5 / 100 - 3.33 * 8, 1) == -16.6, evidence


def test_AI04_010(monkeypatch):
    rows = _rows(3)
    patch_recommend(monkeypatch, rows, [0, 0, 0], [900, 100, 500])
    result = recommend({"district": "마포구", "dong": "연남동"})
    scores = [item["score"] for item in result["all_industries"]]
    evidence = f"입력 score 대응 sales 900/100/500 → 정렬 {scores}"
    note("AI04-010", evidence)
    assert scores == [9.0, 5.0, 1.0], evidence


def test_AI04_011(monkeypatch):
    rows = _rows(7)
    patch_recommend(monkeypatch, rows, list(range(7)), [100] * 7)
    result = recommend({"district": "마포구", "dong": "연남동"})
    evidence = f"추천 건수 recommendations={len(result['recommendations'])} all={len(result['all_industries'])}"
    note("AI04-011", evidence)
    assert len(result["recommendations"]) == 5, evidence


def test_AI04_012(monkeypatch):
    rows = _rows(7)
    patch_recommend(monkeypatch, rows, [1] * 7, [100] * 7)
    result = recommend({"district": "마포구", "dong": "연남동"})
    evidence = f"전체 업종 수 all_industries={len(result['all_industries'])}"
    note("AI04-012", evidence)
    assert len(result["all_industries"]) == 7, evidence


def test_AI04_013(monkeypatch):
    rows = _rows(1)
    patch_recommend(monkeypatch, rows, [1], [100])
    result = recommend({"district": "마포구", "dong": "연남동"})
    evidence = f"추천과 전체 rec={len(result['recommendations'])} all={len(result['all_industries'])}"
    note("AI04-013", evidence)
    assert len(result["recommendations"]) == 1 and len(result["all_industries"]) == 1, evidence


def test_AI04_014(monkeypatch):
    rows = _rows(5)
    patch_recommend(monkeypatch, rows, [1] * 5, [100] * 5)
    result = recommend({"district": "마포구", "dong": "연남동"})
    evidence = f"기본 상한 rec={len(result['recommendations'])}"
    note("AI04-014", evidence)
    assert len(result["recommendations"]) == 5, evidence


def test_AI04_015(monkeypatch):
    rows = _rows(6)
    patch_recommend(monkeypatch, rows, [1] * 6, [100] * 6)
    result = recommend({"district": "마포구", "dong": "연남동"})
    evidence = f"추천과 전체 rec={len(result['recommendations'])} all={len(result['all_industries'])}"
    note("AI04-015", evidence)
    assert len(result["recommendations"]) == 5 and len(result["all_industries"]) == 6, evidence


def test_AI04_016(monkeypatch):
    rows = [stat_row(close_rate=1, change_code="HH")]
    patch_recommend(monkeypatch, rows, [9], [100])
    result = recommend({"district": "마포구", "dong": "연남동"})
    item = result["all_industries"][0]
    evidence = f"실제 close_rate={item['close_rate']} ml={item['ml_close_rate']} status={item['status']}"
    note("AI04-016", evidence)
    assert item["status"] == "danger" and item["is_danger"] is True, evidence
    assert item["close_rate"] == 1 and item["ml_close_rate"] == 9, evidence


def test_AI04_017(monkeypatch):
    rows = [stat_row(close_rate=2.3)]
    patch_recommend(monkeypatch, rows, [1], [100])
    result = recommend({"district": "마포구", "dong": "연남동"})
    value = result["all_industries"][0]["close_rate"]
    evidence = f"반환 폐업률 close_rate={value}"
    note("AI04-017", evidence)
    assert value == 2.3, evidence


def test_AI04_018(monkeypatch):
    rows = [stat_row(change_code="HL", change_name="상권축소", close_rate=1)]
    patch_recommend(monkeypatch, rows, [1], [100])
    result = recommend({"district": "마포구", "dong": "연남동"})
    item = result["all_industries"][0]
    evidence = f"축소 상권 판정 change=HL ml={item['ml_close_rate']} status={item['status']}"
    note("AI04-018", evidence)
    assert item["status"] == "danger" and item["is_danger"] is True, evidence


def test_AI04_019(monkeypatch):
    rows = [
        stat_row(industry="낮음", change_name="첫변화"),
        stat_row(industry="높음", change_name="둘째변화"),
    ]
    patch_recommend(monkeypatch, rows, [0, 0], [10, 900])
    result = recommend({"district": "마포구", "dong": "연남동"})
    evidence = (
        f"반환 change_name={result.get('change_name')!r} "
        f"추천1={result['recommendations'][0]['industry']}"
    )
    note("AI04-019", evidence)
    assert result["change_name"] == "첫변화", evidence


def test_AI04_020(monkeypatch):
    rows = [
        stat_row(industry="C"),
        stat_row(industry="A"),
        stat_row(industry="B"),
    ]
    patch_recommend(monkeypatch, rows, [0, 0, 0], [100, 900, 500])
    result = recommend({"district": "마포구", "dong": "연남동"})
    order = [(item["industry"], item["score"]) for item in result["all_industries"]]
    evidence = f"정렬={order}"
    note("AI04-020", evidence)
    assert [name for name, _score in order] == ["A", "B", "C"], evidence
    assert [score for _name, score in order] == sorted((score for _name, score in order), reverse=True), evidence


def test_AI04_021(monkeypatch):
    rows = _rows(3)
    patch_recommend(monkeypatch, rows, [3, 5], [100, 100, 100])
    try:
        result = recommend({"district": "마포구", "dong": "연남동"})
        outcome = (
            f"error={result.get('error')} all={len(result.get('all_industries', []))} "
            f"industries={[item['industry'] for item in result.get('all_industries', [])]}"
        )
    except Exception as error:
        outcome = f"{type(error).__name__}: {error}"
    evidence = f"3행·ML 2개 → {outcome}"
    note("AI04-021", evidence)
    assert outcome.startswith(("ValueError", "RuntimeError")) or (
        "error=" in outcome and "all=3" in outcome and not outcome.startswith("error=None")
    ), evidence


def test_AI04_022(monkeypatch):
    rows = _rows(1)
    patch_recommend(monkeypatch, rows, [1], [-50])
    try:
        result = recommend({"district": "마포구", "dong": "연남동"})
        item = result["all_industries"][0]
        outcome = f"sales={item['dl_sales_per_store']} score={item['score']} error={result.get('error')}"
    except Exception as error:
        outcome = f"{type(error).__name__}: {error}"
        item = None
    evidence = f"예측 sales=-50 → {outcome}"
    note("AI04-022", evidence)
    assert item is None or item["dl_sales_per_store"] >= 0 or result.get("error"), evidence


def test_AI04_023():
    rows = [row for row in ds.load_stats() if row["dong"] == "신사동"]
    only_gwanak = {row["industry"] for row in rows if row["district"] == "관악구"} - {
        row["industry"] for row in rows if row["district"] == "강남구"
    }
    result = recommend({"district": "강남구", "dong": "신사동"})
    leaked = sorted(only_gwanak.intersection(item["industry"] for item in result.get("all_industries", [])))
    evidence = (
        f"요청 district=강남구 반환 district={result.get('district')} "
        f"관악구전용업종유입={leaked} all={len(result.get('all_industries', []))}"
    )
    note("AI04-023", evidence)
    assert result.get("district") == "강남구", evidence
    assert leaked == [], evidence


def test_AI04_024(monkeypatch):
    rows = _rows(3)
    patch_recommend(monkeypatch, rows, [1, 2, 3], [100, 200, 300])
    result = recommend({"district": "마포구", "dong": "연남동"}, limit=0)
    evidence = f"상한 0건 rec={result['recommendations']} all={len(result['all_industries'])}"
    note("AI04-024", evidence)
    assert result["recommendations"] == [] and len(result["all_industries"]) == 3, evidence


def test_AI04_025(monkeypatch):
    rows = _rows(3)
    patch_recommend(monkeypatch, rows, [1, 2, 3], [300, 200, 100])
    try:
        result = recommend({"district": "마포구", "dong": "연남동"}, limit=-1)
        rec = [item["industry"] for item in result["recommendations"]]
        whole = [item["industry"] for item in result["all_industries"]]
        outcome = f"error={result.get('error')} rec={rec} all={whole}"
    except ValueError as error:
        outcome = f"ValueError: {error}"
        rec, whole = None, None
    evidence = f"limit=-1 → {outcome}"
    note("AI04-025", evidence)
    dropped_last = rec is not None and whole is not None and len(whole) > 1 and rec == whole[:-1]
    assert not dropped_last, evidence
    assert outcome.startswith("ValueError") or rec in ([], whole), evidence


def test_AI04_026(monkeypatch):
    rows = _rows(4)
    patch_recommend(monkeypatch, rows, [1, 2, 3, 4], [10, 20, 30, 40])
    result = recommend({"district": "마포구", "dong": "연남동"}, limit=10000)
    evidence = f"추천과 전체 rec={len(result['recommendations'])} all={len(result['all_industries'])}"
    note("AI04-026", evidence)
    assert len(result["recommendations"]) == len(result["all_industries"]) == 4, evidence


def test_AI04_027():
    def once(dong):
        return recommend({"district": "무시", "dong": dong})

    sequential = [once("연남동"), once("역삼1동")]
    with ThreadPoolExecutor(max_workers=2) as pool:
        parallel = list(pool.map(once, ["연남동", "역삼1동"]))
    evidence = (
        f"병렬 dong={[item.get('dong') for item in parallel]} "
        f"district={[item.get('district') for item in parallel]} "
        f"순차와동일={ [item.get('all_industries') for item in parallel] == [item.get('all_industries') for item in sequential] }"
    )
    note("AI04-027", evidence)
    assert [item.get("dong") for item in parallel] == ["연남동", "역삼1동"], evidence
    assert [item.get("district") for item in parallel] == ["마포구", "강남구"], evidence
    assert [item["industry"] for item in parallel[0]["all_industries"]] == [
        item["industry"] for item in sequential[0]["all_industries"]
    ], evidence
    assert [item["industry"] for item in parallel[1]["all_industries"]] == [
        item["industry"] for item in sequential[1]["all_industries"]
    ], evidence
