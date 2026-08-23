"""Load normalized DE mart into Postgres via psql (stdlib + psql client)."""
from __future__ import annotations

import json
import math
import os
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from . import config


def _sql_str(value: Optional[str]) -> str:
    if value is None:
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def _sql_num(value) -> str:
    if value is None:
        return "NULL"
    return str(value)


def _haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _psql_env() -> Dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PGHOST", "localhost")
    env.setdefault("PGPORT", env.get("DB_PORT", "5432"))
    env.setdefault("PGUSER", env.get("DB_USERNAME", "app_user"))
    env.setdefault("PGPASSWORD", env.get("DB_PASSWORD", "app_password"))
    env.setdefault("PGDATABASE", env.get("DB_NAME", "dasi_golmok"))
    return env


def run_psql(sql: str) -> str:
    env = _psql_env()
    result = subprocess.run(
        ["psql", "-v", "ON_ERROR_STOP=1", "-At", "-c", sql],
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"psql failed: {result.stderr}\nSQL excerpt: {sql[:400]}")
    return result.stdout


def build_mart_context(
    zones: List[Dict[str, Any]],
    stores: List[Dict[str, Any]],
    sales: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    store_by_area: Dict[str, List[Dict[str, Any]]] = {}
    for s in stores:
        store_by_area.setdefault(s["area_code"], []).append(s)
    sales_by_area: Dict[str, List[Dict[str, Any]]] = {}
    for s in sales:
        sales_by_area.setdefault(s["area_code"], []).append(s)

    mart: List[Dict[str, Any]] = []
    for z in zones:
        code = z["area_code"]
        srows = store_by_area.get(code, [])
        salrows = sales_by_area.get(code, [])
        open_rates = [r["open_rate"] for r in srows if r.get("open_rate") is not None]
        close_rates = [r["close_rate"] for r in srows if r.get("close_rate") is not None]
        mart.append(
            {
                "area_code": code,
                "area_name": z["area_name"],
                "area_type_name": z.get("area_type_name"),
                "base_period": z["base_period"],
                "store_count_total": sum(r["store_count"] for r in srows) if srows else 0,
                "open_rate_avg": (sum(open_rates) / len(open_rates)) if open_rates else None,
                "close_rate_avg": (sum(close_rates) / len(close_rates)) if close_rates else None,
                "monthly_sales_total": sum(r["monthly_sales_amount"] for r in salrows) if salrows else None,
                "sales_is_estimate": True,
            }
        )
    return mart


def load_all(
    run_id: str,
    snapshots: List[Dict[str, Any]],
    normalized_paths: Dict[str, Path],
    dq_report: Dict[str, Any],
    fetched_at_iso: str,
) -> Dict[str, Any]:
    zones = json.loads(normalized_paths["geometry"].read_text(encoding="utf-8"))
    stores = json.loads(normalized_paths["stores"].read_text(encoding="utf-8")) if "stores" in normalized_paths else []
    sales = json.loads(normalized_paths["sales"].read_text(encoding="utf-8")) if "sales" in normalized_paths else []
    mart = build_mart_context(zones, stores, sales)

    snap_by_kind = {s["kind"]: s for s in snapshots}
    geom_meta = snap_by_kind["geometry"]
    store_meta = snap_by_kind.get("stores", geom_meta)
    sales_meta = snap_by_kind.get("sales", geom_meta)

    statements: List[str] = []
    statements.append(
        f"""
INSERT INTO de_pipeline_runs (
  id, started_at, finished_at, status, area_mapping_version, schema_version,
  standard_unit_zone_version, source_snapshot_dir, dq_report_path, notes
) VALUES (
  {_sql_str(run_id)}, NOW(), NULL, 'RUNNING',
  {_sql_str(config.AREA_MAPPING_VERSION)}, {_sql_str(config.SCHEMA_VERSION)},
  {_sql_str(config.STANDARD_UNIT_ZONE_VERSION)},
  {_sql_str(str(config.DATA_RAW / run_id))},
  {_sql_str(dq_report.get('report_path'))},
  'fixture ingest MVP'
) ON CONFLICT (id) DO NOTHING;
""".strip()
    )

    for snap in snapshots:
        statements.append(
            f"""
INSERT INTO de_raw_snapshots (
  id, pipeline_run_id, source_name, source_dataset, source_url, base_period,
  license_type, fetched_at, checksum_sha256, storage_path, row_count
) VALUES (
  {_sql_str(snap['id'])}, {_sql_str(run_id)}, {_sql_str(snap['source_name'])},
  {_sql_str(snap['source_dataset'])}, {_sql_str(snap['source_url'])},
  {_sql_str(snap['base_period'])}, {_sql_str(snap['license_type'])},
  {_sql_str(snap['fetched_at'])}::timestamptz, {_sql_str(snap['checksum_sha256'])},
  {_sql_str(snap['storage_path'])}, {snap['row_count']}
) ON CONFLICT DO NOTHING;
""".strip()
        )

    # Replace serving tables for idempotent re-run of same mapping version
    statements.append("DELETE FROM place_area_mappings;")
    statements.append("DELETE FROM mart_area_context;")
    statements.append("DELETE FROM area_sales_stats;")
    statements.append("DELETE FROM area_store_stats;")
    statements.append("DELETE FROM area_zones;")

    for z in zones:
        statements.append(
            f"""
INSERT INTO area_zones (
  area_code, area_name, area_type_code, area_type_name, gu_code, dong_code,
  centroid_lng, centroid_lat, area_sqm, area_mapping_version,
  source_dataset, source_url, base_period, fetched_at, pipeline_run_id, license_type
) VALUES (
  {_sql_str(z['area_code'])}, {_sql_str(z['area_name'])},
  {_sql_str(z.get('area_type_code'))}, {_sql_str(z.get('area_type_name'))},
  {_sql_str(z.get('gu_code'))}, {_sql_str(z.get('dong_code'))},
  {z['centroid_lng']}, {z['centroid_lat']}, {_sql_num(z.get('area_sqm'))},
  {_sql_str(config.AREA_MAPPING_VERSION)},
  {_sql_str(geom_meta['source_dataset'])}, {_sql_str(geom_meta['source_url'])},
  {_sql_str(z['base_period'])}, {_sql_str(fetched_at_iso)}::timestamptz,
  {_sql_str(run_id)}, {_sql_str(geom_meta['license_type'])}
);
""".strip()
        )

    for s in stores:
        statements.append(
            f"""
INSERT INTO area_store_stats (
  id, area_code, service_industry_code, service_industry_name, store_count,
  similar_store_count, open_rate, close_rate, franchise_store_count,
  base_period, area_mapping_version, source_dataset, source_url,
  fetched_at, pipeline_run_id, license_type
) VALUES (
  {_sql_str(str(uuid.uuid4()))}, {_sql_str(s['area_code'])},
  {_sql_str(s['service_industry_code'])}, {_sql_str(s.get('service_industry_name'))},
  {s['store_count']}, {_sql_num(s.get('similar_store_count'))},
  {_sql_num(s.get('open_rate'))}, {_sql_num(s.get('close_rate'))},
  {_sql_num(s.get('franchise_store_count'))}, {_sql_str(s['base_period'])},
  {_sql_str(config.AREA_MAPPING_VERSION)},
  {_sql_str(store_meta['source_dataset'])}, {_sql_str(store_meta['source_url'])},
  {_sql_str(fetched_at_iso)}::timestamptz, {_sql_str(run_id)},
  {_sql_str(store_meta['license_type'])}
);
""".strip()
        )

    for s in sales:
        statements.append(
            f"""
INSERT INTO area_sales_stats (
  id, area_code, service_industry_code, service_industry_name,
  monthly_sales_amount, weekday_sales_amount, weekend_sales_amount,
  base_period, is_estimate, area_mapping_version, source_dataset, source_url,
  fetched_at, pipeline_run_id, license_type
) VALUES (
  {_sql_str(str(uuid.uuid4()))}, {_sql_str(s['area_code'])},
  {_sql_str(s['service_industry_code'])}, {_sql_str(s.get('service_industry_name'))},
  {s['monthly_sales_amount']}, {_sql_num(s.get('weekday_sales_amount'))},
  {_sql_num(s.get('weekend_sales_amount'))}, {_sql_str(s['base_period'])},
  TRUE, {_sql_str(config.AREA_MAPPING_VERSION)},
  {_sql_str(sales_meta['source_dataset'])}, {_sql_str(sales_meta['source_url'])},
  {_sql_str(fetched_at_iso)}::timestamptz, {_sql_str(run_id)},
  {_sql_str(sales_meta['license_type'])}
);
""".strip()
        )

    for m in mart:
        statements.append(
            f"""
INSERT INTO mart_area_context (
  area_code, area_name, area_type_name, base_period, store_count_total,
  open_rate_avg, close_rate_avg, monthly_sales_total, sales_is_estimate,
  area_mapping_version, source_dataset, source_url, source_name,
  fetched_at, pipeline_run_id, license_type, updated_at
) VALUES (
  {_sql_str(m['area_code'])}, {_sql_str(m['area_name'])},
  {_sql_str(m.get('area_type_name'))}, {_sql_str(m['base_period'])},
  {_sql_num(m.get('store_count_total'))}, {_sql_num(m.get('open_rate_avg'))},
  {_sql_num(m.get('close_rate_avg'))}, {_sql_num(m.get('monthly_sales_total'))},
  TRUE, {_sql_str(config.AREA_MAPPING_VERSION)},
  {_sql_str(geom_meta['source_dataset'])}, {_sql_str(geom_meta['source_url'])},
  {_sql_str(geom_meta['source_name'])},
  {_sql_str(fetched_at_iso)}::timestamptz, {_sql_str(run_id)},
  {_sql_str(geom_meta['license_type'])}, NOW()
);
""".strip()
        )

    # Place → Area mapping (Seoul bbox only)
    places_out = run_psql(
        "SELECT id || '|' || COALESCE(latitude::text,'') || '|' || COALESCE(longitude::text,'') FROM places;"
    )
    mapped = 0
    eligible = 0
    min_lng, min_lat, max_lng, max_lat = config.SEOUL_BBOX
    for line in places_out.strip().splitlines():
        if not line.strip():
            continue
        place_id, lat_s, lng_s = line.split("|", 2)
        if not lat_s or not lng_s:
            continue
        lat, lng = float(lat_s), float(lng_s)
        if not (min_lat <= lat <= max_lat and min_lng <= lng <= max_lng):
            continue
        eligible += 1
        best: Optional[Tuple[str, float]] = None
        for z in zones:
            dist = _haversine_m(lat, lng, z["centroid_lat"], z["centroid_lng"])
            if best is None or dist < best[1]:
                best = (z["area_code"], dist)
        if best and best[1] <= config.MAPPING_MAX_DISTANCE_M:
            statements.append(
                f"""
INSERT INTO place_area_mappings (place_id, area_code, area_mapping_version, distance_m, mapped_at, pipeline_run_id)
VALUES ({_sql_str(place_id)}, {_sql_str(best[0])}, {_sql_str(config.AREA_MAPPING_VERSION)},
        {best[1]}, NOW(), {_sql_str(run_id)});
""".strip()
            )
            mapped += 1

    coverage = (mapped / eligible) if eligible else None
    statements.append(
        f"""
UPDATE de_pipeline_runs
SET finished_at = NOW(), status = 'SUCCESS',
    notes = {_sql_str(f'mapped={mapped}/{eligible} coverage={coverage}')}
WHERE id = {_sql_str(run_id)};
""".strip()
    )

    with tempfile.NamedTemporaryFile("w", suffix=".sql", delete=False, encoding="utf-8") as tmp:
        tmp.write("BEGIN;\n")
        tmp.write("\n".join(statements))
        tmp.write("\nCOMMIT;\n")
        sql_path = tmp.name

    env = _psql_env()
    result = subprocess.run(
        ["psql", "-v", "ON_ERROR_STOP=1", "-f", sql_path],
        env=env,
        capture_output=True,
        text=True,
    )
    Path(sql_path).unlink(missing_ok=True)
    if result.returncode != 0:
        raise RuntimeError(f"mart load failed: {result.stderr}")

    return {
        "zones": len(zones),
        "stores": len(stores),
        "sales": len(sales),
        "mart": len(mart),
        "mapping_eligible": eligible,
        "mapping_mapped": mapped,
        "mapping_coverage": coverage,
    }
