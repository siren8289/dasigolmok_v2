"""AI02 행정동 통계·옵션 캐시."""
import json
import time

import pytest

from helpers import note
import src.dong_stats as ds


def _reset_rows():
    ds._rows = None


def test_AI02_001():
    _reset_rows()
    rows = ds.load_stats()
    evidence = f"통계 적재 type={type(rows).__name__} len={len(rows)} sample_keys={sorted(rows[0])[:6]}"
    note("AI02-001", evidence)
    assert isinstance(rows, list), evidence
    assert rows and isinstance(rows[0], dict), evidence


def test_AI02_002():
    ds._options = None
    options = ds.load_options()
    evidence = f"선택지 적재 type={type(options).__name__} keys={sorted(options)}"
    note("AI02-002", evidence)
    assert isinstance(options, dict), evidence
    assert {"districts", "dongs", "industries"} <= set(options), evidence


def test_AI02_003(tmp_path):
    saved = (ds._rows, ds.STATS_PATH)
    missing = tmp_path / "missing_dong_stats.json"
    ds._rows = None
    ds.STATS_PATH = missing
    try:
        with pytest.raises(FileNotFoundError) as caught:
            ds.load_stats()
        evidence = f"STATS_PATH 없음 → {type(caught.value).__name__}: {caught.value}"
        note("AI02-003", evidence)
        assert str(missing) in str(caught.value), evidence
    finally:
        ds._rows, ds.STATS_PATH = saved


def test_AI02_004(tmp_path):
    saved = (ds._options, ds.OPTIONS_PATH)
    missing = tmp_path / "missing_options.json"
    ds._options = None
    ds.OPTIONS_PATH = missing
    try:
        with pytest.raises(FileNotFoundError) as caught:
            ds.load_options()
        evidence = f"OPTIONS_PATH 없음 → {type(caught.value).__name__}: {caught.value}"
        note("AI02-004", evidence)
        assert str(missing) in str(caught.value), evidence
    finally:
        ds._options, ds.OPTIONS_PATH = saved


def test_AI02_005():
    saved_rows, saved_path = ds._rows, ds.STATS_PATH
    calls = {"n": 0}
    payload = saved_path.read_text(encoding="utf-8")

    class CountingPath:
        def read_text(self, encoding="utf-8"):
            calls["n"] += 1
            return payload

    ds._rows = None
    ds.STATS_PATH = CountingPath()
    try:
        first = ds.load_stats()
        second = ds.load_stats()
        evidence = f"load_stats 2회 read_text 호출={calls['n']} same_object={first is second} len={len(first)}"
        note("AI02-005", evidence)
        assert calls["n"] == 1, evidence
        assert first is second, evidence
    finally:
        ds._rows, ds.STATS_PATH = saved_rows, saved_path


def test_AI02_006():
    saved_opt, saved_path = ds._options, ds.OPTIONS_PATH
    calls = {"n": 0}
    payload = saved_path.read_text(encoding="utf-8")

    class CountingPath:
        def read_text(self, encoding="utf-8"):
            calls["n"] += 1
            return payload

    ds._options = None
    ds.OPTIONS_PATH = CountingPath()
    try:
        first = ds.load_options()
        second = ds.load_options()
        evidence = f"load_options 2회 read_text 호출={calls['n']} same_object={first is second}"
        note("AI02-006", evidence)
        assert calls["n"] == 1, evidence
        assert first is second, evidence
    finally:
        ds._options, ds.OPTIONS_PATH = saved_opt, saved_path


def test_AI02_007():
    row = ds.find_stat("연남동", "한식음식점")
    matches = [
        item for item in ds.load_stats()
        if item["dong"] == "연남동" and item["industry"] == "한식음식점"
    ]
    evidence = (
        f"find_stat(연남동,한식음식점) district={None if row is None else row.get('district')} "
        f"industry={None if row is None else row.get('industry')} matches={len(matches)}"
    )
    note("AI02-007", evidence)
    assert row is not None and len(matches) == 1, evidence
    assert row["dong"] == "연남동" and row["industry"] == "한식음식점", evidence
    assert row["quarter"] == matches[0]["quarter"] and row["close_rate"] == matches[0]["close_rate"], evidence


def test_AI02_008():
    target = ds.find_stat("연남동", "한식음식점")
    other = ds.find_stat("연남동", "PC방")
    evidence = (
        f"한식={None if target is None else target.get('industry')} "
        f"PC방={None if other is None else other.get('industry')}"
    )
    note("AI02-008", evidence)
    assert target is not None and other is not None, evidence
    assert target["industry"] == "한식음식점" and other["industry"] == "PC방", evidence
    assert target is not other, evidence


def test_AI02_009():
    yeonnam = ds.find_stat("연남동", "한식음식점")
    yeoksam = ds.find_stat("역삼1동", "한식음식점")
    evidence = (
        f"연남동 district={yeonnam.get('district')} 역삼1동 district={yeoksam.get('district')}"
    )
    note("AI02-009", evidence)
    assert yeonnam["dong"] == "연남동" and yeoksam["dong"] == "역삼1동", evidence
    assert yeonnam["district"] != yeoksam["district"], evidence


