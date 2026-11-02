"""pytest와 별도로 전처리 경계값을 한 번 더 계산한다.

기대값은 data/tests/test_transform.py 와 data/etl/transform.py 에서 확인한 동작이다.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from data.etl.transform import clean_sales, district_from_dong, to_number


def main() -> int:
    numbers = to_number(pd.Series(["1,000", " 20 ", "", "abc", None]))
    if numbers.iloc[0] != 1000 or numbers.iloc[1] != 20:
        print("FAIL to_number 정상값", numbers.tolist())
        return 1
    if not all(pd.isna(numbers.iloc[index]) for index in (2, 3, 4)):
        print("FAIL to_number 빈 값·예외값·NULL", numbers.tolist())
        return 1
    if district_from_dong("11680640") != "강남구" or district_from_dong("99999") != "":
        print("FAIL district_from_dong")
        return 1
    sales = clean_sales(
        pd.DataFrame(
            [
                {
                    "기준_년분기_코드": "20251",
                    "행정동_코드": "11440740",
                    "행정동_코드_명": "연남동",
                    "서비스_업종_코드": "CS100010",
                    "서비스_업종_코드_명": "커피-음료",
                    "당월_매출_금액": "100000000",
                    "당월_매출_건수": "5000",
                }
            ]
        )
    )
    if sales.iloc[0]["sales_amount"] != 10000:
        print("FAIL clean_sales 원→만원", sales.iloc[0]["sales_amount"])
        return 1
    print("oracle PASS to_number 빈값·NULL·예외, clean_sales 100000000원=10000만원")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
