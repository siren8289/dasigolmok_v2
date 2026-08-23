"""Compute versioned KPIs into da_kpi_snapshot + JSON sample report."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from . import config
from .db import run_psql


def _sql_str(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, float):
        return str(v)
    if isinstance(v, (int, bool)):
        return str(v) if not isinstance(v, bool) else ("TRUE" if v else "FALSE")
    return "'" + str(v).replace("'", "''") + "'"


def _q(sql: str) -> str:
    return run_psql(sql).strip()


def compute_kpis(pipeline_run_id: str) -> Dict[str, Any]:
    run_psql(f"DELETE FROM da_kpi_snapshot WHERE pipeline_run_id = {_sql_str(pipeline_run_id)};", tuples_only=False)

    metrics: List[Dict[str, Any]] = []

    # Story Registration by region
    reg_rows = _q(
        """
SELECT dr.region_name || '|' || COUNT(*)::text
FROM fact_story_lifecycle f
JOIN dim_region dr ON dr.region_sk = f.region_sk
GROUP BY dr.region_name
ORDER BY COUNT(*) DESC;
"""
    ).splitlines()
    total_stories = 0
    for line in reg_rows:
        if not line:
            continue
        name, cnt = line.split("|", 1)
        total_stories += int(cnt)
        metrics.append(
            {
                "metric_key": "story_registration",
                "grain_label": "region",
                "segment": {"region": name},
                "metric_value": float(cnt),
                "numerator": float(cnt),
                "denominator": None,
            }
        )
    metrics.append(
        {
            "metric_key": "story_registration",
            "grain_label": "all",
            "segment": {},
            "metric_value": float(total_stories),
            "numerator": float(total_stories),
            "denominator": None,
        }
    )

    map_sessions = float(_q("SELECT COUNT(*) FROM fact_user_engagement WHERE event_name = 'map_view';") or 0)
    detail_from_map = float(
        _q(
            "SELECT COUNT(*) FROM fact_user_engagement WHERE event_name = 'story_detail_view' AND source = 'map';"
        )
        or 0
    )
    map_to_detail = (detail_from_map / map_sessions) if map_sessions else None
    metrics.append(
        {
            "metric_key": "map_to_detail",
            "grain_label": "all",
            "segment": {},
            "metric_value": map_to_detail,
            "numerator": detail_from_map,
            "denominator": map_sessions,
        }
    )

    creators = float(_q("SELECT COUNT(DISTINCT user_sk) FROM fact_story_lifecycle WHERE user_sk IS NOT NULL;") or 0)
    users = float(_q("SELECT COUNT(*) FROM dim_user;") or 0)
    participation = (creators / users) if users else None
    metrics.append(
        {
            "metric_key": "participation_rate",
            "grain_label": "all",
            "segment": {},
            "metric_value": participation,
            "numerator": creators,
            "denominator": users,
        }
    )

    shares = float(_q("SELECT COUNT(*) FROM fact_user_engagement WHERE event_name = 'share';") or 0)
    metrics.append(
        {
            "metric_key": "share_count",
            "grain_label": "all",
            "segment": {"channel": "all"},
            "metric_value": shares,
            "numerator": shares,
            "denominator": None,
        }
    )

    approved = float(_q("SELECT COUNT(*) FROM fact_admin_review WHERE after_status = 'APPROVED';") or 0)
    rejected = float(_q("SELECT COUNT(*) FROM fact_admin_review WHERE after_status = 'REJECTED';") or 0)
    denom = approved + rejected
    metrics.append(
        {
            "metric_key": "approval_rate",
            "grain_label": "all",
            "segment": {},
            "metric_value": (approved / denom) if denom else None,
            "numerator": approved,
            "denominator": denom,
        }
    )

    tta = _q(
        "SELECT COALESCE(AVG(hours_to_decision), 0) FROM fact_admin_review WHERE after_status = 'APPROVED';"
    )
    metrics.append(
        {
            "metric_key": "time_to_approve",
            "grain_label": "all",
            "segment": {},
            "metric_value": float(tta or 0),
            "numerator": float(tta or 0),
            "denominator": None,
            "notes": "hours",
        }
    )

    impressions = float(
        _q("SELECT COUNT(*) FROM fact_user_engagement WHERE event_name = 'curation_impression';") or 0
    )
    clicks = float(
        _q(
            "SELECT COUNT(*) FROM fact_user_engagement WHERE event_name = 'story_detail_view' AND source = 'curation';"
        )
        or 0
    )
    metrics.append(
        {
            "metric_key": "curation_ctr",
            "grain_label": "sort_type",
            "segment": {"sort_type": "popular"},
            "metric_value": (clicks / impressions) if impressions else None,
            "numerator": clicks,
            "denominator": impressions,
        }
    )

    approved_total = float(
        _q(
            """
SELECT COUNT(*) FROM fact_story_lifecycle f
JOIN dim_status s ON s.status_sk = f.status_sk
WHERE s.status_code = 'APPROVED';
"""
        )
        or 0
    )
    with_area = float(
        _q(
            """
