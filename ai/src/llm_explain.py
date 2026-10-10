"""LLM(Gemini)으로 진단 결과를 쉬운 문장으로 설명한다.

GEMINI_API_KEY 가 없거나 호출에 실패하면 미리 정한 기본 문장을 쓴다.
"""
import os

STATUS_NAMES = {"stable": "안정", "warning": "주의", "danger": "위험", "unknown": "판단 불가"}
CHANGE_NAMES = {"HH": "정체", "HL": "상권축소", "LH": "상권확장", "LL": "다이나믹"}


def basic_explanation(result):
    """LLM 없이 만드는 기본 설명"""
    status = STATUS_NAMES[result["status"]]
    return (
        f"{result['dong']} {result['industry']} 상권은 '{status}' 단계입니다. "
        f"최근 폐업률은 {result['close_rate']}%이고, AI가 예상한 폐업률은 {result['ml_close_rate']}%입니다. "
        f"점포당 예상 매출은 약 {result['dl_sales_per_store']}만원입니다. "
        "이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다."
    )


def make_prompt(request, result):
    return "\n".join([
        "너는 서울 골목 상권 상담 도우미다.",
        "아래 진단 결과를 보고 사장님에게 3문장 이내의 쉬운 한국어로 설명하고, 현실적인 조언 1개를 덧붙여라.",
        "숫자는 그대로 인용하고, 투자 권유나 단정적인 표현은 하지 마라.",
        "",
        f"행정동: {request['dong']} ({request['district']})",
        f"업종: {request['industry']}",
        f"상권변화: {CHANGE_NAMES.get(result['change_code'], result['change_code'])}",
        f"최근 점포 수: {result['store_count']} / 폐업률: {result['close_rate']}%",
        f"ML 예상 폐업률: {result['ml_close_rate']}%",
        f"DL 예상 점포당 매출: {result['dl_sales_per_store']}만원",
        f"위험 단계: {STATUS_NAMES[result['status']]}",
    ])


def explain(request, result):
    """(설명 문장, 출처) 를 돌려준다. 출처는 "gemini" 또는 "basic"."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return basic_explanation(result), "basic"

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=15000),
        )
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=make_prompt(request, result),
        )
        if response.text:
            return response.text.strip(), "gemini"
    except Exception as error:
        print("Gemini 호출 실패, 기본 설명을 사용합니다:", type(error).__name__)

    return basic_explanation(result), "basic"
