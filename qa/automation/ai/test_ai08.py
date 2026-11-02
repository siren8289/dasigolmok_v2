"""AI08 PyTorch MLP 매출 예측."""
import time
import tracemalloc

import joblib
import numpy as np
import pytest
import torch

from helpers import note
from src.features import make_input_frame
import src.dl_model as dl


def _one(**overrides):
    return make_input_frame(
        overrides.get("district", "마포구"),
        overrides.get("industry", "한식음식점"),
        overrides.get("change_code", "HH"),
        overrides.get("store_count", 10),
        overrides.get("open_rate", 1.1),
        overrides.get("franchise_ratio", 0.2),
        overrides.get("foot_traffic", 10000),
        overrides.get("operate_months", 24),
    )


def _many(count):
    import pandas as pd

    rows = [
        {
            "district": "마포구",
            "industry": "한식음식점",
            "change_code": "HH",
            "store_count": 10 + index,
            "open_rate": 1.1,
            "franchise_ratio": 0.2,
            "foot_traffic": 10000 + index * 500,
            "operate_months": 24,
        }
        for index in range(count)
    ]
    return pd.DataFrame(rows)


def _install_forward(model, fn):
    original = model.forward
    model.forward = fn
    return original


def test_AI08_001():
    loaded = joblib.load(dl.PREPROCESSOR_PATH)
    _model, preprocessor = dl.load_dl_model()
    evidence = (
        f"전처리기 로드 joblib preprocessor type={type(loaded).__name__} "
        f"cached={type(preprocessor).__name__} transform={hasattr(preprocessor, 'transform')}"
    )
    note("AI08-001", evidence)
    assert hasattr(loaded, "transform") and hasattr(preprocessor, "transform"), evidence


def test_AI08_002(monkeypatch):
    seen = {}
    real = dl.torch.load

    def wrapped(*args, **kwargs):
        seen["kwargs"] = kwargs
        seen["path"] = str(args[0])
        return real(*args, **kwargs)

    saved = (dl._model, dl._preprocessor)
    dl._model = None
    dl._preprocessor = None
    monkeypatch.setattr(dl.torch, "load", wrapped)
    try:
        model, _preprocessor = dl.load_dl_model()
        evidence = (
            f"가중치 로드 torch.load kwargs={seen.get('kwargs')} path={seen.get('path')} "
            f"training={model.training}"
        )
        note("AI08-002", evidence)
        assert seen["kwargs"].get("weights_only") is True, evidence
        assert seen["kwargs"].get("map_location") == "cpu", evidence
        assert "sales_mlp.pt" in seen["path"], evidence
    finally:
        if dl._model is None:
            dl._model, dl._preprocessor = saved


def test_AI08_003():
    model, _preprocessor = dl.load_dl_model()
    dropouts = [module for module in model.modules() if isinstance(module, torch.nn.Dropout)]
    evidence = (
        f"평가 모드 model.training={model.training} dropout_count={len(dropouts)} "
        f"dropout_training={[module.training for module in dropouts]}"
    )
    note("AI08-003", evidence)
    assert model.training is False, evidence
    assert dropouts and all(module.training is False for module in dropouts), evidence


def test_AI08_004(monkeypatch):
    calls = {"torch": 0, "joblib": 0}
    real_torch = dl.torch.load
    real_joblib = dl.joblib.load

    def torch_wrapped(*args, **kwargs):
        calls["torch"] += 1
        return real_torch(*args, **kwargs)

    def joblib_wrapped(path):
        calls["joblib"] += 1
        return real_joblib(path)

    saved = (dl._model, dl._preprocessor)
    dl._model = None
    dl._preprocessor = None
    monkeypatch.setattr(dl.torch, "load", torch_wrapped)
    monkeypatch.setattr(dl.joblib, "load", joblib_wrapped)
    try:
        dl.predict_dl(_one())
        dl.predict_dl(_one())
        evidence = f"두 번 추론 torch.load={calls['torch']} joblib.load={calls['joblib']}"
        note("AI08-004", evidence)
        assert calls["torch"] == 1 and calls["joblib"] == 1, evidence
    finally:
        if dl._model is None:
            dl._model, dl._preprocessor = saved