SELECT COUNT(*) FROM fact_story_lifecycle f
JOIN dim_status s ON s.status_sk = f.status_sk
WHERE s.status_code = 'APPROVED' AND f.has_area_context = TRUE;
"""
        )
        or 0
    )
    metrics.append(
        {
            "metric_key": "area_context_coverage",
            "grain_label": "all",
            "segment": {},
            "metric_value": (with_area / approved_total) if approved_total else None,
            "numerator": with_area,
            "denominator": approved_total,
            "notes": "출처·기준분기는 area join 리포트 참고",
        }
    )

    # Area engagement lift (association only)
    eng_has = float(
        _q(
            """
SELECT COUNT(*)::float / NULLIF((SELECT COUNT(DISTINCT story_id) FROM fact_story_lifecycle WHERE has_area_context), 0)
FROM fact_user_engagement
WHERE event_name IN ('like_toggle', 'share', 'story_detail_view')
  AND has_area_context = TRUE;
"""
        )
        or 0
    )
    eng_no = float(
        _q(
            """
SELECT COUNT(*)::float / NULLIF((SELECT COUNT(DISTINCT story_id) FROM fact_story_lifecycle WHERE NOT has_area_context), 0)
FROM fact_user_engagement
WHERE event_name IN ('like_toggle', 'share', 'story_detail_view')
  AND (has_area_context = FALSE OR has_area_context IS NULL);
"""
        )
        or 0
    )
    lift = (eng_has / eng_no) if eng_no else None
    metrics.append(
        {
            "metric_key": "area_engagement_lift",
            "grain_label": "all",
            "segment": {"interpretation": "association_only"},
            "metric_value": lift,
            "numerator": eng_has,
            "denominator": eng_no,
            "notes": "인과 단정 금지. Area Context 유무와 engagement 연관만 보고.",
        }
    )

    # Area density vs store change proxy (open/close rates) — correlation table
    area_join = _q(
        """
SELECT da.area_code || '|' || da.area_name || '|' || COALESCE(da.area_type_name,'') || '|' ||
       da.base_period || '|' || COUNT(f.story_id)::text || '|' ||
       COALESCE(fac.store_count_total::text,'') || '|' ||
       COALESCE(fac.open_rate_avg::text,'') || '|' ||
       COALESCE(fac.close_rate_avg::text,'') || '|' ||
       fac.source_name || '|' || fac.license_type
FROM fact_story_lifecycle f
JOIN dim_area da ON da.area_sk = f.area_sk
JOIN fact_area_context_snapshot fac ON fac.area_code = da.area_code
JOIN dim_status s ON s.status_sk = f.status_sk AND s.status_code = 'APPROVED'
GROUP BY da.area_code, da.area_name, da.area_type_name, da.base_period,
         fac.store_count_total, fac.open_rate_avg, fac.close_rate_avg, fac.source_name, fac.license_type
ORDER BY COUNT(f.story_id) DESC;
"""
    ).splitlines()

    area_density = []
    for line in area_join:
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) < 10:
            continue
        area_density.append(
            {
                "area_code": parts[0],
                "area_name": parts[1],
                "area_type_name": parts[2],
                "base_period": parts[3],
                "approved_story_count": int(parts[4]),
                "store_count_total": int(parts[5]) if parts[5] else None,
                "open_rate_avg": float(parts[6]) if parts[6] else None,
                "close_rate_avg": float(parts[7]) if parts[7] else None,
                "source_name": parts[8],
                "license_type": parts[9],
                "attribution": f"출처: {parts[8]} · 데이터 기준일: {parts[3]} · {parts[9]}",
                "caveat": "스토리 밀도와 점포 지표의 연관만 관찰. 인과 단정 금지.",
            }
        )

    inserts = []
    for m in metrics:
        inserts.append(
            f"""
INSERT INTO da_kpi_snapshot (
  id, metric_key, grain_label, segment_json, metric_value, numerator, denominator,
  formula_version, computed_at, pipeline_run_id, notes
) VALUES (
  {_sql_str(str(uuid.uuid4()))}, {_sql_str(m['metric_key'])}, {_sql_str(m['grain_label'])},
  {_sql_str(json.dumps(m.get('segment') or {}, ensure_ascii=False))},
  {_sql_str(m.get('metric_value'))}, {_sql_str(m.get('numerator'))}, {_sql_str(m.get('denominator'))},
  {_sql_str(config.FORMULA_VERSION)}, NOW(), {_sql_str(pipeline_run_id)},
  {_sql_str(m.get('notes'))}
);
""".strip()
        )
    if inserts:
        run_psql("BEGIN;\n" + "\n".join(inserts) + "\nCOMMIT;\n", tuples_only=False)

    report = {
        "pipeline_run_id": pipeline_run_id,
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "formula_version": config.FORMULA_VERSION,
        "kpis": metrics,
        "area_context_join": area_density,
        "quality": {
            "idempotent_events": True,
            "user_id": "sha256_masked",
            "null_area_segment": "미매핑",
        },
        "disclaimer": "Area Context 관련 지표는 공공데이터 Context 레이어와의 연관만 나타내며 인과를 주장하지 않습니다.",
    }
    config.REPORTS.mkdir(parents=True, exist_ok=True)
    path = config.REPORTS / f"kpi_{pipeline_run_id}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    report["report_path"] = str(path)
    return report
