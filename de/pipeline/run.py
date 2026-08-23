"""Run DE pipeline: ingest → validate → normalize → DQ → mart load."""
from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Allow `python -m pipeline.run` from de/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline import config
from pipeline.dq import evaluate
from pipeline.ingest import ingest_fixtures
from pipeline.load_mart import load_all
from pipeline.normalize import normalize_all
from pipeline.validate import validate_snapshot


def main() -> int:
    run_id = uuid.uuid4().hex  # fits VARCHAR(36)
    fetched_at = datetime.now(timezone.utc)
    print(f"[de] pipeline_run_id={run_id}")

    for d in (config.DATA_RAW, config.DATA_QUARANTINE, config.DATA_STAGING, config.REPORTS):
        d.mkdir(parents=True, exist_ok=True)

    snapshots = ingest_fixtures(run_id, fetched_at)
    print(f"[de] ingested snapshots={len(snapshots)}")

    validation_results = [validate_snapshot(snap, run_id) for snap in snapshots]
    for v in validation_results:
        print(
            f"[de] validate {v['source_dataset']}: valid={v['valid_count']} "
            f"quarantine={v['quarantine_count']} schema_pass={v['schema_pass_rate']:.2%}"
        )

    normalized_paths = normalize_all(validation_results, run_id)
    print(f"[de] normalized kinds={list(normalized_paths.keys())}")

    dq_report = evaluate(validation_results, normalized_paths, run_id)
    print(f"[de] dq_passed={dq_report['passed']} report={dq_report['report_path']}")

    # Soft schema warnings from intentional fixture quarantine must not block mart
    # if normalized geometry/stores/sales are present and hard checks passed.
    hard_failed = any(
        (not c.get("passed", True)) and c.get("metric") in {"completeness", "uniqueness", "freshness"}
        for c in dq_report["checks"]
    )
    if hard_failed or "geometry" not in normalized_paths:
        print("[de] HARD DQ failure — mart load blocked (Story path unaffected)")
        summary = {"status": "BLOCKED", "pipeline_run_id": run_id, "dq": dq_report}
        out = config.REPORTS / f"run_{run_id}.json"
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        return 1

    load_stats = load_all(
        run_id=run_id,
        snapshots=snapshots,
        normalized_paths=normalized_paths,
        dq_report=dq_report,
        fetched_at_iso=fetched_at.isoformat(),
    )
    print(f"[de] mart_loaded={load_stats}")

    summary = {
        "status": "SUCCESS",
        "pipeline_run_id": run_id,
        "area_mapping_version": config.AREA_MAPPING_VERSION,
        "validation": validation_results,
        "dq": dq_report,
        "load": load_stats,
        "lineage_sample": {
            "source_name": snapshots[0]["source_name"],
            "source_url": snapshots[0]["source_url"],
            "base_period": snapshots[0]["base_period"],
            "fetched_at": snapshots[0]["fetched_at"],
            "checksum_sha256": snapshots[0]["checksum_sha256"],
            "license_type": snapshots[0]["license_type"],
        },
    }
    out = config.REPORTS / f"run_{run_id}.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[de] summary={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