def test_AI02_010():
    found = ds.find_stat("없는동", "한식음식점")
    rows = ds.industries_in_dong("없는동")
    evidence = f"없는 동 조회 find_stat={found!r} industries_in_dong={rows!r}"
    note("AI02-010", evidence)
    assert found is None, evidence
    assert rows == [], evidence


def test_AI02_011():
    rows = ds.industries_in_dong("연남동")
    expected = [item for item in ds.load_stats() if item["dong"] == "연남동"]
    evidence = f"industries_in_dong('연남동')={len(rows)} 전체필터={len(expected)} districts={sorted({r['district'] for r in rows})}"
    note("AI02-011", evidence)
    assert len(rows) == len(expected) and len(rows) > 0, evidence
    assert all(item["dong"] == "연남동" for item in rows), evidence


def test_AI02_012():
    exact = ds.find_stat("연남동", "한식음식점")
    padded = ds.find_stat(" 연남동 ", "한식음식점")
    padded_industry = ds.find_stat("연남동", " 한식음식점 ")
    evidence = (
        f"exact={'있음' if exact else '없음'} "
        f"dong=' 연남동 ' → {padded!r} industry=' 한식음식점 ' → {padded_industry!r}"
    )
    note("AI02-012", evidence)
    assert padded is not None and padded.get("dong") == "연남동", evidence
    assert padded_industry is not None, evidence


def test_AI02_013():
    rows = ds.industries_in_dong("신사동")
    districts = sorted({row["district"] for row in rows})
    evidence = f"industries_in_dong('신사동') rows={len(rows)} districts={districts}"
    note("AI02-013", evidence)
    assert len(districts) == 1, evidence


def test_AI02_014():
    saved = ds._rows
    older = {
        "dong": "테스트동",
        "industry": "테스트업종",
        "district": "마포구",
        "quarter": 20231,
        "close_rate": 1.0,
    }
    newer = {
        "dong": "테스트동",
        "industry": "테스트업종",
        "district": "마포구",
        "quarter": 20244,
        "close_rate": 9.0,
    }
    ds._rows = [older, newer]
    try:
        found = ds.find_stat("테스트동", "테스트업종")
        evidence = f"복수 quarter 조회 결과 quarter={found.get('quarter')} close_rate={found.get('close_rate')}"
        note("AI02-014", evidence)
        assert found["quarter"] == 20244 and found["close_rate"] == 9.0, evidence
    finally:
        ds._rows = saved


def test_AI02_015():
    saved = ds._rows
    rows = [
        {"dong": f"d{i % 1000}", "industry": f"i{i % 50}", "quarter": 1}
        for i in range(500_000)
    ]
    ds._rows = rows
    try:
        started = time.perf_counter()
        for _ in range(20):
            found = ds.find_stat("없는동-대용량", "없는업종")
        elapsed = time.perf_counter() - started
        evidence = (
            f"50만 행 미존재 키 20회 elapsed={elapsed:.3f}s "
            f"회당={elapsed / 20 * 1000:.1f}ms 결과={found!r} 인덱스없음"
        )
        note("AI02-015", evidence)
        assert found is None, evidence
        assert elapsed < 0.05, evidence
    finally:
        ds._rows = saved


def test_AI02_016():
    saved = ds._rows
    ds._rows = [{"dong": "연남동"}]
    try:
        with pytest.raises(KeyError) as caught:
            ds.find_stat("연남동", "한식음식점")
        evidence = f"industry 누락 행 → {type(caught.value).__name__}: {caught.value}"
        note("AI02-016", evidence)
        assert "industry" in str(caught.value), evidence
    finally:
        ds._rows = saved


def test_AI02_017():
    saved = ds._rows
    ds._rows = {"dong": "연남동", "industry": "한식음식점"}
    try:
        try:
            found = ds.find_stat("연남동", "한식음식점")
            outcome = f"반환={found!r}"
        except ValueError as error:
            outcome = f"ValueError: {error}"
        except Exception as error:
            outcome = f"{type(error).__name__}: {error}"
        evidence = f"통계 최상위 dict 조회 결과 {outcome}"
        note("AI02-017", evidence)
        assert outcome.startswith("ValueError"), evidence
        assert any(token in outcome for token in ("list", "구조", "형식", "배열")), evidence
    finally:
        ds._rows = saved


def test_AI02_018(tmp_path):
    saved = (ds._options, ds.OPTIONS_PATH)
    path = tmp_path / "options.json"
    path.write_text(json.dumps({"districts": ["A"], "dongs": [], "industries": []}), encoding="utf-8")
    ds._options = None
    ds.OPTIONS_PATH = path
    try:
        first = ds.load_options()
        path.write_text(json.dumps({"districts": ["B"], "dongs": [], "industries": []}), encoding="utf-8")
        second = ds.load_options()
        evidence = f"캐시 후 파일 변경 first={first.get('districts')} second={second.get('districts')}"
        note("AI02-018", evidence)
        assert second.get("districts") == ["B"], evidence
    finally:
        ds._options, ds.OPTIONS_PATH = saved
