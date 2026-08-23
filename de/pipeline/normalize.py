"""Normalize validated rows: canonical area_code, YYYYQn period, dedup."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from . import config


def _period(row: Dict[str, str]) -> str:
    return f"{row['기준_년_코드']}Q{row['기준_분기_코드']}"


def normalize_geometry(staging_csv: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with staging_csv.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not row:
                continue
            rows.append(
                {
                    "area_code": row["상권_코드"].strip(),
                    "area_name": row["상권_코드_명"].strip(),
                    "area_type_code": row.get("상권_구분_코드", "").strip(),
                    "area_type_name": row.get("상권_구분_코드_명", "").strip(),
                    "gu_code": row.get("자치구_코드", "").strip(),
                    "dong_code": row.get("행정동_코드", "").strip(),
                    "centroid_lng": float(row["엑스좌표_값"]),
                    "centroid_lat": float(row["와이좌표_값"]),
                    "area_sqm": float(row["영역_면적"]) if row.get("영역_면적") else None,
                    "base_period": _period(row),
                }
            )
    # dedup by area_code (last wins)
    dedup = {r["area_code"]: r for r in rows}
    return list(dedup.values())


def normalize_stores(staging_csv: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with staging_csv.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not row:
                continue
            rows.append(
                {
                    "area_code": row["상권_코드"].strip(),
                    "service_industry_code": row["서비스_업종_코드"].strip(),
                    "service_industry_name": row.get("서비스_업종_코드_명", "").strip(),
                    "store_count": int(float(row["점포_수"])),
                    "similar_store_count": int(float(row["유사_업종_점포_수"])) if row.get("유사_업종_점포_수") else None,
                    "open_rate": float(row["개업_율"]) if row.get("개업_율") else None,
                    "close_rate": float(row["폐업_률"]) if row.get("폐업_률") else None,
                    "franchise_store_count": int(float(row["프랜차이즈_점포_수"])) if row.get("프랜차이즈_점포_수") else None,
                    "base_period": _period(row),
                }
            )
    dedup = {(r["area_code"], r["base_period"], r["service_industry_code"]): r for r in rows}
    return list(dedup.values())


def normalize_sales(staging_csv: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with staging_csv.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not row:
                continue
            rows.append(
                {
                    "area_code": row["상권_코드"].strip(),
                    "service_industry_code": row["서비스_업종_코드"].strip(),
                    "service_industry_name": row.get("서비스_업종_코드_명", "").strip(),
                    "monthly_sales_amount": int(float(row["당월_매출_금액"])),
                    "weekday_sales_amount": int(float(row["주중_매출_금액"])) if row.get("주중_매출_금액") else None,
                    "weekend_sales_amount": int(float(row["주말_매출_금액"])) if row.get("주말_매출_금액") else None,
                    "base_period": _period(row),
                    "is_estimate": True,
                }
            )
    dedup = {(r["area_code"], r["base_period"], r["service_industry_code"]): r for r in rows}
    return list(dedup.values())


def write_json(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_all(validation_results: List[Dict[str, Any]], run_id: str) -> Dict[str, Path]:
    out: Dict[str, Path] = {}
    staging_root = config.DATA_STAGING / run_id
    for result in validation_results:
        kind = result["kind"]
        staging = Path(result["staging_path"])
        if result["valid_count"] == 0:
            continue
        if kind == "geometry":
            rows = normalize_geometry(staging)
            path = staging_root / "area_zones.normalized.json"
        elif kind == "stores":
            rows = normalize_stores(staging)
            path = staging_root / "area_store_stats.normalized.json"
        else:
            rows = normalize_sales(staging)
            path = staging_root / "area_sales_stats.normalized.json"
        write_json(path, rows)
        out[kind] = path
        result["normalized_count"] = len(rows)
        result["normalized_path"] = str(path)
    return out