def test_AI08_005():
    predicted = dl.predict_dl(_one())
    evidence = f"1행 매출={predicted}"
    note("AI08-005", evidence)
    assert len(predicted) == 1 and predicted[0] > 0, evidence


def test_AI08_006():
    batch = dl.predict_dl(_many(5))
    singles = [
        dl.predict_dl(_one(store_count=10 + index, foot_traffic=10000 + index * 500))[0]
        for index in range(5)
    ]
    nearest = [
        min(range(len(singles)), key=lambda index: abs(batch[position] - singles[index]))
        for position in range(len(batch))
    ]
    evidence = f"5행 batch={batch} singles={singles} 최근접위치={nearest}"
    note("AI08-006", evidence)
    assert len(batch) == 5 and nearest == [0, 1, 2, 3, 4], evidence


def test_AI08_007():
    model, _preprocessor = dl.load_dl_model()
    target = float(np.log1p(100.0))

    def fake(x):
        return torch.full((x.shape[0], 1), target)

    original = _install_forward(model, fake)
    try:
        predicted = dl.predict_dl(_one())
        evidence = f"log1p(100)={target:.6f} expm1 후 예측={predicted}"
        note("AI08-007", evidence)
        assert predicted == [100.0], evidence
    finally:
        model.forward = original


def test_AI08_008(monkeypatch):
    monkeypatch.setattr(dl.np, "expm1", lambda _output: np.array([-10.0]))
    predicted = dl.predict_dl(_one())
    evidence = f"음수 복원 inverse=-10 → {predicted}"
    note("AI08-008", evidence)
    assert predicted == [0.0], evidence


def test_AI08_009():
    model, _preprocessor = dl.load_dl_model()

    def fake(x):
        return torch.zeros((x.shape[0], 1))

    original = _install_forward(model, fake)
    try:
        predicted = dl.predict_dl(_one())
        evidence = f"영 로그 복원 output log=0 → {predicted}"
        note("AI08-009", evidence)
        assert predicted == [0.0], evidence
    finally:
        model.forward = original


def test_AI08_010(monkeypatch):
    monkeypatch.setattr(dl.np, "expm1", lambda _output: np.array([333.33]))
    predicted = dl.predict_dl(_one())
    evidence = f"예측 333.33 → {predicted}"
    note("AI08-010", evidence)
    assert predicted == [333.3], evidence


def test_AI08_011():
    model, _preprocessor = dl.load_dl_model()
    seen = {}

    def fake(x):
        seen["dtype"] = str(x.dtype)
        seen["shape"] = tuple(x.shape)
        return torch.zeros((x.shape[0], 1))

    original = _install_forward(model, fake)
    try:
        dl.predict_dl(_one())
        evidence = f"모델 입력 dtype={seen.get('dtype')} shape={seen.get('shape')}"
        note("AI08-011", evidence)
        assert seen.get("dtype") == "torch.float32", evidence
    finally:
        model.forward = original


def test_AI08_012():
    tracemalloc.start()
    started = time.perf_counter()
    predicted = dl.predict_dl(_many(100))
    elapsed = time.perf_counter() - started
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    evidence = (
        f"100행 결과={len(predicted)} min={min(predicted)} max={max(predicted)} "
        f"latency={elapsed:.3f}s peak={peak / 1024 / 1024:.1f}MB"
    )
    note("AI08-012", evidence)
    assert len(predicted) == 100, evidence
    assert all(math_ok(value) and value >= 0 for value in predicted), evidence
    assert elapsed < 30, evidence


def math_ok(value):
    return value == value and value not in (float("inf"), float("-inf"))


def test_AI08_013(tmp_path):
    saved = (dl._model, dl._preprocessor, dl.MODEL_PATH)
    missing = tmp_path / "sales_mlp.pt"
    dl._model = None
    dl._preprocessor = None
    dl.MODEL_PATH = missing
    try:
        with pytest.raises(FileNotFoundError) as caught:
            dl.load_dl_model()
        evidence = f"sales_mlp.pt 없음 → {type(caught.value).__name__}: {caught.value}"
        note("AI08-013", evidence)
        assert "sales_mlp.pt" in str(caught.value) or str(missing) in str(caught.value), evidence
    finally:
        dl._model, dl._preprocessor, dl.MODEL_PATH = saved


