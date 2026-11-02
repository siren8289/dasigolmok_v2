#!/usr/bin/env python3
"""실행 결과 JSON을 케이스 카드와 섹션 README에 반영한다."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / "qa"


def load_cases(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data["cases"] if isinstance(data, dict) else data
    for row in cases:
        if row["status"] not in {"PASS", "FAIL", "RISK"}:
            raise SystemExit(f"bad status {row}")
        if row["status"] == "FAIL" and not row.get("defect_id"):
            row["defect_id"] = "DEF-" + row["id"]
        if row["status"] != "FAIL":
            row["defect_id"] = ""
    return cases


def patch_case(section: str, row: dict) -> None:
    path = QA / section / row["id"] / "case.md"
    text = path.read_text(encoding="utf-8")
    evidence = (row.get("evidence") or "—").replace("\n", " ")
    defect = row.get("defect_id") or "—"
    text2, n = re.subn(
        r"\| 실행 상태 \(O\) \| .* \|",
        f"| 실행 상태 (O) | {row['status']} |",
        text,
        count=1,
    )
    text2, n2 = re.subn(
        r"\| 실제 결과/증적 \(P\) \| .* \|",
        f"| 실제 결과/증적 (P) | {evidence} |",
        text2,
        count=1,
    )
    text2, n3 = re.subn(
        r"\| 결함 ID \(Q\) \| .* \|",
        f"| 결함 ID (Q) | {defect} |",
        text2,
        count=1,
    )
    if n != 1 or n2 != 1 or n3 != 1:
        raise SystemExit(f"patch failed {path}")
    path.write_text(text2, encoding="utf-8")


def patch_readme(section: str, rows: list[dict]) -> None:
    path = QA / section / "README.md"
    text = path.read_text(encoding="utf-8")
    by_id = {r["id"]: r for r in rows}
    lines = []
    for line in text.splitlines():
        match = re.search(r"\[([A-Z0-9]+-\d+)\]", line)
        if match and match.group(1) in by_id:
            row = by_id[match.group(1)]
            # rebuild the status columns at the end: | status | defect |
            parts = line.split("|")
            # leading empty, then cells, trailing empty
            if len(parts) >= 7:
                parts[-3] = f" {row['status']} "
                parts[-2] = f" {row['defect_id'] or '—'} "
                line = "|".join(parts)
        lines.append(line)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    import sys

    paths = [Path(p) for p in sys.argv[1:]]
    for path in paths:
        data_cases = load_cases(path)
        sections: dict[str, list[dict]] = {}
        for row in data_cases:
            section = row.get("section")
            if not section:
                raise SystemExit(f"{row['id']} missing section")
            sections.setdefault(section, []).append(row)
        for section, rows in sections.items():
            for row in rows:
                patch_case(section, row)
            patch_readme(section, rows)
            print(section, len(rows))


if __name__ == "__main__":
    main()
