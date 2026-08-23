"""Shared psql helpers."""
from __future__ import annotations

import os
import subprocess
from typing import Dict


def psql_env() -> Dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PGHOST", env.get("DB_HOST", "localhost"))
    env.setdefault("PGPORT", env.get("DB_PORT", "5432"))
    env.setdefault("PGUSER", env.get("DB_USERNAME", "app_user"))
    env.setdefault("PGPASSWORD", env.get("DB_PASSWORD", "app_password"))
    env.setdefault("PGDATABASE", env.get("DB_NAME", "dasi_golmok"))
    return env


def run_psql(sql: str, tuples_only: bool = True) -> str:
    args = ["psql", "-v", "ON_ERROR_STOP=1"]
    if tuples_only:
        args.extend(["-At"])
    args.extend(["-c", sql])
    result = subprocess.run(args, env=psql_env(), capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    return result.stdout


def run_psql_file(path: str) -> str:
    result = subprocess.run(
        ["psql", "-v", "ON_ERROR_STOP=1", "-f", path],
        env=psql_env(),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    return result.stdout