def test_AI08_014(tmp_path):
    saved = (dl._model, dl._preprocessor, dl.PREPROCESSOR_PATH)
    missing = tmp_path / "sales_mlp_preprocessor.joblib"
    dl._model = None
    dl._preprocessor = None
    dl.PREPROCESSOR_PATH = missing
    try:
        with pytest.raises(FileNotFoundError) as caught:
            dl.load_dl_model()
        evidence = f"preprocessor 없음 → {type(caught.value).__name__}: {caught.value}"
        note("AI08-014", evidence)
        assert missing.name in str(caught.value), evidence
    finally:
        dl._model, dl._preprocessor, dl.PREPROCESSOR_PATH = saved


def test_AI08_015(tmp_path):
    bad_model = dl.SalesMLP(64)
    path = tmp_path / "mismatch.pt"
    torch.save({"input_size": 8, "model_state_dict": bad_model.state_dict()}, path)
    saved = (dl._model, dl._preprocessor, dl.MODEL_PATH)
    dl._model = None
    dl._preprocessor = None
    dl.MODEL_PATH = path
    try:
        with pytest.raises(RuntimeError) as caught:
            dl.load_dl_model()
        evidence = f"input_size 불일치 → {type(caught.value).__name__}: {str(caught.value)[:180]}"
        note("AI08-015", evidence)
        assert "size mismatch" in str(caught.value) or "Error" in type(caught.value).__name__, evidence
    finally:
        dl._model, dl._preprocessor, dl.MODEL_PATH = saved


def test_AI08_016():
    model, _preprocessor = dl.load_dl_model()

    def fake(x):
        return torch.full((x.shape[0], 1), float("nan"))

    original = _install_forward(model, fake)
    try:
        predicted = dl.predict_dl(_one())
        evidence = f"결측 복원 output=NaN → {predicted}"
        note("AI08-016", evidence)
        assert math_ok(predicted[0]), evidence
    finally:
        model.forward = original


def test_AI08_017():
    model, _preprocessor = dl.load_dl_model()

    def fake(x):
        return torch.full((x.shape[0], 1), float("inf"))

    original = _install_forward(model, fake)
    try:
        predicted = dl.predict_dl(_one())
        evidence = f"무한값 복원 output=+inf → {predicted}"
        note("AI08-017", evidence)
        assert math_ok(predicted[0]) and predicted[0] < 1_000_000_000, evidence
    finally:
        model.forward = original


def test_AI08_018():
    frame = _one(store_count=21, foot_traffic=33333)
    first = dl.predict_dl(frame)
    second = dl.predict_dl(frame.copy())
    model, _preprocessor = dl.load_dl_model()
    evidence = f"1회={first} 2회={second} eval={not model.training}"
    note("AI08-018", evidence)
    assert first == second and model.training is False, evidence


def test_AI08_019():
    model, _preprocessor = dl.load_dl_model()
    seen = {}
    original = model.forward

    def wrapped(x):
        seen["grad_enabled"] = torch.is_grad_enabled()
        output = original(x)
        seen["requires_grad"] = bool(output.requires_grad)
        return output

    model.forward = wrapped
    tracemalloc.start()
    try:
        for _ in range(1000):
            dl.predict_dl(_one())
        _current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
        model.forward = original
    grads = [parameter.grad is not None for parameter in model.parameters()]
    evidence = (
        f"1000회 grad_enabled={seen.get('grad_enabled')} requires_grad={seen.get('requires_grad')} "
        f"param_grad_any={any(grads)} peak={peak / 1024 / 1024:.1f}MB"
    )
    note("AI08-019", evidence)
    assert seen.get("grad_enabled") is False and seen.get("requires_grad") is False, evidence
    assert not any(grads), evidence


def test_AI08_020():
    model, _preprocessor = dl.load_dl_model()
    device = next(model.parameters()).device
    evidence = (
        f"parameter.device={device} cuda_available={torch.cuda.is_available()} "
        f"map_location 코드경로=cpu"
    )
    note("AI08-020", evidence)
    assert device.type == "cpu", evidence
