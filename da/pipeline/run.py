"""Run DA pipeline: seed events → star build → KPI snapshot/report."""
from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline import config
from pipeline.build_star import build_star
from pipeline.compute_kpi import compute_kpis
from pipeline.seed_events import seed_events


def main() -> int:
    run_id = uuid.uuid4().hex
    print(f"[da] pipeline_run_id={run_id}")
    config.REPORTS.mkdir(parents=True, exist_ok=True)

    n_events = seed_events(run_id)
    print(f"[da] seeded_events={n_events} (idempotent upsert)")

    counts = build_star(run_id)
    print(f"[da] star_counts={counts}")

    report = compute_kpis(run_id)
    print(f"[da] kpi_count={len(report['kpis'])} area_joins={len(report['area_context_join'])}")
    print(f"[da] report={report['report_path']}")

    summary = {
        "status": "SUCCESS",
        "pipeline_run_id": run_id,
        "events_seeded": n_events,
        "star": counts,
        "report_path": report["report_path"],
        "sample_kpis": {
            m["metric_key"]: m.get("metric_value")
            for m in report["kpis"]
            if m.get("grain_label") in {"all", "sort_type"}
        },
    }
    out = config.REPORTS / f"run_{run_id}.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[da] summary={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
