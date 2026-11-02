"""DE05 to_number / fill_missing / remove_outliers."""
import numpy as np
import pandas as pd
import pytest

from data.etl.transform import fill_missing, remove_outliers, to_number


def test_DE05_001():
    out = to_number(pd.Series(["1,234.5"]))
    assert out.iloc[0] == pytest.approx(1234.5)


def test_DE05_002():
    out = to_number(pd.Series([""]))
    assert pd.isna(out.iloc[0])


def test_DE05_003():
    out = to_number(pd.Series(["오류"]))
    assert pd.isna(out.iloc[0])


def test_DE05_004():
    df = pd.DataFrame(
        {"industry": ["한식", "한식", "카페", "카페"], "v": [np.nan, np.nan, 10.0, 30.0]}
    )
    out = fill_missing(df, "v", "industry")
    assert out.loc[out["industry"] == "한식", "v"].tolist() == [20.0, 20.0]


def test_DE05_005():
    df = pd.DataFrame({"industry": ["한식", "한식", "한식"], "v": [1.0, np.nan, 3.0]})
    out = fill_missing(df, "v", "industry")
    assert out["v"].tolist() == [1.0, 2.0, 3.0]


def test_DE05_006():
    df = pd.DataFrame({"industry": ["한식", "한식"], "v": [50.0, np.nan]})
    out = fill_missing(df, "v", "industry")
    assert out.iloc[0]["v"] == 50


def test_DE05_007():
    df = pd.DataFrame({"industry": ["한식", "카페"], "v": [np.nan, np.nan]})
    out = fill_missing(df.copy(), "v", "industry")
    assert out["v"].isna().all()
    quality = out.attrs.get("quality_check") if hasattr(out, "attrs") else None
    assert quality, f"전체 NaN 유지 values={out['v'].tolist()} 후속 품질검사 없음"


def test_DE05_008():
    df = pd.DataFrame({"industry": ["한식"], "v": [42.0]})
    out = remove_outliers(df, "v", "industry")
    assert len(out) == 1
    assert out.iloc[0]["v"] == 42


def test_DE05_009():
    values = list(range(100))
    df = pd.DataFrame({"industry": ["한식"] * 100, "v": values})
    original = pd.Series(values, dtype=float)
    low, high = original.quantile(0.01), original.quantile(0.99)
    out = remove_outliers(df, "v", "industry")
    outside = [value for value in values if value < low or value > high]
    assert outside
    assert set(outside).isdisjoint(set(out["v"]))
    assert out["v"].min() >= low
    assert out["v"].max() <= high


def test_DE05_010():
    values = list(range(1, 101)) + [10_000_000]
    df = pd.DataFrame({"industry": ["한식"] * len(values), "v": values})
    out = remove_outliers(df, "v", "industry")
    assert 10_000_000 not in set(out["v"])
    assert 50 in set(out["v"])


def test_DE05_011():
    values = [-100] + list(range(1, 101))
    df = pd.DataFrame({"industry": ["한식"] * len(values), "v": values})
    out = remove_outliers(df, "v", "industry")
    assert -100 not in set(out["v"])
    assert 50 in set(out["v"])


def test_DE05_012():
    df = pd.DataFrame({"industry": ["한식"] * 5, "v": [1.0, 2.0, 3.0, 4.0, np.nan]})
    out = fill_missing(df, "v", "industry")
    assert out.iloc[-1]["v"] == pytest.approx(2.5)


def test_DE05_013():
    df = pd.DataFrame({"industry": ["한식"] * 4, "v": ["1", "2", None, "4"]})
    out = fill_missing(df, "v", "industry")
    assert pd.api.types.is_numeric_dtype(out["v"])
    assert out["v"].iloc[2] == pytest.approx(2.5)


def test_DE05_014():
    hansik = [10.0] * 99 + [1000.0]
    cafe = [1000.0] * 100
    df = pd.DataFrame(
        {
            "industry": ["한식"] * 100 + ["카페"] * 100,
            "v": hansik + cafe,
        }
    )
    out = remove_outliers(df, "v", "industry")
    hansik_out = out[out["industry"] == "한식"]["v"]
    cafe_out = out[out["industry"] == "카페"]["v"]
    assert 1000.0 not in set(hansik_out)
    assert 1000.0 in set(cafe_out)
    assert len(cafe_out) == 100


def test_DE05_015():
    df = pd.DataFrame({"industry": ["한식"], "v": [1.0]})
    with pytest.raises(KeyError) as caught:
        fill_missing(df, "no_such", "industry")
    assert "no_such" in str(caught.value)


def test_DE05_016():
    df = pd.DataFrame({"industry": ["한식", None, "한식"], "v": [1.0, np.nan, 3.0]})
    out = fill_missing(df, "v", "industry")
    missing = out[out["industry"].isna()]
    assert missing.empty or missing["v"].isna().all(), (
        f"industry=None 행이 다른 그룹 값으로 채워짐 {missing['v'].tolist()}"
    )


def test_DE05_017():
    df = pd.DataFrame({"industry": [None, None], "v": [1.0, 10_000_000.0]})
    out = remove_outliers(df, "v", "industry")
    assert isinstance(out, pd.DataFrame)
    assert len(out) == 0


def test_DE05_018():
    df = pd.DataFrame({"industry": ["한식"] * 5, "v": [5.0] * 5})
    out = remove_outliers(df, "v", "industry")
    assert len(out) == 5
    assert set(out["v"]) == {5.0}


def test_DE05_019():
    df = pd.DataFrame({"industry": ["한식", "한식"], "v": [np.nan, np.nan]})
    try:
        out = remove_outliers(df, "v", "industry")
    except Exception as error:
        assert "quantile" in str(error).lower() or "이상" in str(error) or "NaN" in str(error)
    else:
        assert len(out) == 0 or out["v"].notna().all()
