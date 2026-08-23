"""Build star schema using Python-side user hashes (no pgcrypto required)."""
from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

from .db import run_psql, run_psql_file


def _sha(user_id: str) -> str:
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()


def _sql_str(v) -> str:
    if v is None:
        return "NULL"
    return "'" + str(v).replace("'", "''") + "'"


def build_star(pipeline_run_id: str) -> dict:
    # Sync dim_user from users with Python sha256 to match event hashes
    users_out = run_psql("SELECT id || '|' || role FROM users;")
    user_stmts = []
    id_to_hash = {}
    for line in users_out.strip().splitlines():
        if not line.strip():
            continue
        uid, role = line.split("|", 1)
        h = _sha(uid)
        id_to_hash[uid] = h
        masked = "ADMIN" if role == "ADMIN" else "USER"
        user_stmts.append(
            f"INSERT INTO dim_user (user_id_hash, role_masked) VALUES ({_sql_str(h)}, {_sql_str(masked)}) "
            f"ON CONFLICT (user_id_hash) DO UPDATE SET role_masked = EXCLUDED.role_masked;"
        )
    if user_stmts:
        run_psql("BEGIN;\n" + "\n".join(user_stmts) + "\nCOMMIT;\n", tuples_only=False)

    # Also include any event hashes
    run_psql(
        """
INSERT INTO dim_user (user_id_hash, role_masked)
SELECT DISTINCT user_id_hash, 'USER' FROM raw_events WHERE user_id_hash IS NOT NULL
ON CONFLICT (user_id_hash) DO NOTHING;
""",
        tuples_only=False,
    )

    # Temp map table for story/reviewer hash joins
    map_rows = [f"({_sql_str(uid)}, {_sql_str(h)})" for uid, h in id_to_hash.items()]
    map_values = ",\n".join(map_rows) if map_rows else "('__none__','__none__')"

    sql = f"""
BEGIN;

CREATE TEMP TABLE tmp_user_hash (user_id VARCHAR(36) PRIMARY KEY, user_id_hash VARCHAR(64) NOT NULL);
INSERT INTO tmp_user_hash (user_id, user_id_hash) VALUES {map_values}
ON CONFLICT DO NOTHING;

INSERT INTO dim_date (date_key, full_date, year, quarter, month, week_of_year, day_of_week)
SELECT DISTINCT
    TO_CHAR(d::date, 'YYYYMMDD')::int,
    d::date,
    EXTRACT(YEAR FROM d)::int,
    EXTRACT(QUARTER FROM d)::int,
    EXTRACT(MONTH FROM d)::int,
    EXTRACT(WEEK FROM d)::int,
    EXTRACT(ISODOW FROM d)::int
FROM (
    SELECT created_at::date AS d FROM stories
    UNION SELECT occurred_at::date FROM raw_events
    UNION SELECT created_at::date FROM review_logs
    UNION SELECT CURRENT_DATE
) src
ON CONFLICT (date_key) DO NOTHING;

INSERT INTO dim_region (region_id, region_name, region_slug)
SELECT id, name, slug FROM regions
ON CONFLICT (region_id) DO UPDATE SET region_name = EXCLUDED.region_name, region_slug = EXCLUDED.region_slug;

INSERT INTO dim_place (place_id, place_name, region_id, area_mapping_segment)
SELECT p.id, p.name, p.region_id,
       CASE WHEN pam.place_id IS NULL THEN '미매핑' ELSE 'mapped' END
FROM places p
LEFT JOIN place_area_mappings pam ON pam.place_id = p.id
ON CONFLICT (place_id) DO UPDATE
SET place_name = EXCLUDED.place_name,
    region_id = EXCLUDED.region_id,
    area_mapping_segment = EXCLUDED.area_mapping_segment;

INSERT INTO dim_tag (tag_id, tag_name, tag_type)
SELECT id, name, type FROM tags
ON CONFLICT (tag_id) DO UPDATE SET tag_name = EXCLUDED.tag_name, tag_type = EXCLUDED.tag_type;

INSERT INTO dim_area (
  area_code, area_name, area_type_name, area_mapping_version,
  standard_unit_zone_version, source_name, source_url, license_type, base_period
)
SELECT
  m.area_code, m.area_name, m.area_type_name, m.area_mapping_version,
  '2024', m.source_name, m.source_url, m.license_type, m.base_period
FROM mart_area_context m
ON CONFLICT (area_code) DO UPDATE SET
  area_name = EXCLUDED.area_name,
  area_type_name = EXCLUDED.area_type_name,
  base_period = EXCLUDED.base_period,
  source_name = EXCLUDED.source_name,
  source_url = EXCLUDED.source_url,
  license_type = EXCLUDED.license_type,
  area_mapping_version = EXCLUDED.area_mapping_version;

DELETE FROM fact_user_engagement;
DELETE FROM fact_admin_review;
DELETE FROM fact_story_lifecycle;
DELETE FROM fact_area_context_snapshot;

INSERT INTO fact_area_context_snapshot (
  area_code, area_sk, base_period, store_count_total, open_rate_avg, close_rate_avg,
  monthly_sales_total, sales_is_estimate, source_name, source_url, license_type,
  fetched_at, area_mapping_version, metric_formula_version
)
SELECT
  m.area_code, da.area_sk, m.base_period, m.store_count_total, m.open_rate_avg, m.close_rate_avg,
  m.monthly_sales_total, m.sales_is_estimate, m.source_name, m.source_url, m.license_type,
  m.fetched_at, m.area_mapping_version, 'v1'
FROM mart_area_context m
JOIN dim_area da ON da.area_code = m.area_code;

INSERT INTO fact_story_lifecycle (
  story_id, region_sk, place_sk, user_sk, status_sk, area_sk,
  register_date_key, approve_date_key, has_area_context, like_count,
  category, period_tag, created_at, approved_at, metric_formula_version
)
SELECT
  s.id,
  dr.region_sk,
  dp.place_sk,
  du.user_sk,
  ds.status_sk,
  da.area_sk,
  TO_CHAR(s.created_at::date, 'YYYYMMDD')::int,
  CASE WHEN rl.approved_at IS NOT NULL THEN TO_CHAR(rl.approved_at::date, 'YYYYMMDD')::int END,
  (pam.place_id IS NOT NULL),
  s.like_count,
  (SELECT t.name FROM story_tags st JOIN tags t ON t.id = st.tag_id WHERE st.story_id = s.id AND t.type = 'THEME' LIMIT 1),
  (SELECT t.name FROM story_tags st JOIN tags t ON t.id = st.tag_id WHERE st.story_id = s.id AND t.type = 'PERIOD' LIMIT 1),
  s.created_at,
  rl.approved_at,
  'v1'
FROM stories s
JOIN dim_region dr ON dr.region_id = s.region_id
LEFT JOIN dim_place dp ON dp.place_id = s.place_id
LEFT JOIN tmp_user_hash th ON th.user_id = s.user_id
LEFT JOIN dim_user du ON du.user_id_hash = th.user_id_hash
JOIN dim_status ds ON ds.status_code = s.status
LEFT JOIN place_area_mappings pam ON pam.place_id = s.place_id
LEFT JOIN dim_area da ON da.area_code = pam.area_code
LEFT JOIN LATERAL (
  SELECT MIN(created_at) AS approved_at
  FROM review_logs r
  WHERE r.story_id = s.id AND r.after_status = 'APPROVED'
) rl ON TRUE
WHERE s.status <> 'DELETED';

INSERT INTO fact_user_engagement (
  engagement_id, event_id, event_name, date_key, region_sk, story_id, user_sk,
  area_sk, has_area_context, source, channel, sort_type, occurred_at, metric_formula_version
)
SELECT
  e.event_id,
  e.event_id,
  e.event_name,
  TO_CHAR(e.occurred_at::date, 'YYYYMMDD')::int,
  dr.region_sk,
  e.story_id,
  du.user_sk,
  da.area_sk,
  e.has_area_context,
  e.source,
  e.channel,
  e.sort_type,
  e.occurred_at,
  'v1'
FROM raw_events e
LEFT JOIN dim_region dr ON dr.region_id = e.region_id
LEFT JOIN dim_user du ON du.user_id_hash = e.user_id_hash
LEFT JOIN dim_area da ON da.area_code = e.area_code
WHERE e.event_name IN (
  'map_view', 'story_detail_view', 'like_toggle', 'share',
  'curation_impression', 'area_context_view', 'story_register'
);

INSERT INTO fact_admin_review (
  review_id, story_id, date_key, before_status, after_status, reviewer_user_sk,
  hours_to_decision, occurred_at, metric_formula_version
)
SELECT
  r.id,
  r.story_id,
  TO_CHAR(r.created_at::date, 'YYYYMMDD')::int,
  r.before_status,
  r.after_status,
  du.user_sk,
  EXTRACT(EPOCH FROM (r.created_at - s.created_at)) / 3600.0,
  r.created_at,
  'v1'
FROM review_logs r
JOIN stories s ON s.id = r.story_id
LEFT JOIN tmp_user_hash th ON th.user_id = r.reviewer_id
LEFT JOIN dim_user du ON du.user_id_hash = th.user_id_hash;

COMMIT;
"""
    with tempfile.NamedTemporaryFile("w", suffix=".sql", delete=False, encoding="utf-8") as tmp:
        tmp.write(sql)
        path = tmp.name
    run_psql_file(path)
    Path(path).unlink(missing_ok=True)

    counts = {
        "fact_story_lifecycle": int(run_psql("SELECT COUNT(*) FROM fact_story_lifecycle;") or 0),
        "fact_user_engagement": int(run_psql("SELECT COUNT(*) FROM fact_user_engagement;") or 0),
        "fact_admin_review": int(run_psql("SELECT COUNT(*) FROM fact_admin_review;") or 0),
        "fact_area_context_snapshot": int(run_psql("SELECT COUNT(*) FROM fact_area_context_snapshot;") or 0),
        "dim_area": int(run_psql("SELECT COUNT(*) FROM dim_area;") or 0),
    }
    return counts
