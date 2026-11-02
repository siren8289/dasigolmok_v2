"""AI01–AI09 공통 픽스처 값과 관찰 기록."""
import json

EVIDENCE = {}


def note(case_id, text):
    EVIDENCE[case_id] = str(text)[:400]


def stat_row(**overrides):
    row = {
        "quarter": 20244,
        "dong_code": 11440710,
        "dong": "연남동",
        "district": "마포구",
        "industry_code": "CS100001",
        "industry": "한식음식점",
        "store_count": 10,
        "open_rate": 1.0,
        "open_count": 1,
        "close_rate": 2.0,
        "close_count": 1,
        "franchise_count": 1,
        "franchise_ratio": 0.1,
        "sales_amount": 1000.0,
        "sales_count": 10.0,
        "foot_traffic": 1000,
        "change_code": "HH",
        "change_name": "정체",
        "operate_months": 12,
        "sales_per_store": 100.0,
    }
    row.update(overrides)
    return row


def request_for(row, **overrides):
    body = {"district": row["district"], "dong": row["dong"], "industry": row["industry"]}
    body.update(overrides)
    return body


def patch_diagnose(monkeypatch, row, ml=None, dl=None, explanation=("text", "basic"), capture=None):
    monkeypatch.setattr("src.service.find_stat", lambda dong, industry: row)

    def predict_ml(frame):
        if capture is not None:
            capture["frame"] = frame.copy()
        return [1.23] if ml is None else list(ml)

    def predict_dl(frame):
        if capture is not None:
            capture["dl_frame"] = frame.copy()
        return [100.0] if dl is None else list(dl)

    monkeypatch.setattr("src.service.predict_ml", predict_ml)
    monkeypatch.setattr("src.service.predict_dl", predict_dl)
    if explanation is not None:
        monkeypatch.setattr("src.service.explain", lambda request, result: explanation)
    return row


def patch_recommend(monkeypatch, rows, ml, dl, capture=None):
    monkeypatch.setattr("src.service.industries_in_dong", lambda dong: rows)

    def predict_ml(frame):
        if capture is not None:
            capture["ml_rows"] = len(frame)
            capture["ml_frame"] = frame.copy()
        return list(ml)

    def predict_dl(frame):
        if capture is not None:
            capture["dl_rows"] = len(frame)
        return list(dl)

    monkeypatch.setattr("src.service.predict_ml", predict_ml)
    monkeypatch.setattr("src.service.predict_dl", predict_dl)


def install_fake_gemini(monkeypatch, text="gemini-ok", exc=None, capture=None):
    import sys
    import types

    class Models:
        def generate_content(self, model, contents):
            if capture is not None:
                capture["model"] = model
                capture["contents"] = contents
            if exc is not None:
                raise exc
            return types.SimpleNamespace(text=text)

    class Client:
        def __init__(self, api_key=None, http_options=None):
            if capture is not None:
                capture["api_key"] = api_key
                capture["constructed"] = True
            self.models = Models()

    google_mod = types.ModuleType("google")
    genai_mod = types.ModuleType("google.genai")
    types_mod = types.ModuleType("google.genai.types")
    genai_mod.Client = Client
    types_mod.HttpOptions = lambda timeout=None: {"timeout": timeout}
    google_mod.genai = genai_mod
    monkeypatch.setitem(sys.modules, "google", google_mod)
    monkeypatch.setitem(sys.modules, "google.genai", genai_mod)
    monkeypatch.setitem(sys.modules, "google.genai.types", types_mod)


def sample_result(**overrides):
    result = {
        "dong": "연남동",
        "industry": "한식음식점",
        "status": "stable",
        "close_rate": 7.3,
        "ml_close_rate": 3.4,
        "dl_sales_per_store": 740,
        "change_code": "HH",
        "store_count": 12,
    }
    result.update(overrides)
    return result


def sample_request(**overrides):
    body = {"dong": "연남동", "district": "마포구", "industry": "한식음식점"}
    body.update(overrides)
    return body


def dumps(payload):
    return json.dumps(payload, ensure_ascii=False, default=str)
