"""전처리가 끝난 행정동×업종 통계를 읽는다."""
import json
from pathlib import Path

STATS_PATH = Path(__file__).resolve().parent.parent / "models" / "dong_stats.json"
OPTIONS_PATH = Path(__file__).resolve().parent.parent / "models" / "options.json"

_rows = None
_options = None


def load_stats():
    global _rows
    if _rows is None:
        _rows = json.loads(STATS_PATH.read_text(encoding="utf-8"))
    return _rows


def load_options():
    global _options
    if _options is None:
        _options = json.loads(OPTIONS_PATH.read_text(encoding="utf-8"))
    return _options


def find_stat(dong, industry):
    """행정동 이름 + 업종 이름으로 한 줄을 찾는다. 없으면 None."""
    for row in load_stats():
        if row["dong"] == dong and row["industry"] == industry:
            return row
    return None


def industries_in_dong(dong):
    """그 행정동에 있는 업종 통계를 모두 돌려준다."""
    return [row for row in load_stats() if row["dong"] == dong]
