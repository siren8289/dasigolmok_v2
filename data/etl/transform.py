"""2단계: 받아 온 원본을 학습에 쓸 수 있게 전처리한다.

전처리 순서
  1. 숫자 문자열 정리 ("1,000" → 1000, 빈칸 → NaN)
  2. 필요한 컬럼만 고르고 이름을 영어/짧게 통일
  3. 서울이 아닌 행, 점포 수 0 이하 행 제거
  4. 결측치 채우기 (같은 업종 중앙값)
  5. 파생 변수 만들기 (점포당 매출, 자치구, 프랜차이즈 비율)
  6. 이상치 제거 (업종별 점포당 매출 상하위 1%)
  7. 점포 + 매출 + 유동인구 + 변화지표를 하나로 붙이기
"""
import pandas as pd

from data.etl.config import CHANGE_NAMES, SEOUL_DISTRICTS


def to_number(series):
    """'1,000' 같은 문자열을 숫자로 바꾼다. 바꿀 수 없으면 NaN."""
    cleaned = series.astype(str).str.replace(",", "").str.strip()
    return pd.to_numeric(cleaned, errors="coerce")


def district_from_dong(dong_code):
    """행정동 코드(8자리) 앞 5자리로 자치구 이름을 찾는다."""
    return SEOUL_DISTRICTS.get(str(dong_code)[:5], "")


def _base_columns(raw, extra):
    """공통 키(분기, 행정동, 업종)를 같은 이름으로 맞춘다."""
    df = pd.DataFrame()
    df["quarter"] = raw["기준_년분기_코드"].astype(str)
    df["dong_code"] = raw["행정동_코드"].astype(str)
    df["dong"] = raw["행정동_코드_명"].astype(str)
    df["district"] = df["dong_code"].map(district_from_dong)
    for new_name, old_name in extra.items():
        df[new_name] = raw[old_name]
    return df


def clean_store(raw):
    """점포 표 정리. 점포 수, 개업/폐업, 프랜차이즈 수."""
    df = _base_columns(raw, {
        "industry_code": "서비스_업종_코드",
        "industry": "서비스_업종_코드_명",
        "store_count": "점포_수",
        "open_rate": "개업_율",
        "open_count": "개업_점포_수",
        "close_rate": "폐업_률",
        "close_count": "폐업_점포_수",
        "franchise_count": "프랜차이즈_점포_수",
    })
    for column in ["store_count", "open_rate", "open_count", "close_rate", "close_count", "franchise_count"]:
        df[column] = to_number(df[column])

    df = df[df["district"] != ""]
    df = df[df["store_count"] > 0]
    df["franchise_ratio"] = (df["franchise_count"] / df["store_count"]).clip(0, 1).round(3)
    return df.drop_duplicates(["quarter", "dong_code", "industry_code"])


def clean_sales(raw):
    """추정매출 표 정리. 금액 단위는 원 → 만원으로 바꾼다."""
    df = _base_columns(raw, {
        "industry_code": "서비스_업종_코드",
        "industry": "서비스_업종_코드_명",
        "sales_amount": "당월_매출_금액",
        "sales_count": "당월_매출_건수",
    })
    df["sales_amount"] = to_number(df["sales_amount"]) / 10000  # 원 → 만원
    df["sales_count"] = to_number(df["sales_count"])
    df = df[df["district"] != ""]
    df = df[df["sales_amount"] > 0]
    return df.drop_duplicates(["quarter", "dong_code", "industry_code"])


def clean_pop(raw):
    """유동인구 표 정리. (행정동 × 분기, 업종 없음)"""
    df = pd.DataFrame()
    df["quarter"] = raw["기준_년분기_코드"].astype(str)
    df["dong_code"] = raw["행정동_코드"].astype(str)
    df["dong"] = raw["행정동_코드_명"].astype(str)
    df["district"] = df["dong_code"].map(district_from_dong)
    df["foot_traffic"] = to_number(raw["총_유동인구_수"])
    df = df[df["district"] != ""]
    df = df[df["foot_traffic"] > 0]
    return df.drop_duplicates(["quarter", "dong_code"])


