"""DE08 ETL 실행·저장. 외부 API와 실제 data/raw·processed 는 쓰지 않는다."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

from data.etl import load, run as etl_run
from data.etl.load import save_json, save_processed


ROOT = Path(__file__).resolve().parents[3]


def _raw_store(**overrides):
    base = {
        "기준_년분기_코드": "20242",
        "행정동_코드": "11440740",
        "행정동_코드_명": "연남동",
        "서비스_업종_코드": "CS100001",
        "서비스_업종_코드_명": "한식음식점",
        "점포_수": "10",
        "개업_율": "3.20",
        "개업_점포_수": "1",
        "폐업_률": "2",
        "폐업_점포_수": "1",
        "프랜차이즈_점포_수": "2",
    }
    base.update(overrides)
    return base


def _raw_sales(**overrides):
    base = {
        "기준_년분기_코드": "20242",
        "행정동_코드": "11440740",
        "행정동_코드_명": "연남동",
        "서비스_업종_코드": "CS100001",
        "서비스_업종_코드_명": "한식음식점",
        "당월_매출_금액": "100000000",
        "당월_매출_건수": "3000",
    }
    base.update(overrides)
    return base


def _raw_pop(**overrides):
    base = {
        "기준_년분기_코드": "20242",
        "행정동_코드": "11440740",
        "행정동_코드_명": "연남동",
        "총_유동인구_수": "50000",
    }
    base.update(overrides)
    return base


def _raw_change(**overrides):
    base = {
        "기준_년분기_코드": "20242",
        "행정동_코드": "11440740",
        "행정동_코드_명": "연남동",
        "상권_변화_지표": "HH",
        "상권_변화_지표_명": "정체",
        "운영_영업_개월_평균": "15.5",
    }
    base.update(overrides)
    return base


def _tables():
    return {
        "store": pd.DataFrame([_raw_store()]),
        "sales": pd.DataFrame([_raw_sales()]),
        "pop": pd.DataFrame([_raw_pop()]),
        "change": pd.DataFrame([_raw_change()]),
    }


def _use_tmp(monkeypatch, tmp_path):
    raw = tmp_path / "raw"
    processed = tmp_path / "processed"
    raw.mkdir()
    processed.mkdir()
    monkeypatch.setattr(load, "RAW_DIR", raw)
    monkeypatch.setattr(load, "PROCESSED_DIR", processed)
    return raw, processed


def _patch_sources(monkeypatch, tables, fetch_log=None):
    def fake_fetch(key):
        if fetch_log is not None:
            fetch_log.append(key)
        table = tables[key]
        if isinstance(table, Exception):
            raise table
        return table.copy()

    monkeypatch.setattr(etl_run, "fetch_seoul_table", fake_fetch)
    monkeypatch.setattr(etl_run, "fetch_semas_upjong", lambda: ([{"name": "음식"}], [{"name": "한식"}]))
    monkeypatch.setattr(etl_run, "fetch_semas_dongs", lambda: [{"ctyNm": "마포구"}])
    monkeypatch.setattr(etl_run, "fetch_semas_stores", lambda *args, **kwargs: [{"bizesNm": "테스트가게"}])


def test_DE08_001(monkeypatch, tmp_path, capsys):
    _use_tmp(monkeypatch, tmp_path)
    _patch_sources(monkeypatch, _tables())
    etl_run.run(skip_download=False)
    out = capsys.readouterr().out
    assert "[1/3] 수집" in out
    assert "[2/3] 전처리" in out
    assert "[3/3] 저장" in out


def test_DE08_002(monkeypatch, tmp_path, capsys):
    raw, _processed = _use_tmp(monkeypatch, tmp_path)
    tables = _tables()
    for name, frame in tables.items():
        frame.to_csv(raw / f"{name}.csv", index=False)
    fetch_log = []
    _patch_sources(monkeypatch, tables, fetch_log)
    etl_run.run(skip_download=True)
    out = capsys.readouterr().out
    assert fetch_log == []
    assert out.count("캐시 사용") == 4


def test_DE08_003(monkeypatch, tmp_path):
    _use_tmp(monkeypatch, tmp_path)
    fetch_log = []
    _patch_sources(monkeypatch, _tables(), fetch_log)
    etl_run.run(skip_download=True)
    assert fetch_log == ["store", "sales", "pop", "change"]


def test_DE08_004(monkeypatch, tmp_path, capsys):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    _patch_sources(monkeypatch, _tables())

    def boom():
        raise RuntimeError("semas down")

    monkeypatch.setattr(etl_run, "fetch_semas_upjong", boom)
    etl_run.run(skip_download=False)
    out = capsys.readouterr().out
    options = json.loads((processed / "options.json").read_text(encoding="utf-8"))
    assert "건너뜁니다" in out
    assert options["semas_dong_count"] == 0
    assert options["semas_upjong_count"] == 0
    assert "[3/3] 저장" in out


def test_DE08_005(monkeypatch, tmp_path, capsys):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    tables = _tables()
    tables["store"] = RuntimeError("store download failed")
    _patch_sources(monkeypatch, tables)
    with pytest.raises(RuntimeError):
        etl_run.run(skip_download=False)
    out = capsys.readouterr().out
    assert "실패" in out or "오류" in out
    assert not (processed / "train.csv").exists()


def test_DE08_006(monkeypatch, tmp_path):
    raw, processed = _use_tmp(monkeypatch, tmp_path)
    tables = _tables()
    tables["sales"] = RuntimeError("sales download failed")
    _patch_sources(monkeypatch, tables)
    with pytest.raises(RuntimeError):
        etl_run.run(skip_download=False)
    assert (raw / "store.csv").exists()
    assert not (processed / "train.csv").exists()
    assert not (processed / "dong_stats.csv").exists()
    assert not (processed / "options.json").exists()


def test_DE08_007(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    tables = _tables()
    tables["pop"] = RuntimeError("유동인구 수집 실패")
    _patch_sources(monkeypatch, tables)
    with pytest.raises(RuntimeError) as caught:
        etl_run.run(skip_download=False)
    assert "유동인구" in str(caught.value)
    assert not (processed / "train.csv").exists()


def test_DE08_008(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    tables = _tables()
    tables["change"] = RuntimeError("상권변화 수집 실패")
    _patch_sources(monkeypatch, tables)
    with pytest.raises(RuntimeError) as caught:
        etl_run.run(skip_download=False)
    assert "상권변화" in str(caught.value)
    assert not (processed / "options.json").exists()


def test_DE08_009(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    _patch_sources(monkeypatch, _tables())
    etl_run.run(skip_download=False)
    train = pd.read_csv(processed / "train.csv")
    assert len(train) >= 1
    assert "sales_per_store" in train.columns


def test_DE08_010(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    _patch_sources(monkeypatch, _tables())
    etl_run.run(skip_download=False)
    stats = pd.read_csv(processed / "dong_stats.csv")
    assert len(stats) >= 1
    assert "median_close_rate" in stats.columns


def test_DE08_011(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    _patch_sources(monkeypatch, _tables())
    etl_run.run(skip_download=False)
    options = json.loads((processed / "options.json").read_text(encoding="utf-8"))
    assert "districts" in options and "dongs" in options and "industries" in options


def test_DE08_012(monkeypatch, tmp_path):
    raw, _processed = _use_tmp(monkeypatch, tmp_path)
    _patch_sources(monkeypatch, _tables())
    etl_run.run(skip_download=False)
    for name in ("store", "sales", "pop", "change"):
        assert (raw / f"{name}.csv").exists()
        assert (raw / f"{name}.csv").stat().st_size > 0


def test_DE08_013(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    tables = _tables()
    tables["sales"] = pd.DataFrame(columns=list(_raw_sales().keys()))
    _patch_sources(monkeypatch, tables)
    with pytest.raises(Exception) as caught:
        etl_run.run(skip_download=False)
    assert "품질" in str(caught.value) or "빈" in str(caught.value) or "sales" in str(caught.value).lower()
    assert not (processed / "train.csv").exists()


def test_DE08_014(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    stores = []
    sales = []
    for code, name in (("A", "한식"), ("B", "카페"), ("C", "분식")):
        stores.append(_raw_store(기준_년분기_코드="20241", 서비스_업종_코드=code, 서비스_업종_코드_명=name))
    stores.append(_raw_store(기준_년분기_코드="20242", 서비스_업종_코드="A", 서비스_업종_코드_명="한식"))
    for row in stores:
        sales.append(
            _raw_sales(
                기준_년분기_코드=row["기준_년분기_코드"],
                서비스_업종_코드=row["서비스_업종_코드"],
                서비스_업종_코드_명=row["서비스_업종_코드_명"],
            )
        )
    tables = _tables()
    tables["store"] = pd.DataFrame(stores)
    tables["sales"] = pd.DataFrame(sales)
    tables["pop"] = pd.DataFrame([_raw_pop(기준_년분기_코드="20241"), _raw_pop(기준_년분기_코드="20242")])
    tables["change"] = pd.DataFrame(
        [_raw_change(기준_년분기_코드="20241"), _raw_change(기준_년분기_코드="20242")]
    )
    _patch_sources(monkeypatch, tables)
    etl_run.run(skip_download=False)
    stats = pd.read_csv(processed / "dong_stats.csv", dtype={"quarter": str})
    quarters = set(stats["quarter"].astype(str))
    assert quarters == {"20241"} or "partial" in stats.columns or "coverage" in stats.columns, (
        f"최신 분기 일부만 있는데 선택 분기={quarters} rows={len(stats)}"
    )


def test_DE08_015(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    _patch_sources(monkeypatch, _tables())
    etl_run.run(skip_download=False)
    blob = (processed / "options.json").read_bytes()
    text = blob.decode("utf-8")
    assert "연남동" in text
    assert "\\u" not in text


def test_DE08_016(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    processed.chmod(0o555)
    try:
        with pytest.raises(PermissionError) as caught:
            save_processed(pd.DataFrame([{"a": 1}]), "train")
        assert "Permission" in type(caught.value).__name__ or "train" in str(caught.value)
        assert not (processed / "train.csv").exists()
    finally:
        processed.chmod(0o755)


def test_DE08_017(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    target = processed / "train.csv"
    target.write_text("GOOD\n", encoding="utf-8")

    def crash(self, path_or_buf, *args, **kwargs):
        Path(path_or_buf).write_text("PARTIAL", encoding="utf-8")
        raise RuntimeError("crash during write")

    monkeypatch.setattr(pd.DataFrame, "to_csv", crash)
    with pytest.raises(RuntimeError):
        save_processed(pd.DataFrame([{"a": 1}]), "train")
    assert target.read_text(encoding="utf-8") == "GOOD\n"


def test_DE08_018(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    tables = _tables()
    tables["store"] = pd.DataFrame([_raw_store(서비스_업종_코드_명="QA동기화업종")])
    tables["sales"] = pd.DataFrame([_raw_sales(서비스_업종_코드_명="QA동기화업종")])
    _patch_sources(monkeypatch, tables)
    etl_run.run(skip_download=False)
    model_options = ROOT / "ai" / "models" / "options.json"
    before = model_options.read_text(encoding="utf-8")
    assert "QA동기화업종" in before or "QA동기화업종" in (processed / "options.json").read_text(encoding="utf-8")
    assert "QA동기화업종" in before, "processed/options.json 만 갱신되고 ai/models/options.json 은 그대로"


def test_DE08_019(monkeypatch, tmp_path):
    raw, processed = _use_tmp(monkeypatch, tmp_path)
    tables = _tables()
    _patch_sources(monkeypatch, tables)
    etl_run.run(skip_download=False)
    first = (processed / "train.csv").read_bytes()
    for name, frame in tables.items():
        frame.to_csv(raw / f"{name}.csv", index=False)
    etl_run.run(skip_download=True)
    second = (processed / "train.csv").read_bytes()
    assert first == second
    train = pd.read_csv(processed / "train.csv")
    assert train.duplicated().sum() == 0


def test_DE08_020(monkeypatch, tmp_path):
    raw, _processed = _use_tmp(monkeypatch, tmp_path)
    _patch_sources(monkeypatch, _tables())
    etl_run.run(skip_download=False)
    blob = "\n".join((raw / name).read_text(encoding="utf-8") for name in ("store.csv", "sales.csv", "pop.csv", "change.csv"))
    for banned in ("DATA_GO_KR_KEY", "주민", "전화번호", "이메일", "010-"):
        assert banned not in blob
    header = (raw / "store.csv").read_text(encoding="utf-8").splitlines()[0]
    assert "점포_수" in header


def test_DE08_021():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "data/tests", "-q", "--tb=line"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_DE08_022(monkeypatch, tmp_path, capsys):
    _use_tmp(monkeypatch, tmp_path)
    _patch_sources(monkeypatch, _tables())
    etl_run.run(skip_download=False)
    out = capsys.readouterr().out
    assert "학습용" in out and "행" in out
    assert "20242" in out or "분기" in out, f"행 수는 있으나 기간이 없음: {out}"


def test_DE08_023(monkeypatch, tmp_path):
    _raw, processed = _use_tmp(monkeypatch, tmp_path)
    _patch_sources(monkeypatch, _tables())
    etl_run.run(skip_download=False)
    options = json.loads((processed / "options.json").read_text(encoding="utf-8"))
    assert any(key in options for key in ("기준일", "data_as_of", "as_of")), f"keys={list(options)}"
    assert any(key in options for key in ("처리일", "processed_at", "processed_on")), f"keys={list(options)}"
