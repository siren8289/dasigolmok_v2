"""DA pipeline config (stdlib)."""
from pathlib import Path

DA_ROOT = Path(__file__).resolve().parents[1]
REPORTS = DA_ROOT / "reports"
FIXTURES = DA_ROOT / "fixtures"
FORMULA_VERSION = "v1"
METRIC_KEYS = [
    "story_registration",
    "map_to_detail",
    "participation_rate",
    "share_count",
    "approval_rate",
    "time_to_approve",
    "curation_ctr",
    "area_context_coverage",
    "area_engagement_lift",
]
