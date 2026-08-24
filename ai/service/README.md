# FastAPI AI Assist (`ai/service`)

다시, 골목의 **보조** AI 서비스입니다. Spring Backend가 HTTP로 호출하며, Story/Review 상태를 직접 변경하지 않습니다.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Liveness |
| POST | `/v1/analyze/tags` | 태그 후보 |
| POST | `/v1/analyze/summary` | 요약 후보 |
| POST | `/v1/analyze/classify` | 분류 후보 |
| POST | `/v1/curation/candidates` | 큐레이션 순위 후보 |

## Run locally

```bash
npm run ai:dev
# or: bash ai/scripts/run_ai.sh
```

Default port: `8000`.

## Spring wiring

```bash
AI_ENABLED=true
AI_ADAPTER=fastapi
AI_BASE_URL=http://localhost:8000
AI_TAG_SUGGEST_ENABLED=true
AI_SUMMARY_ENABLED=true
AI_CLASSIFY_ENABLED=true
AI_CURATION_ASSIST_ENABLED=true
```

FastAPI 장애 시 Backend는 규칙 fallback으로 응답하며, 스토리 등록·지도·관리자 검수는 계속 동작합니다.