def clean_change(raw):
    """상권변화지표 표 정리. (행정동 × 분기, 업종 없음)"""
    df = pd.DataFrame()
    df["quarter"] = raw["기준_년분기_코드"].astype(str)
    df["dong_code"] = raw["행정동_코드"].astype(str)
    df["dong"] = raw["행정동_코드_명"].astype(str)
    df["district"] = df["dong_code"].map(district_from_dong)
    df["change_code"] = raw["상권_변화_지표"].astype(str)
    df["change_name"] = df["change_code"].map(CHANGE_NAMES).fillna(raw["상권_변화_지표_명"])
    df["operate_months"] = to_number(raw["운영_영업_개월_평균"])
    df = df[df["district"] != ""]
    return df.drop_duplicates(["quarter", "dong_code"])


def fill_missing(df, column, group_column):
    """빈 숫자는 같은 그룹(업종)의 중앙값으로 채운다. 그래도 없으면 전체 중앙값."""
    df[column] = df[column].fillna(df.groupby(group_column)[column].transform("median"))
    df[column] = df[column].fillna(df[column].median())
    return df


def remove_outliers(df, column, group_column):
    """그룹별로 상하위 1%를 이상치로 보고 제거한다."""
    kept = []
    for _, group in df.groupby(group_column):
        low = group[column].quantile(0.01)
        high = group[column].quantile(0.99)
        kept.append(group[(group[column] >= low) & (group[column] <= high)])
    return pd.concat(kept, ignore_index=True)


def merge_tables(store, sales, pop, change):
    """점포를 기준으로 매출·유동인구·변화지표를 붙인다."""
    df = store.merge(
        sales[["quarter", "dong_code", "industry_code", "sales_amount", "sales_count"]],
        on=["quarter", "dong_code", "industry_code"],
        how="left",
    )
    df = df.merge(
        pop[["quarter", "dong_code", "foot_traffic"]],
        on=["quarter", "dong_code"],
        how="left",
    )
    df = df.merge(
        change[["quarter", "dong_code", "change_code", "change_name", "operate_months"]],
        on=["quarter", "dong_code"],
        how="left",
    )

    # 결측치: 매출/유동인구/영업개월은 같은 업종 중앙값
    for column in ["sales_amount", "sales_count", "foot_traffic", "operate_months"]:
        df = fill_missing(df, column, "industry")

    df["change_code"] = df["change_code"].fillna("HH")
    df["change_name"] = df["change_code"].map(CHANGE_NAMES).fillna("정체")

    # 파생 변수: 점포 1개당 매출(만원)
    df["sales_per_store"] = (df["sales_amount"] / df["store_count"]).round(1)

    # 이상치 제거 후, 숫자가 너무 작아지지 않게 점포 수가 3개 이상인 행만 학습에 쓴다.
    df = df[df["store_count"] >= 3]
    df = remove_outliers(df, "sales_per_store", "industry")
    return df.reset_index(drop=True)


def make_dong_stats(train):
    """가장 최근 분기만 남겨, 화면/추천에서 쓰는 행정동×업종 통계를 만든다."""
    latest = train["quarter"].max()
    now = train[train["quarter"] == latest].copy()
    now["median_close_rate"] = now.groupby("dong_code")["close_rate"].transform("median")
    now["median_sales_per_store"] = now.groupby("dong_code")["sales_per_store"].transform("median")
    return now


def make_options(train, semas_dongs, semas_upjong):
    """프론트 선택 상자용 목록. (자치구, 행정동, 업종)"""
    dongs = (
        train[["district", "dong", "dong_code"]]
        .drop_duplicates()
        .sort_values(["district", "dong"])
    )
    industries = (
        train[["industry", "industry_code"]]
        .drop_duplicates()
        .sort_values("industry")
    )
    return {
        "districts": sorted(train["district"].dropna().unique().tolist()),
        "dongs": dongs.to_dict(orient="records"),
        "industries": industries.to_dict(orient="records"),
        "semas_dong_count": len(semas_dongs),
        "semas_upjong_count": len(semas_upjong),
    }


def classify_risk(close_rate, change_code):
    """규칙 기반 위험 단계. (AI 없이도 같은 기준으로 판정한다)

    - 폐업률 8% 이상이거나 상권축소(HL) → 위험
    - 폐업률 4% 이상이거나 다이나믹(LL) → 주의
    - 그 외 → 안정
    """
    if close_rate is None:
        return "unknown"
    if close_rate >= 8 or change_code == "HL":
        return "danger"
    if close_rate >= 4 or change_code == "LL":
        return "warning"
    return "stable"
