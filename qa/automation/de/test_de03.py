"""DE03 clean_store."""
import pandas as pd
import pytest

from data.etl.transform import clean_store


def _row(**overrides):
    base = {
        "기준_년분기_코드": "20242",
        "행정동_코드": "11440740",
        "행정동_코드_명": "연남동",
        "서비스_업종_코드": "CS100001",
        "서비스_업종_코드_명": "한식음식점",
        "점포_수": "10",
        "개업_율": "3.20",
        "개업_점포_수": "1",
        "폐업_률": "5.25",
        "폐업_점포_수": "1",
        "프랜차이즈_점포_수": "2",
    }
    base.update(overrides)
    return base


def test_DE03_001():
    df = clean_store(pd.DataFrame([_row()]))
    assert {"quarter", "dong_code", "industry_code"} <= set(df.columns)
    assert df.iloc[0]["quarter"] == "20242"
    assert df.iloc[0]["dong_code"] == "11440740"
    assert df.iloc[0]["industry_code"] == "CS100001"


def test_DE03_002():
    df = clean_store(pd.DataFrame([_row(행정동_코드="11440100")]))
    assert len(df) == 1
    assert df.iloc[0]["district"] == "마포구"


def test_DE03_003():
    df = clean_store(pd.DataFrame([_row(행정동_코드="26110510", 행정동_코드_명="부산동")]))
    assert len(df) == 0


def test_DE03_004():
    df = clean_store(pd.DataFrame([_row(점포_수="1")]))
    assert len(df) == 1
    assert df.iloc[0]["store_count"] == 1


def test_DE03_005():
    df = clean_store(pd.DataFrame([_row(점포_수="0")]))
    assert len(df) == 0


def test_DE03_006():
    df = clean_store(pd.DataFrame([_row(점포_수="-1")]))
    assert len(df) == 0


def test_DE03_007():
    df = clean_store(pd.DataFrame([_row(점포_수="1,000")]))
    assert len(df) == 1
    assert df.iloc[0]["store_count"] == 1000


def test_DE03_008():
    df = clean_store(pd.DataFrame([_row(폐업_률="5.25")]))
    assert df.iloc[0]["close_rate"] == pytest.approx(5.25)


def test_DE03_009():
    df = clean_store(pd.DataFrame([_row(개업_율="3.20")]))
    assert df.iloc[0]["open_rate"] == pytest.approx(3.20)


def test_DE03_010():
    df = clean_store(pd.DataFrame([_row(프랜차이즈_점포_수="2", 점포_수="10")]))
    assert df.iloc[0]["franchise_ratio"] == pytest.approx(0.2)


def test_DE03_011():
    df = clean_store(pd.DataFrame([_row(프랜차이즈_점포_수="12", 점포_수="10")]))
    assert df.iloc[0]["franchise_ratio"] == pytest.approx(1)


def test_DE03_012():
    df = clean_store(pd.DataFrame([_row(프랜차이즈_점포_수="-1", 점포_수="10")]))
    assert df.iloc[0]["franchise_ratio"] == pytest.approx(0)


def test_DE03_013():
    df = clean_store(pd.DataFrame([_row(프랜차이즈_점포_수=None, 점포_수="10")]))
    ratio = df.iloc[0]["franchise_ratio"]
    assert pd.notna(ratio), f"franchise_count=None 이후 franchise_ratio={ratio} NaN 후처리 없음"


def test_DE03_014():
    raw = pd.DataFrame([_row(점포_수="10"), _row(점포_수="99")])
    df = clean_store(raw)
    assert len(df) == 1


def test_DE03_015():
    raw = pd.DataFrame([_row(기준_년분기_코드="20241"), _row(기준_년분기_코드="20242")])
    df = clean_store(raw)
    assert len(df) == 2
    assert set(df["quarter"]) == {"20241", "20242"}


def test_DE03_016():
    raw = pd.DataFrame(
        [
            _row(서비스_업종_코드="CS100001", 서비스_업종_코드_명="한식음식점"),
            _row(서비스_업종_코드="CS100010", 서비스_업종_코드_명="커피-음료"),
        ]
    )
    df = clean_store(raw)
    assert len(df) == 2
    assert set(df["industry_code"]) == {"CS100001", "CS100010"}


def test_DE03_017():
    df = clean_store(pd.DataFrame([_row(행정동_코드=11440740.0)]))
    assert df.iloc[0]["district"] == "마포구"
    assert df.iloc[0]["dong_code"] == "11440740"


def test_DE03_018():
    df = clean_store(pd.DataFrame([_row(행정동_코드_명="")]))
    assert len(df) == 0, f"dong='' 행이 {len(df)}건 남음"


def test_DE03_019():
    df = clean_store(pd.DataFrame([_row(폐업_률="120")]))
    assert len(df) == 0 or df.iloc[0]["close_rate"] <= 100
    if len(df):
        assert 0 <= df.iloc[0]["close_rate"] <= 100, f"close_rate={df.iloc[0]['close_rate']}"


def test_DE03_020():
    df = clean_store(pd.DataFrame([_row(점포_수="2.5")]))
    assert len(df) == 0 or float(df.iloc[0]["store_count"]).is_integer(), (
        f"store_count={df.iloc[0]['store_count']} 소수 허용, 정수 검증 없음"
    )
