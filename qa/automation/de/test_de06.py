"""DE06 merge_tables / make_dong_stats."""
import pandas as pd
import pytest

from data.etl.transform import make_dong_stats, merge_tables


def _store(**overrides):
    base = {
        "quarter": "20242",
        "dong_code": "11440740",
        "dong": "연남동",
        "district": "마포구",
        "industry_code": "CS100001",
        "industry": "한식음식점",
        "store_count": 10.0,
        "open_rate": 3.2,
        "open_count": 1.0,
        "close_rate": 2.0,
        "close_count": 1.0,
        "franchise_count": 2.0,
        "franchise_ratio": 0.2,
    }
    base.update(overrides)
    return base


def _sales(**overrides):
    base = {
        "quarter": "20242",
        "dong_code": "11440740",
        "industry_code": "CS100001",
        "sales_amount": 1000.0,
        "sales_count": 3000.0,
    }
    base.update(overrides)
    return base


def _pop(**overrides):
    base = {"quarter": "20242", "dong_code": "11440740", "foot_traffic": 50000.0}
    base.update(overrides)
    return base


def _change(**overrides):
    base = {
        "quarter": "20242",
        "dong_code": "11440740",
        "change_code": "HH",
        "change_name": "정체",
        "operate_months": 12.0,
    }
    base.update(overrides)
    return base


def _frame(rows, columns):
    if not rows:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(rows)


def _merge(stores, sales, pops, changes):
    return merge_tables(
        _frame(stores, list(_store().keys())),
        _frame(sales, list(_sales().keys())),
        _frame(pops, list(_pop().keys())),
        _frame(changes, list(_change().keys())),
    )


def test_DE06_001():
    out = _merge([_store()], [_sales(sales_amount=1000)], [_pop()], [_change()])
    assert len(out) == 1
    assert out.iloc[0]["sales_amount"] == pytest.approx(1000)


def test_DE06_002():
    out = _merge([_store()], [_sales()], [_pop(foot_traffic=80000)], [_change()])
    assert out.iloc[0]["foot_traffic"] == pytest.approx(80000)


def test_DE06_003():
    out = _merge([_store()], [_sales()], [_pop()], [_change(change_code="LH", change_name="상권확장")])
    assert out.iloc[0]["change_code"] == "LH"
    assert out.iloc[0]["change_name"] == "상권확장"
    assert out.iloc[0]["operate_months"] == pytest.approx(12)


def test_DE06_004():
    out = _merge(
        [_store(dong="연남동")],
        [],
        [_pop()],
        [_change()],
    )
    assert len(out) == 1, f"매출 없는 점포가 최종 {len(out)}행"
    assert out.iloc[0]["dong"] == "연남동"
    assert out.iloc[0]["industry"] == "한식음식점"


def test_DE06_005():
    stores = [
        _store(dong_code="11440740", dong="연남동"),
        _store(dong_code="11440750", dong="성산동"),
        _store(dong_code="11440760", dong="서교동"),
    ]
    sales = [
        _sales(dong_code="11440740", sales_amount=100),
        _sales(dong_code="11440760", sales_amount=100),
    ]
    pops = [_pop(dong_code=code) for code in ("11440740", "11440750", "11440760")]
    changes = [_change(dong_code=code) for code in ("11440740", "11440750", "11440760")]
    out = _merge(stores, sales, pops, changes)
    missing = out[out["dong_code"] == "11440750"]
    assert len(missing) == 1
    assert missing.iloc[0]["sales_amount"] == pytest.approx(100)


def test_DE06_006():
    stores = [
        _store(dong_code="11440740"),
        _store(dong_code="11440750"),
        _store(dong_code="11440760"),
    ]
    sales = [_sales(dong_code=code) for code in ("11440740", "11440750", "11440760")]
    pops = [_pop(dong_code="11440740", foot_traffic=500), _pop(dong_code="11440760", foot_traffic=500)]
    changes = [_change(dong_code=code) for code in ("11440740", "11440750", "11440760")]
    out = _merge(stores, sales, pops, changes)
    filled = out[out["dong_code"] == "11440750"]
    assert filled.iloc[0]["foot_traffic"] == pytest.approx(500)


