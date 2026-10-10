"""dasiGolmok AI 서버 (FastAPI). Spring 백엔드가 내부에서 호출한다.

GET  /api/v1/options    자치구·행정동·업종 목록
POST /api/v1/diagnose   골목 상권 진단
POST /api/v1/recommend  같은 동의 업종 추천
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.service import diagnose, options, recommend

app = FastAPI(title="dasiGolmok AI", version="2.0.0")


class DiagnoseRequest(BaseModel):
    district: str = Field(examples=["마포구"])
    dong: str = Field(examples=["연남동"])
    industry: str = Field(examples=["한식음식점"])


class RecommendRequest(BaseModel):
    district: str = Field(examples=["마포구"])
    dong: str = Field(examples=["연남동"])


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/options")
def options_api():
    return options()


@app.post("/api/v1/diagnose")
def diagnose_api(request: DiagnoseRequest):
    result = diagnose(request.model_dump())
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.post("/api/v1/recommend")
def recommend_api(request: RecommendRequest):
    result = recommend(request.model_dump())
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result
