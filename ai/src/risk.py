"""규칙 기반 위험 단계.

폐업률과 상권변화지표만 보고 단계를 나눈다.
  - 8% 이상이거나 상권축소(HL) → 위험 (danger)
  - 4% 이상이거나 다이나믹(LL) → 주의 (warning)
  - 그 외 → 안정 (stable)
"""

SAFE_CLOSE = 4
DANGER_CLOSE = 8


def classify(close_rate, change_code):
    """(상태, 위험 여부) 를 돌려준다."""
    if close_rate is None:
        return "unknown", False
    if close_rate >= DANGER_CLOSE or change_code == "HL":
        return "danger", True
    if close_rate >= SAFE_CLOSE or change_code == "LL":
        return "warning", False
    return "stable", False
