"""전처리 함수 테스트. 실행: python -m pytest data/tests"""
import pandas as pd

from data.etl.transform import (
    classify_risk,
    clean_change,
    clean_pop,
    clean_sales,
    clean_store,
    district_from_dong,
    merge_tables,
    to_number,
)


def test_to_number():
    series = pd.Series(["1,000", " 20 ", "", "abc"])
    out = to_number(series)
    assert out.iloc[0] == 1000
    assert out.iloc[1] == 20
    assert pd.isna(out.iloc[2])
    assert pd.isna(out.iloc[3])


def test_district_from_dong():
    assert district_from_dong("11680640") == "강남구"
    assert district_from_dong("11440740") == "마포구"
    assert district_from_dong("99999") == ""


def test_clean_store():
    raw = pd.DataFrame([
        {
            "기준_년분기_코드": "20251", "행정동_코드": "11680640", "행정동_코드_명": "역삼1동",
            "서비스_업종_코드": "CS100001", "서비스_업종_코드_명": "한식음식점",
            "점포_수": "80", "개업_율": "3", "개업_점포_수": "2",
            "폐업_률": "2", "폐업_점포_수": "2", "프랜차이즈_점포_수": "8",
        },
        {
            "기준_년분기_코드": "20251", "행정동_코드": "99999999", "행정동_코드_명": "없는동",
            "서비스_업종_코드": "CS100001", "서비스_업종_코드_명": "한식음식점",
            "점포_수": "0", "개업_율": "0", "개업_점포_수": "0",
            "폐업_률": "0", "폐업_점포_수": "0", "프랜차이즈_점포_수": "0",
        },
    ])
    df = clean_store(raw)
    assert len(df) == 1
    assert df.iloc[0]["district"] == "강남구"
    assert df.iloc[0]["franchise_ratio"] == 0.1


def test_clean_sales_won_to_manwon():
    raw = pd.DataFrame([{
        "기준_년분기_코드": "20251", "행정동_코드": "11440740", "행정동_코드_명": "연남동",
        "서비스_업종_코드": "CS100010", "서비스_업종_코드_명": "커피-음료",
        "당월_매출_금액": "100000000", "당월_매출_건수": "5000",
    }])
    df = clean_sales(raw)
    assert df.iloc[0]["sales_amount"] == 10000  # 1억원 → 1만 만원


def test_merge_and_risk():
    store = clean_store(pd.DataFrame([{
        "기준_년분기_코드": "20251", "행정동_코드": "11440740", "행정동_코드_명": "연남동",
        "서비스_업종_코드": "CS100001", "서비스_업종_코드_명": "한식음식점",
        "점포_수": "50", "개업_율": "4", "개업_점포_수": "2",
        "폐업_률": "3", "폐업_점포_수": "1", "프랜차이즈_점포_수": "5",
    }]))
    sales = clean_sales(pd.DataFrame([{
        "기준_년분기_코드": "20251", "행정동_코드": "11440740", "행정동_코드_명": "연남동",
        "서비스_업종_코드": "CS100001", "서비스_업종_코드_명": "한식음식점",
        "당월_매출_금액": "500000000", "당월_매출_건수": "10000",
    }]))
    pop = clean_pop(pd.DataFrame([{
        "기준_년분기_코드": "20251", "행정동_코드": "11440740", "행정동_코드_명": "연남동",
        "총_유동인구_수": "800000",
    }]))
    change = clean_change(pd.DataFrame([{
        "기준_년분기_코드": "20251", "행정동_코드": "11440740", "행정동_코드_명": "연남동",
        "상권_변화_지표": "LH", "상권_변화_지표_명": "상권확장",
        "운영_영업_개월_평균": "90", "폐업_영업_개월_평균": "50",
        "서울_운영_영업_개월_평균": "118", "서울_폐업_영업_개월_평균": "54",
    }]))
    merged = merge_tables(store, sales, pop, change)
    assert len(merged) == 1
    assert merged.iloc[0]["sales_per_store"] == 1000.0
    assert merged.iloc[0]["change_name"] == "상권확장"
    assert classify_risk(3, "LH") == "stable"
    assert classify_risk(5, "HH") == "warning"
    assert classify_risk(2, "HL") == "danger"
