"""저장소 소스에서 하드코딩된 비밀과 위험한 렌더링을 찾는다.

테스트 픽스처와 qa 기록은 보지 않는다. 위치는 파일을 읽어 확인한 줄만 적는다.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOTS = (
    "front/src",
    "back/src/main",
    "ai/src",
    "data/etl",
    "scripts",
    ".github/workflows",
)
FILES = ("compose.yaml",)
EXTENSIONS = {".py", ".java", ".ts", ".tsx", ".js", ".yml", ".yaml", ".sh", ".conf"}
SKIP_PARTS = {"node_modules", "build", "dist", "__pycache__", "test", "tests"}

PATTERNS = (
    ("CRITICAL", "개인키", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("CRITICAL", "클라우드 액세스 키", re.compile(r"AKIA[0-9A-Z]{16}")),
    (
        "HIGH",
        "소스에 고정된 자격 증명",
        re.compile(
            r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"
        ),
    ),
    ("HIGH", "HTML 비이스케이프 삽입", re.compile(r"dangerouslySetInnerHTML")),
    ("MEDIUM", "동적 코드 실행", re.compile(r"(?<![\w.])eval\(")),
)


def _iter_files(root: Path):
    for relative in ROOTS:
        base = root / relative
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in EXTENSIONS:
                continue
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            if path.stat().st_size > 1_000_000:
                continue
            yield path
    for name in FILES:
        path = root / name
        if path.is_file():
            yield path


def _ignored_line(line: str) -> bool:
    markers = ("os.getenv", "os.environ", "process.env", "${", "getenv(")
    return any(marker in line for marker in markers)


def scan(root: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path in _iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            if _ignored_line(line):
                continue
            for severity, label, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append(
                        {
                            "severity": severity,
                            "label": label,
                            "file": str(path.relative_to(root)),
                            "line": str(number),
                            "function": "UNKNOWN",
                            "excerpt": line.strip()[:180],
                        }
                    )
    return findings


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    findings = scan(root)
    json.dump(findings, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    blocking = [item for item in findings if item["severity"] in {"HIGH", "CRITICAL"}]
    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
