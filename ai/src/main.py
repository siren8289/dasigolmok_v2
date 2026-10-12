"""dasiGolmok AI 서버 (FastAPI). Spring 백엔드가 내부에서 호출한다.

GET  /api/v1/options                         자치구·행정동·업종 목록
POST /api/v1/diagnose                        골목 상권 진단
POST /api/v1/recommend                       같은 동의 업종 추천
POST /api/v1/commercial-rag/ask              상권 분석 근거 및 지원 정책 RAG 종합 안내 (v2.1 신규)
POST /api/v1/commercial-rag/market-search    상권 근거 보고서 검색 및 Reranking (v2.1 신규)
POST /api/v1/commercial-rag/support-policies 창업 지원 정책 검색 및 마감 판정 (v2.1 신규)
POST /api/v1/commercial-rag/evaluate         RAG 성능 및 안전성 지표 평가 (v2.1 신규)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.service import diagnose, options, recommend
from src.features.commercial_rag_001.router import router as commercial_rag_router

app = FastAPI(title="dasiGolmok AI", version="2.1.0")

# 신규 상권 RAG 및 정책 안내 라우터 등록
app.include_router(commercial_rag_router)


class DiagnoseRequest(BaseModel):
    district: str = Field(examples=["마포구"])
    dong: str = Field(examples=["연남동"])
    industry: str = Field(examples=["한식음식점"])


class RecommendRequest(BaseModel):
    district: str = Field(examples=["마포구"])
    dong: str = Field(examples=["연남동"])


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.1.0"}


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
