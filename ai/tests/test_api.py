"""AI 서버 테스트. 실행: cd ai && python -m pytest

GEMINI_API_KEY 를 비워서 LLM 대신 기본 설명이 나오는지 확인한다.
학습된 모델 파일이 있어야 한다. (python -m ai.train.train_ml / train_dl)
"""
from fastapi.testclient import TestClient

from src.main import app
from src.risk import classify

client = TestClient(app)


def test_risk_rules():
    assert classify(2, "LH") == ("stable", False)
    assert classify(5, "HH") == ("warning", False)
    assert classify(9, "HH") == ("danger", True)
    assert classify(1, "HL") == ("danger", True)


def test_options():
    response = client.get("/api/v1/options")
    assert response.status_code == 200
    body = response.json()
    assert "마포구" in body["districts"]
    assert len(body["dongs"]) > 10
    assert len(body["industries"]) > 5


def test_diagnose(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    response = client.post("/api/v1/diagnose", json={
        "district": "강남구", "dong": "역삼1동", "industry": "한식음식점",
    })
    assert response.status_code == 200
    body = response.json()
    assert body["dong"] == "역삼1동"
    assert body["ml_close_rate"] >= 0
    assert body["dl_sales_per_store"] > 0
    assert body["explanation_source"] == "basic"
    assert body["status"] in ("stable", "warning", "danger")


def test_recommend():
    response = client.post("/api/v1/recommend", json={"district": "마포구", "dong": "연남동"})
    assert response.status_code == 200
    body = response.json()
    assert body["dong"] == "연남동"
    assert len(body["all_industries"]) >= 3
    scores = [item["score"] for item in body["all_industries"]]
    assert scores == sorted(scores, reverse=True)


def test_unknown_dong():
    response = client.post("/api/v1/diagnose", json={
        "district": "마포구", "dong": "없는동", "industry": "한식음식점",
    })
    assert response.status_code == 404
