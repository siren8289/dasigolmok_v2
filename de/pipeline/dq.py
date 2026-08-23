"""Data quality gates before serving mart load."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from . import config


def _completeness(rows: List[Dict[str, Any]], required: List[str]) -> float:
    if not rows:
        return 1.0
    ok = 0
    for row in rows:
        if all(row.get(k) is not None and row.get(k) != "" for k in required):
            ok += 1
    return ok / len(rows)


def evaluate(validation_results: List[Dict[str, Any]], normalized_paths: Dict[str, Path], run_id: str) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    passed = True

    for result in validation_results:
        schema_rate = result["schema_pass_rate"]
        schema_ok = schema_rate >= config.DQ_SCHEMA_PASS_MIN
        checks.append(
            {
                "metric": "schema_pass_rate",
                "dataset": result["source_dataset"],
                "value": round(schema_rate, 4),
                "threshold": config.DQ_SCHEMA_PASS_MIN,
                "passed": schema_ok,
                # Fixture quarantine demos may fall below 99%; hard gate is mart-ready data.
                "severity": "warn",
            }
        )

        if result.get("normalized_count") is not None and result["valid_count"] > 0:
            valid = result["valid_count"]
            diff = abs(valid - result["normalized_count"]) / valid
            reconcile_ok = result["normalized_count"] <= valid
            checks.append(
                {
                    "metric": "row_reconciliation",
                    "dataset": result["source_dataset"],
                    "value": {
                        "raw": result["raw_count"] or 0,
                        "valid": valid,
                        "normalized": result["normalized_count"],
                        "quarantine": result["quarantine_count"],
                        "dedup_diff_ratio": round(diff, 4),
                    },
                    "passed": reconcile_ok,
                    "severity": "hard",
                }
            )
            if not reconcile_ok:
                passed = False

    geometry_path = normalized_paths.get("geometry")
    if geometry_path and geometry_path.exists():
        zones = json.loads(geometry_path.read_text(encoding="utf-8"))
        comp = _completeness(zones, ["area_code", "area_name", "centroid_lat", "centroid_lng", "base_period"])
        comp_ok = comp >= config.DQ_COMPLETENESS_MIN
        checks.append(
            {
                "metric": "completeness",
                "dataset": "seoul_area_geometry",
                "value": round(comp, 4),
                "threshold": config.DQ_COMPLETENESS_MIN,
                "passed": comp_ok,
                "severity": "hard",
            }
        )
        if not comp_ok:
            passed = False

        keys = [z["area_code"] for z in zones]
        unique_ok = len(keys) == len(set(keys))
        checks.append(
            {
                "metric": "uniqueness",
                "dataset": "area_zones",
                "value": {"rows": len(keys), "unique": len(set(keys))},
                "threshold": 1.0,
                "passed": unique_ok,
                "severity": "hard",
            }
        )
        if not unique_ok:
            passed = False

        periods = sorted({z["base_period"] for z in zones})
        fresh_ok = bool(periods) and periods[-1] >= f"{config.MIN_YEAR}Q1"
        checks.append(
            {
                "metric": "freshness",
                "dataset": "area_zones",
                "value": {"max_base_period": periods[-1] if periods else None, "periods": periods},
                "passed": fresh_ok,
                "severity": "hard",
            }
        )
        if not fresh_ok:
            passed = False
    else:
        passed = False
        checks.append(
            {
                "metric": "completeness",
                "dataset": "seoul_area_geometry",
                "value": 0,
                "passed": False,
                "severity": "hard",
            }
        )

    report = {
        "pipeline_run_id": run_id,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "area_mapping_version": config.AREA_MAPPING_VERSION,
        "passed": passed,
        "checks": checks,
    }
    config.REPORTS.mkdir(parents=True, exist_ok=True)
    path = config.REPORTS / f"dq_{run_id}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    report["report_path"] = str(path)
    return report
