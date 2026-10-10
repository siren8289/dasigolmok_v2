"""두 가지 메인 기능의 실제 계산을 담당한다.

1. diagnose  : 골목 상권 진단 (규칙 + ML 폐업률 + DL 매출 + LLM 설명)
2. recommend : 같은 동의 업종을 점수 순으로 추천
"""
import pandas as pd

from src.dong_stats import find_stat, industries_in_dong, load_options
from src.dl_model import predict_dl
from src.features import make_input_frame
from src.llm_explain import explain
from src.ml_model import predict_ml
from src.risk import classify


def _frame_from_stat(stat):
    return make_input_frame(
        stat["district"],
        stat["industry"],
        stat["change_code"],
        stat["store_count"],
        stat["open_rate"],
        stat["franchise_ratio"],
        stat["foot_traffic"],
        stat["operate_months"],
    )


def diagnose(request):
    """request: 사용자가 고른 행정동·업종"""
    stat = find_stat(request["dong"], request["industry"])
    if stat is None:
        return {"error": "해당 행정동·업종 데이터가 없습니다."}

    frame = _frame_from_stat(stat)
    ml_close = predict_ml(frame)[0]
    dl_sales = predict_dl(frame)[0]

    # 규칙은 '실제 최근 폐업률'로, 단계는 ML 예측 폐업률도 함께 보여 준다.
    status, is_danger = classify(stat["close_rate"], stat["change_code"])

    result = {
        "district": stat["district"],
        "dong": stat["dong"],
        "industry": stat["industry"],
        "quarter": stat["quarter"],
        "store_count": stat["store_count"],
        "open_rate": stat["open_rate"],
        "close_rate": stat["close_rate"],
        "franchise_ratio": stat["franchise_ratio"],
        "foot_traffic": stat["foot_traffic"],
        "change_code": stat["change_code"],
        "change_name": stat["change_name"],
        "operate_months": stat["operate_months"],
        "sales_per_store": stat["sales_per_store"],
        "ml_close_rate": ml_close,
        "dl_sales_per_store": dl_sales,
        "status": status,
        "is_danger": is_danger,
    }
    explanation, source = explain(request, result)
    result["explanation"] = explanation
    result["explanation_source"] = source
    return result


def recommend(request, limit=5):
    """같은 행정동의 업종을 모아, 예상 폐업률이 낮고 매출이 높은 순으로 보여 준다."""
    rows = industries_in_dong(request["dong"])
    if not rows:
        return {"error": "해당 행정동 데이터가 없습니다.", "recommendations": []}

    frame = pd.concat([_frame_from_stat(row) for row in rows], ignore_index=True)
    ml_closes = predict_ml(frame)
    dl_sales = predict_dl(frame)

    items = []
    for row, close, sales in zip(rows, ml_closes, dl_sales):
        status, is_danger = classify(close, row["change_code"])
        # 점수가 높을수록 추천. 폐업률이 낮고, 매출이 높을수록 좋다.
        score = round(sales / 100 - close * 8, 1)
        items.append({
            "industry": row["industry"],
            "store_count": row["store_count"],
            "close_rate": row["close_rate"],
            "ml_close_rate": close,
            "dl_sales_per_store": sales,
            "change_name": row["change_name"],
            "status": status,
            "is_danger": is_danger,
            "score": score,
        })

    items.sort(key=lambda item: item["score"], reverse=True)
    return {
        "district": rows[0]["district"],
        "dong": request["dong"],
        "change_name": rows[0]["change_name"],
        "recommendations": items[:limit],
        "all_industries": items,
    }


def options():
    return load_options()
