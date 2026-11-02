"""DE07 make_options."""
import pandas as pd

from data.etl.config import SEOUL_DISTRICTS
from data.etl.transform import make_dong_stats, make_options


def _train_row(**overrides):
    base = {
        "quarter": "20242",
        "district": "마포구",
        "dong": "연남동",
        "dong_code": "11440740",
        "industry": "한식음식점",
        "industry_code": "CS100001",
        "close_rate": 2.0,
        "sales_per_store": 100.0,
    }
    base.update(overrides)
    return base


def test_DE07_001():
    rows = [
        _train_row(district=name, dong=f"{name}동", dong_code=f"{code}000", industry="한식", industry_code="A")
        for code, name in SEOUL_DISTRICTS.items()
    ]
    options = make_options(pd.DataFrame(rows), [], [])
    assert len(options["districts"]) == 25
    assert options["districts"] == sorted(SEOUL_DISTRICTS.values())


def test_DE07_002():
    rows = [
        _train_row(district="마포구", dong="합정동", dong_code="11440710"),
        _train_row(district="강남구", dong="역삼1동", dong_code="11680640"),
        _train_row(district="마포구", dong="연남동", dong_code="11440740"),
        _train_row(district="강남구", dong="삼성동", dong_code="11680510"),
    ]
    options = make_options(pd.DataFrame(rows), [], [])
    pairs = [(row["district"], row["dong"]) for row in options["dongs"]]
    assert pairs == sorted(pairs)


def test_DE07_003():
    rows = [
        _train_row(district="마포구", dong="연남동", dong_code="11440740"),
        _train_row(district="마포구", dong="연남동", dong_code="11440740", industry="커피", industry_code="B"),
    ]
    options = make_options(pd.DataFrame(rows), [], [])
    assert len(options["dongs"]) == 1


def test_DE07_004():
    rows = [
        _train_row(industry="한식", industry_code="A"),
        _train_row(industry="커피", industry_code="B"),
        _train_row(industry="분식", industry_code="C"),
    ]
    options = make_options(pd.DataFrame(rows), [], [])
    names = [row["industry"] for row in options["industries"]]
    assert names == sorted(["한식", "커피", "분식"])


def test_DE07_005():
    rows = [
        _train_row(industry="한식", industry_code="CS100001"),
        _train_row(industry="한식", industry_code="CS100001", dong="합정동", dong_code="11440710"),
    ]
    options = make_options(pd.DataFrame(rows), [], [])
    assert len(options["industries"]) == 1


def test_DE07_006():
    rows = [
        _train_row(industry="한식", industry_code="CS100001"),
        _train_row(industry="한식", industry_code="CS100099"),
    ]
    options = make_options(pd.DataFrame(rows), [], [])
    codes = sorted(row["industry_code"] for row in options["industries"])
    assert codes == ["CS100001", "CS100099"]


def test_DE07_007():
    options = make_options(pd.DataFrame([_train_row()]), [], [])
    assert options["dongs"] == [
        {"district": "마포구", "dong": "연남동", "dong_code": "11440740"}
    ]


def test_DE07_008():
    semas = [{"code": str(i)} for i in range(5)]
    options = make_options(pd.DataFrame([_train_row()]), semas, [])
    assert options["semas_dong_count"] == 5


def test_DE07_009():
    semas = [{"code": str(i)} for i in range(10)]
    options = make_options(pd.DataFrame([_train_row()]), [], semas)
    assert options["semas_upjong_count"] == 10


def test_DE07_010():
    options = make_options(pd.DataFrame([_train_row()]), [], [])
    assert options["semas_dong_count"] == 0
    assert options["semas_upjong_count"] == 0


def test_DE07_011():
    train = pd.DataFrame(columns=["district", "dong", "dong_code", "industry", "industry_code"])
    options = make_options(train, [], [])
    assert options["districts"] == []
    assert options["dongs"] == []
    assert options["industries"] == []


def test_DE07_012():
    rows = [_train_row(district="마포구"), _train_row(district=None, dong="없는동", dong_code="00000000")]
    options = make_options(pd.DataFrame(rows), [], [])
    assert all(pd.notna(name) and str(name).strip() for name in options["districts"])
    assert None not in options["districts"]
    assert "마포구" in options["districts"]


def test_DE07_013():
    code = "11680640"
    options = make_options(pd.DataFrame([_train_row(dong_code=code, district="강남구", dong="역삼1동")]), [], [])
    assert options["dongs"][0]["dong_code"] == "11680640"
    assert isinstance(options["dongs"][0]["dong_code"], str)
    assert len(options["dongs"][0]["dong_code"]) == 8


def test_DE07_014():
    options = make_options(pd.DataFrame([_train_row(industry=" 한식 ")]), [], [])
    assert options["industries"][0]["industry"] == "한식"


def test_DE07_015():
    rows = [
        _train_row(district="마포구", dong="연남동", dong_code="11440740", industry="한식", industry_code="A"),
        _train_row(district="강남구", dong="역삼1동", dong_code="11680640", industry="커피", industry_code="B"),
    ]
    train = pd.DataFrame(rows)
    options = make_options(train, [], [])
    stats = make_dong_stats(train)
    stat_dongs = set(zip(stats["district"], stats["dong_code"]))
    stat_inds = set(zip(stats["industry"], stats["industry_code"]))
    for dong in options["dongs"]:
        assert (dong["district"], dong["dong_code"]) in stat_dongs
    for industry in options["industries"]:
        assert (industry["industry"], industry["industry_code"]) in stat_inds


def test_DE07_016():
    rows = [
        _train_row(district="마포구", dong="연남동", dong_code="11440740"),
        _train_row(district="마포구", dong="합정동", dong_code="11440710"),
        _train_row(district="강남구", dong="역삼1동", dong_code="11680640"),
    ]
    options = make_options(pd.DataFrame(rows), [], [])
    mapo = [row["dong"] for row in options["dongs"] if row["district"] == "마포구"]
    gangnam = [row["dong"] for row in options["dongs"] if row["district"] == "강남구"]
    assert mapo == ["연남동", "합정동"] or mapo == sorted(mapo)
    assert set(mapo) == {"연남동", "합정동"}
    assert gangnam == ["역삼1동"]