def test_DE06_007():
    stores = [
        _store(dong_code="11440740"),
        _store(dong_code="11440750"),
        _store(dong_code="11440760"),
    ]
    sales = [_sales(dong_code=code) for code in ("11440740", "11440750", "11440760")]
    pops = [_pop(dong_code=code) for code in ("11440740", "11440750", "11440760")]
    changes = [
        _change(dong_code="11440740", operate_months=15),
        _change(dong_code="11440760", operate_months=15),
    ]
    out = _merge(stores, sales, pops, changes)
    filled = out[out["dong_code"] == "11440750"]
    assert filled.iloc[0]["operate_months"] == pytest.approx(15)


def test_DE06_008():
    out = _merge([_store()], [_sales()], [_pop()], [])
    assert len(out) == 1
    assert out.iloc[0]["change_code"] == "HH"


def test_DE06_009():
    out = _merge(
        [_store()],
        [_sales()],
        [_pop()],
        [_change(change_code="HH", change_name=None)],
    )
    assert out.iloc[0]["change_name"] == "정체"


def test_DE06_010():
    out = _merge([_store(store_count=10)], [_sales(sales_amount=1000)], [_pop()], [_change()])
    assert out.iloc[0]["sales_per_store"] == pytest.approx(100)


def test_DE06_011():
    out = _merge([_store(store_count=2)], [_sales()], [_pop()], [_change()])
    assert len(out) == 0


def test_DE06_012():
    out = _merge([_store(store_count=3)], [_sales(sales_amount=300)], [_pop()], [_change()])
    assert len(out) == 1
    assert out.iloc[0]["store_count"] == 3


def test_DE06_013():
    stores = [
        _store(industry_code="CS100001", industry="한식음식점"),
        _store(industry_code="CS100010", industry="커피-음료"),
    ]
    sales = [
        _sales(industry_code="CS100001", sales_amount=1000, sales_count=11),
        _sales(industry_code="CS100010", sales_amount=1000, sales_count=22),
    ]
    out = _merge(stores, sales, [_pop()], [_change()])
    by_code = dict(zip(out["industry_code"], out["sales_count"]))
    assert by_code["CS100001"] == pytest.approx(11)
    assert by_code["CS100010"] == pytest.approx(22)


def test_DE06_014():
    stores = [
        _store(dong_code="11440740", dong="연남동"),
        _store(dong_code="11680640", dong="역삼1동", district="강남구"),
    ]
    sales = [
        _sales(dong_code="11440740", sales_count=111),
        _sales(dong_code="11680640", sales_count=222),
    ]
    pops = [_pop(dong_code="11440740"), _pop(dong_code="11680640", foot_traffic=90000)]
    changes = [_change(dong_code="11440740"), _change(dong_code="11680640")]
    out = _merge(stores, sales, pops, changes)
    by_dong = dict(zip(out["dong_code"], out["sales_count"]))
    assert by_dong["11440740"] == pytest.approx(111)
    assert by_dong["11680640"] == pytest.approx(222)
    assert out.loc[out["dong_code"] == "11680640", "foot_traffic"].iloc[0] == pytest.approx(90000)


def test_DE06_015():
    stores = [_store(quarter="20241"), _store(quarter="20242")]
    sales = [
        _sales(quarter="20241", sales_count=111),
        _sales(quarter="20242", sales_count=222),
    ]
    pops = [_pop(quarter="20241"), _pop(quarter="20242")]
    changes = [_change(quarter="20241"), _change(quarter="20242")]
    out = _merge(stores, sales, pops, changes)
    by_q = dict(zip(out["quarter"], out["sales_count"]))
    assert by_q["20241"] == pytest.approx(111)
    assert by_q["20242"] == pytest.approx(222)


