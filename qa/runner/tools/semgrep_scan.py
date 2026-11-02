#!/usr/bin/env python3
"""Semgrep 정적 분석 (security 1차). 미설치면 pip로 설치를 시도한다."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TARGETS = ["ai/src", "data/etl", "back/src", "front/src"]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def semgrep_bin() -> str | None:
    found = shutil.which("semgrep")
    if found:
        return found
    # pip scripts path fallback
    candidate = Path(sys.executable).resolve().parent / "semgrep"
    if candidate.exists():
        return str(candidate)
    return None


def ensure_semgrep() -> tuple[str | None, str]:
    binary = semgrep_bin()
    if binary:
        probe = run([binary, "--version"])
        if probe.returncode == 0:
            return binary, probe.stdout.strip()
    install = run([sys.executable, "-m", "pip", "install", "semgrep"])
    if install.returncode != 0:
        return None, (install.stderr or install.stdout)[-1000:]
    binary = semgrep_bin()
    if not binary:
        return None, "semgrep installed but binary not found on PATH"
    probe = run([binary, "--version"])
    if probe.returncode != 0:
        return None, (probe.stderr or probe.stdout)[-1000:]
    return binary, probe.stdout.strip()


def main() -> int:
    binary, detail = ensure_semgrep()
    if not binary:
        print(json.dumps({"status": "ERROR", "detail": detail}, ensure_ascii=False))
        return 2
    existing = [path for path in TARGETS if (ROOT / path).exists()]
    args = [
        binary,
        "--config",
        "p/owasp-top-ten",
        "--json",
        "--quiet",
        "--error",
        *existing,
    ]
    completed = run(args)
    try:
        payload = json.loads(completed.stdout or "{}")
    except json.JSONDecodeError:
        print(json.dumps({"status": "ERROR", "detail": (completed.stderr or completed.stdout)[-1500:]}, ensure_ascii=False))
        return 2
    results = payload.get("results") or []
    highs = [
        item
        for item in results
        if str(item.get("extra", {}).get("severity", "")).upper() in {"ERROR", "HIGH", "CRITICAL"}
    ]
    if completed.returncode not in {0, 1}:
        status = "ERROR"
    elif highs:
        status = "FAIL"
    else:
        status = "PASS"
    print(
        json.dumps(
            {
                "status": status,
                "findings": len(results),
                "high": len(highs),
                "exit": completed.returncode,
                "version": detail,
            },
            ensure_ascii=False,
        )
    )
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
