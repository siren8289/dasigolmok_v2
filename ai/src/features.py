"""ML·DL 모델이 함께 쓰는 입력 컬럼 정의.

학습할 때와 예측할 때 컬럼 이름·순서가 같아야 하므로 한 파일에 모아 둔다.
"""
import pandas as pd

# 글자로 된 값(범주형) → 원-핫 인코딩
CATEGORY_COLUMNS = ["district", "industry", "change_code"]
# 숫자로 된 값(수치형)
NUMBER_COLUMNS = ["store_count", "open_rate", "franchise_ratio", "foot_traffic", "operate_months"]

FEATURE_COLUMNS = CATEGORY_COLUMNS + NUMBER_COLUMNS
ML_TARGET = "close_rate"          # ML이 맞히는 값: 폐업률(%)
DL_TARGET = "sales_per_store"     # DL이 맞히는 값: 점포당 매출(만원)


def make_input_frame(district, industry, change_code, store_count, open_rate,
                     franchise_ratio, foot_traffic, operate_months):
    """사용자/통계 값 1건을 모델 입력용 표(1행)로 만든다."""
    return pd.DataFrame([{
        "district": district,
        "industry": industry,
        "change_code": change_code,
        "store_count": store_count,
        "open_rate": open_rate,
        "franchise_ratio": franchise_ratio,
        "foot_traffic": foot_traffic,
        "operate_months": operate_months,
    }])
