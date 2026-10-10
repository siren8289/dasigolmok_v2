"""학습 스크립트가 같이 쓰는 함수."""
import json
from pathlib import Path

import pandas as pd

from ai.src.features import DL_TARGET, FEATURE_COLUMNS, ML_TARGET

ROOT_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
MODELS_DIR = ROOT_DIR / "ai" / "models"


def load_train_data():
    """data 파이프라인이 만든 전처리 결과를 읽는다."""
    path = PROCESSED_DIR / "train.csv"
    if not path.exists():
        raise FileNotFoundError(f"{path} 가 없습니다. 먼저 `python -m data.etl.run` 을 실행하세요.")
    df = pd.read_csv(path)
    needed = FEATURE_COLUMNS + [ML_TARGET, DL_TARGET]
    df = df.dropna(subset=needed)
    # 전체(30만 행)로 학습하면 시간이 오래 걸려, 8만 건만 무작위로 쓴다.
    if len(df) > 80000:
        df = df.sample(80000, random_state=42)
    return df


def copy_serving_files():
    """Docker 이미지에는 models/ 만 넣기 때문에, 통계·선택목록을 여기로 복사한다."""
    MODELS_DIR.mkdir(exist_ok=True)
    stats = pd.read_csv(PROCESSED_DIR / "dong_stats.csv")
    stats = stats.astype(object).where(stats.notna(), None)
    (MODELS_DIR / "dong_stats.json").write_text(
        json.dumps(stats.to_dict(orient="records"), ensure_ascii=False),
        encoding="utf-8",
    )
    options = (PROCESSED_DIR / "options.json").read_text(encoding="utf-8")
    (MODELS_DIR / "options.json").write_text(options, encoding="utf-8")
