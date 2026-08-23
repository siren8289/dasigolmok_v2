"""Schema/range validation with quarantine for failed rows."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from . import config


def _to_float(value: str | None):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _to_int(value: str | None):
    if value is None or value == "":
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def _period(row: Dict[str, str]) -> Tuple[str | None, int | None]:
    year = _to_int(row.get("기준_년_코드"))
    quarter = _to_int(row.get("기준_분기_코드"))
    if year is None or quarter is None:
        return None, year
    if quarter < 1 or quarter > 4:
        return None, year
    return f"{year}Q{quarter}", year


def validate_geometry(row: Dict[str, str]) -> Tuple[bool, str | None]:
    if not row.get("상권_코드"):
        return False, "missing_key"
    period, year = _period(row)
    if period is None:
        return False, "missing_key"
    if year is not None and year < config.MIN_YEAR:
        return False, "out_of_range"
    lng = _to_float(row.get("엑스좌표_값"))
    lat = _to_float(row.get("와이좌표_값"))
    if lng is None or lat is None:
        return False, "missing_key"
    if not (-180 <= lng <= 180 and -90 <= lat <= 90):
        return False, "out_of_range"
    area = _to_float(row.get("영역_면적"))
    if area is not None and area < 0:
        return False, "out_of_range"
    return True, None


def validate_stores(row: Dict[str, str]) -> Tuple[bool, str | None]:
    if not row.get("상권_코드") or not row.get("서비스_업종_코드"):
        return False, "missing_key"
    period, year = _period(row)
    if period is None:
        return False, "missing_key"
    if year is not None and year < config.MIN_YEAR:
        return False, "out_of_range"
    if _to_int(row.get("점포_수")) is None:
        return False, "missing_key"
    open_rate = _to_float(row.get("개업_율"))
    close_rate = _to_float(row.get("폐업_률"))
    for rate in (open_rate, close_rate):
        if rate is not None and not (0 <= rate <= 100):
            return False, "out_of_range"
    return True, None


def validate_sales(row: Dict[str, str]) -> Tuple[bool, str | None]:
    if not row.get("상권_코드") or not row.get("서비스_업종_코드"):
        return False, "missing_key"
    period, year = _period(row)
    if period is None:
        return False, "missing_key"
    if year is not None and year < config.MIN_YEAR:
        return False, "out_of_range"
    amount = _to_int(row.get("당월_매출_금액"))
    if amount is None:
        return False, "missing_key"
    if amount < 0:
        return False, "out_of_range"
    return True, None


VALIDATORS = {
    "geometry": validate_geometry,
    "stores": validate_stores,
    "sales": validate_sales,
}


def validate_snapshot(snap: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    kind = snap["kind"]
    validator = VALIDATORS[kind]
    src = Path(snap["storage_path"])
    q_dir = config.DATA_QUARANTINE / run_id
    s_dir = config.DATA_STAGING / run_id
    q_dir.mkdir(parents=True, exist_ok=True)
    s_dir.mkdir(parents=True, exist_ok=True)

    ok_rows: List[Dict[str, str]] = []
    bad_rows: List[Dict[str, Any]] = []

    with src.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for row in reader:
            passed, reason = validator(row)
            if passed:
                ok_rows.append(row)
            else:
                bad = dict(row)
                bad["quarantine_reason"] = reason or "schema_drift"
                bad_rows.append(bad)

    staging_path = s_dir / f"{snap['source_dataset']}.valid.csv"
    quarantine_path = q_dir / f"{snap['source_dataset']}.quarantine.csv"

    if ok_rows:
        with staging_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ok_rows)
    else:
        staging_path.write_text("", encoding="utf-8")

    if bad_rows:
        q_fields = list(fieldnames) + ["quarantine_reason"]
        with quarantine_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=q_fields)
            writer.writeheader()
            writer.writerows(bad_rows)

    total = len(ok_rows) + len(bad_rows)
    return {
        "source_dataset": snap["source_dataset"],
        "kind": kind,
        "raw_count": snap["row_count"],
        "valid_count": len(ok_rows),
        "quarantine_count": len(bad_rows),
        "schema_pass_rate": (len(ok_rows) / total) if total else 1.0,
        "staging_path": str(staging_path),
        "quarantine_path": str(quarantine_path) if bad_rows else None,
    }