def test_DE06_016():
    out = _merge(
        [_store()],
        [_sales()],
        [_pop(foot_traffic=100), _pop(foot_traffic=200)],
        [_change()],
    )
    assert len(out) == 1, f"인구 중복키로 행이 1→{len(out)} 증식했는데 감지하지 않음"


def test_DE06_017():
    from data.etl.transform import clean_sales

    raw = pd.DataFrame(
        [
            {
                "기준_년분기_코드": "20242",
                "행정동_코드": "11440740",
                "행정동_코드_명": "연남동",
                "서비스_업종_코드": "CS100001",
                "서비스_업종_코드_명": "한식음식점",
                "당월_매출_금액": "0",
                "당월_매출_건수": "3",
            },
            {
                "기준_년분기_코드": "20242",
                "행정동_코드": "11680640",
                "행정동_코드_명": "역삼1동",
                "서비스_업종_코드": "CS100001",
                "서비스_업종_코드_명": "한식음식점",
                "당월_매출_금액": "10000",
                "당월_매출_건수": "3",
            },
        ]
    )
    df = clean_sales(raw)
    assert len(df) == 1
    assert df.iloc[0]["dong_code"] == "11680640"
    assert df.iloc[0]["sales_amount"] == pytest.approx(1)


def test_DE06_018():
    train = pd.DataFrame(
        [
            _store(quarter="20241", close_rate=2, sales_per_store=10),
            _store(quarter="20242", close_rate=4, sales_per_store=20),
        ]
    )
    stats = make_dong_stats(train)
    assert set(stats["quarter"]) == {"20242"}
    assert len(stats) == 1


def test_DE06_019():
    train = pd.DataFrame(
        [
            _store(industry_code="A", industry="한식", close_rate=2, sales_per_store=10),
            _store(industry_code="B", industry="카페", close_rate=4, sales_per_store=10),
            _store(industry_code="C", industry="분식", close_rate=6, sales_per_store=10),
        ]
    )
    stats = make_dong_stats(train)
    assert stats["median_close_rate"].iloc[0] == pytest.approx(4.0)


def test_DE06_020():
    train = pd.DataFrame(
        [
            _store(industry_code="A", industry="한식", sales_per_store=100, close_rate=1),
            _store(industry_code="B", industry="카페", sales_per_store=300, close_rate=1),
        ]
    )
    stats = make_dong_stats(train)
    assert stats["median_sales_per_store"].iloc[0] == pytest.approx(200)


def test_DE06_021():
    train = pd.DataFrame(
        [
            _store(quarter="20249", sales_per_store=1, close_rate=1),
            _store(quarter="202410", sales_per_store=2, close_rate=1),
        ]
    )
    try:
        stats = make_dong_stats(train)
    except Exception as error:
        assert any(token in str(error) for token in ("형식", "분기", "quarter"))
    else:
        assert set(stats["quarter"]) == {"202410"}, (
            f"문자열 max 분기={sorted(set(stats['quarter']))} (사전순 20249 > 202410)"
        )


def test_DE06_022():
    out = _merge([_store()], [_sales()], [_pop()], [_change(change_code="HL", change_name="기타")])
    assert out.iloc[0]["change_name"] == "상권축소"


def test_DE06_023():
    stores = []
    for quarter in ("20241", "20242"):
        for code, name in (("A", "한식"), ("B", "카페"), ("C", "분식")):
            stores.append(
                _store(quarter=quarter, industry_code=code, industry=name, close_rate=2, sales_per_store=10)
            )
    stats = make_dong_stats(pd.DataFrame(stores))
    assert len(stats) == 3
    assert set(stats["quarter"]) == {"20242"}


def test_DE06_024():
    try:
        out = _merge(
            [_store(industry=None)],
            [_sales()],
            [_pop()],
            [_change()],
        )
    except Exception as error:
        assert "업종" in str(error) or "industry" in str(error).lower(), (
            f"업종 누락이 피처 방어 없이 실패: {type(error).__name__}: {error}"
        )
    else:
        assert out["industry"].notna().all(), f"industry null {len(out)}행이 학습 테이블에 남음"
