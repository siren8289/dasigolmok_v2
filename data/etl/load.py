"""3단계: 결과를 CSV/JSON 파일로 저장한다."""
import json

import pandas as pd

from data.etl.config import PROCESSED_DIR, RAW_DIR


def save_raw_table(df, name):
    """원본 표를 그대로 저장한다. (문제가 생기면 원본부터 다시 확인할 수 있게)"""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"{name}.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def save_raw_json(rows, name):
    """API 원본(리스트)을 JSON으로 저장한다."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"{name}.json"
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def save_processed(df, name):
    """전처리된 표를 저장한다. AI 학습은 이 파일을 읽는다."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / f"{name}.csv"
    df.to_csv(path, index=False, encoding="utf-8-sig")
    return path


def save_json(data, name):
    """선택 목록 같은 작은 JSON을 processed/ 에 저장한다."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / f"{name}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_raw_table(name):
    """이미 받아 둔 원본 CSV가 있으면 읽는다. 없으면 None."""
    path = RAW_DIR / f"{name}.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)
