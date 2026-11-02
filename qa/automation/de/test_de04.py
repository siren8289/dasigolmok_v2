"""DE04 clean_sales / clean_pop / clean_change."""
import inspect

import pandas as pd
import pytest

from data.etl.transform import clean_change, clean_pop, clean_sales


def _sales(**overrides):
    base = {
        "기준_년분기_코드": "20242",
        "행정동_코드": "11440740",
        "행정동_코드_명": "연남동",
        "서비스_업종_코드": "CS100001",
        "서비스_업종_코드_명": "한식음식점",
        "당월_매출_금액": "10000000",
        "당월_매출_건수": "3000",
    }
    base.update(overrides)
    return base


def _pop(**overrides):
    base = {
        "기준_년분기_코드": "20242",
        "행정동_코드": "11440740",
        "행정동_코드_명": "연남동",
        "총_유동인구_수": "100",
    }
    base.update(overrides)
    return base


def _change(**overrides):
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


def test_DE04_001():
    df = clean_sales(pd.DataFrame([_sales(당월_매출_금액="10000000")]))
    assert df.iloc[0]["sales_amount"] == pytest.approx(1000)


def test_DE04_002():
    df = clean_sales(pd.DataFrame([_sales(당월_매출_금액="1")]))
    assert df.iloc[0]["sales_amount"] == pytest.approx(0.0001)


def test_DE04_003():
    df = clean_sales(pd.DataFrame([_sales(당월_매출_금액="0")]))
    assert len(df) == 0


def test_DE04_004():
    df = clean_sales(pd.DataFrame([_sales(당월_매출_금액="-100")]))
    assert len(df) == 0


def test_DE04_005():
    df = clean_sales(pd.DataFrame([_sales(당월_매출_금액=None)]))
    assert len(df) == 0


def test_DE04_006():
    df = clean_sales(pd.DataFrame([_sales(당월_매출_금액="1,000")]))
    assert df.iloc[0]["sales_amount"] == pytest.approx(0.1)


def test_DE04_007():
    df = clean_sales(pd.DataFrame([_sales(당월_매출_건수="3,000")]))
    assert df.iloc[0]["sales_count"] == pytest.approx(3000)


def test_DE04_008():
    df = clean_sales(pd.DataFrame([_sales(행정동_코드="26110510", 행정동_코드_명="부산동")]))
    assert len(df) == 0


def test_DE04_009():
    raw = pd.DataFrame(
        [
            _sales(당월_매출_금액="10000000"),
            _sales(당월_매출_금액="20000000"),
        ]
    )
    df = clean_sales(raw)
    assert len(df) == 1


def test_DE04_010():
    df = clean_pop(pd.DataFrame([_pop(총_유동인구_수="100")]))
    assert len(df) == 1
    assert df.iloc[0]["foot_traffic"] == pytest.approx(100)


def test_DE04_011():
    df = clean_pop(pd.DataFrame([_pop(총_유동인구_수="0")]))
    assert len(df) == 0


def test_DE04_012():
    df = clean_pop(pd.DataFrame([_pop(총_유동인구_수="-1")]))
    assert len(df) == 0


def test_DE04_013():
    df = clean_pop(pd.DataFrame([_pop(총_유동인구_수="50,000")]))
    assert df.iloc[0]["foot_traffic"] == pytest.approx(50000)


def test_DE04_014():
    raw = pd.DataFrame([_pop(총_유동인구_수="100"), _pop(총_유동인구_수="200")])
    df = clean_pop(raw)
    assert len(df) == 1


def test_DE04_015():
    df = clean_change(pd.DataFrame([_change(상권_변화_지표="HH")]))
    assert df.iloc[0]["change_name"] == "정체"


def test_DE04_016():
    df = clean_change(pd.DataFrame([_change(상권_변화_지표="HL", 상권_변화_지표_명="상권축소")]))
    assert df.iloc[0]["change_name"] == "상권축소"


def test_DE04_017():
    df = clean_change(pd.DataFrame([_change(상권_변화_지표="LH", 상권_변화_지표_명="상권확장")]))
    assert df.iloc[0]["change_name"] == "상권확장"


def test_DE04_018():
    df = clean_change(pd.DataFrame([_change(상권_변화_지표="LL", 상권_변화_지표_명="다이나믹")]))
    assert df.iloc[0]["change_name"] == "다이나믹"


def test_DE04_019():
    df = clean_change(
        pd.DataFrame([_change(상권_변화_지표="XX", 상권_변화_지표_명="원본변화명")])
    )
    assert df.iloc[0]["change_name"] == "원본변화명"


def test_DE04_020():
    df = clean_change(pd.DataFrame([_change(운영_영업_개월_평균="15.5")]))
    assert df.iloc[0]["operate_months"] == pytest.approx(15.5)


def test_DE04_021():
    df = clean_change(
        pd.DataFrame([_change(행정동_코드="26110510", 행정동_코드_명="부산동")])
    )
    assert len(df) == 0


def test_DE04_022():
    raw = pd.DataFrame([{key: value for key, value in _pop().items() if key != "총_유동인구_수"}])
    with pytest.raises(KeyError) as caught:
        clean_pop(raw)
    assert "총_유동인구_수" in str(caught.value)


def test_DE04_023(capsys):
    import data.etl.transform as transform

    sales = clean_sales(pd.DataFrame([_sales()]))
    pop = clean_pop(pd.DataFrame([_pop(총_유동인구_수="1000")]))
    logged = capsys.readouterr().out
    metrics = getattr(sales, "attrs", {})
    source = inspect.getsource(transform.merge_tables) + inspect.getsource(transform.clean_sales)
    measured = any(token in source for token in ("tracemalloc", "perf_counter", "memory_info"))
    assert measured or "메모리" in logged or "elapsed_sec" in metrics, (
        f"계측 없음. clean_sales rows={len(sales)} pop rows={len(pop)}. "
        "200만행 메모리·수행시간을 기록하는 코드가 없어 대용량 부하는 실행하지 않음"
    )
