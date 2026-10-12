"""기존 src/features.py 모듈과 신규 src/features 패키지의 공존을 지원합니다.

기존 코드(service.py 등)가 `from src.features import ...` 형태로 가져올 때,
기존 features.py의 함수와 상수를 그대로 제공하여 기존 기능에 영향을 주지 않도록 합니다.
"""
from pathlib import Path
import importlib.util

# 상위 폴더의 기존 features.py 파일 경로를 찾습니다.
_features_file = Path(__file__).resolve().parent.parent / "features.py"

if _features_file.exists():
    _spec = importlib.util.spec_from_file_location("_legacy_features", _features_file)
    _module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_module)
    for _key, _value in _module.__dict__.items():
        if not _key.startswith("__"):
            globals()[_key] = _value
