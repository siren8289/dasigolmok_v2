"""Ingest fixture/OpenAPI snapshots into immutable raw storage with checksum."""
from __future__ import annotations

import hashlib
import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from . import config


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _period_from_rows(csv_path: Path) -> str:
    import csv

    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = row.get("기준_년_코드") or row.get("base_year")
            quarter = row.get("기준_분기_코드") or row.get("base_quarter")
            if year and quarter:
                return f"{year}Q{quarter}"
    return "UNKNOWN"


def ingest_fixtures(run_id: str, fetched_at: datetime | None = None) -> List[Dict[str, Any]]:
    fetched_at = fetched_at or datetime.now(timezone.utc)
    run_dir = config.DATA_RAW / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    snapshots: List[Dict[str, Any]] = []

    for dataset_id, meta in config.DATASETS.items():
        src = config.FIXTURES / meta["fixture"]
        if not src.exists():
            raise FileNotFoundError(f"Missing fixture: {src}")
        dest = run_dir / f"{dataset_id}.csv"
        shutil.copy2(src, dest)
        checksum = _sha256(dest)
        base_period = _period_from_rows(dest)
        with dest.open(encoding="utf-8") as f:
            row_count = max(sum(1 for _ in f) - 1, 0)
        snap = {
            "id": str(uuid.uuid4()),
            "pipeline_run_id": run_id,
            "source_name": meta["name"],
            "source_dataset": dataset_id,
            "source_url": meta["source_url"],
            "base_period": base_period,
            "license_type": meta["license_type"],
            "fetched_at": fetched_at.isoformat(),
            "checksum_sha256": checksum,
            "storage_path": str(dest),
            "row_count": row_count,
            "kind": meta["kind"],
        }
        snapshots.append(snap)

    meta_path = run_dir / "snapshots.json"
    meta_path.write_text(json.dumps(snapshots, ensure_ascii=False, indent=2), encoding="utf-8")
    return snapshots
