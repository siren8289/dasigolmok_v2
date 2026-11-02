#!/usr/bin/env python3
"""QA MASTER 원문을 섹션 폴더와 케이스 카드로 펼친다."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROMPT = Path(
    "/Users/jeong-yelim/.grok/sessions/"
    "%2FUsers%2Fjeong-yelim%2Forca%2Fdasigolmok_v2/"
    "01a19bbd-2892-7772-9fa8-9cc49c2a27f5/prompts/prompt_0.txt"
)
QA = ROOT / "qa"
META = QA / "_meta"

COLUMNS = [
    "id",
    "section",
    "feature",
    "item",
    "priority",
    "kind",
    "purpose",
    "precondition",
    "input",
    "steps",
    "expected",
    "criteria",
    "tool",
    "basis",
    "status",
    "evidence",
    "defect_id",
    "code_path",
    "code_url",
    "note",
]

ID_RE = re.compile(r"^[A-Z]{2,4}\d{1,2}-\d{3}$")


def parse_record(raw: str) -> list[str]:
    """4칸 구분. 필드의 첫 글자가 큰따옴표면 인용 필드이고, 내부 "" 는 이스케이프다."""
    fields: list[str] = []
    i = 0
    n = len(raw)
    while i < n:
        if raw.startswith('"', i):
            i += 1
            buf: list[str] = []
            while i < n:
                if raw.startswith('""', i):
                    buf.append('"')
                    i += 2
                elif raw[i] == '"':
                    i += 1
                    break
                else:
                    buf.append(raw[i])
                    i += 1
            fields.append("".join(buf).strip())
        else:
            j = raw.find("    ", i)
            if j == -1:
                fields.append(raw[i:].strip())
                break
            fields.append(raw[i:j].strip())
            i = j
        if i >= n:
            break
        if raw.startswith("    ", i):
            i += 4
        else:
            break
    return fields


def load_records() -> list[dict]:
    text = PROMPT.read_text(encoding="utf-8")
    start = text.find("FE01-001")
    body = text[start:]
    end = body.find("</user_query>")
    if end != -1:
        body = body[:end]
    parts = re.split(r"(?=^[A-Z]{2,4}\d{1,2}-\d{3}    )", body, flags=re.M)
    records = []
    for part in parts:
        part = part.strip("\n")
        if not part.strip():
            continue
        fields = parse_record(part.strip())
        if len(fields) != 20:
            raise SystemExit(f"field count {len(fields)} for {fields[0] if fields else part[:40]!r}")
        row = dict(zip(COLUMNS, fields))
        if not ID_RE.match(row["id"]):
            raise SystemExit(f"bad id {row['id']}")
        if row["id"] == "QA02-018":
            row["note"] = row["note"].replace(
                "섹션마다 커밋 푸쉬 하면서 해 전부 폴더 만들고", ""
            ).strip()
        records.append(row)
    ids = [r["id"] for r in records]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate ids")
    return records


def case_md(row: dict) -> str:
    status = row["status"] or "미실행"
    evidence = row["evidence"]
    defect = row["defect_id"]
    return f"""# {row['id']} {row['item']}

| 항목 | 내용 |
| --- | --- |
| TC ID | {row['id']} |
| 분야 | {row['section']} |
| 세부 기능 | {row['feature']} |
| 원자 검증 항목 | {row['item']} |
| 우선순위 | {row['priority']} |
| 테스트 구분 | {row['kind']} |
| 근거 분류 | {row['basis']} |
| 추천 도구 | {row['tool']} |
| 관련 코드 경로 | `{row['code_path']}` |
| GitHub 코드 URL | {row['code_url']} |

## 검증 목적

{row['purpose']}

## 사전조건

{row['precondition']}

## 테스트 입력값

{row['input']}

## 실행 절차

{row['steps']}

## 기대 결과

{row['expected']}

## 판정 기준

{row['criteria']}

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | {status} |
| 실제 결과/증적 (P) | {evidence or '—'} |
| 결함 ID (Q) | {defect or '—'} |

## 비고/근거

{row['note']}
"""


def main() -> None:
    records = load_records()
    META.mkdir(parents=True, exist_ok=True)
    (META / "cases.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    sections: dict[str, list[dict]] = {}
    for row in records:
        sections.setdefault(row["section"], []).append(row)
    (META / "sections.json").write_text(
        json.dumps(
            [{"section": name, "count": len(rows), "ids": [r["id"] for r in rows]} for name, rows in sections.items()],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    for name, rows in sections.items():
        folder = QA / name
        folder.mkdir(parents=True, exist_ok=True)
        (META / "sections" ).mkdir(parents=True, exist_ok=True)
        (META / "sections" / f"{name}.json").write_text(
            json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        lines = [
            f"# {name}",
            "",
            f"- 세부 기능: {rows[0]['feature']}",
            f"- 케이스: {len(rows)}",
            f"- 코드: `{rows[0]['code_path']}`",
            "",
            "| TC ID | 원자 검증 항목 | 우선순위 | 근거 분류 | 실행 상태 | 결함 ID |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for row in rows:
            case_dir = folder / row["id"]
            case_dir.mkdir(parents=True, exist_ok=True)
            (case_dir / "case.md").write_text(case_md(row), encoding="utf-8")
            lines.append(
                f"| [{row['id']}](./{row['id']}/case.md) | {row['item']} | {row['priority']} | {row['basis']} | {row['status'] or '미실행'} | {row['defect_id'] or '—'} |"
            )
        (folder / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"records={len(records)} sections={len(sections)}")


if __name__ == "__main__":
    main()
