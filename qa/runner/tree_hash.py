"""워킹 트리에서 QA 게이트가 다시 돌아야 하는 변경만 해시한다."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

WATCH_PREFIXES = (
    "front/src/",
    "front/nginx.conf",
    "front/vite.config.ts",
    "front/package.json",
    "front/package-lock.json",
    "front/tsconfig.json",
    "back/src/",
    "back/build.gradle",
    "ai/src/",
    "ai/tests/",
    "ai/requirements.txt",
    "data/etl/",
    "data/tests/",
    "data/requirements.txt",
    "db/",
    "scripts/",
    ".github/workflows/",
    "qa/runner/",
    "qa/config/",
    "compose.yaml",
    "AGENTS.md",
    "qa-policy.md",
)
SKIP_PARTS = {"__pycache__", "node_modules", "build", "dist", ".gradle"}


def _watched(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if any(part in SKIP_PARTS for part in Path(normalized).parts):
        return False
    return any(
        normalized == prefix or normalized.startswith(prefix)
        for prefix in WATCH_PREFIXES
    )


def changed_paths(root: Path) -> list[str]:
    """HEAD 대비 수정·추가된 감시 경로. 커밋된 트리만이면 빈 목록."""
    output = subprocess.check_output(
        ["git", "status", "--porcelain", "-z"],
        cwd=root,
        text=True,
    )
    found: list[str] = []
    entries = output.split("\0")
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if len(entry) < 4:
            continue
        status = entry[:2]
        path = entry[3:]
        if "R" in status or "C" in status:
            if index < len(entries) and entries[index]:
                path = entries[index]
                index += 1
        if _watched(path):
            found.append(path)
    return sorted(set(found))


def working_tree_token(root: Path) -> str | None:
    """감시 중인 미커밋 변경이 없으면 None."""
    paths = changed_paths(root)
    if not paths:
        return None
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.encode())
        file_path = root / path
        if file_path.is_file():
            digest.update(file_path.read_bytes())
        else:
            digest.update(b"<missing>")
    return digest.hexdigest()
