# dasiGolmok 

## 1. 핵심 한 줄

> **Golmok은 쓰기 API 안에서 무거운 통계 Materialized View 갱신을 바로 실행하던 구조를, 커밋 이후 비동기 작업으로 분리해 관리자 상태변경 API 응답시간을 약 96.2% 개선한 프로젝트입니다.**

---

## 프로젝트 구조

```text
dasigolmog/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── ai/
│   ├── catalog/
│   │   └── policy.yaml
│   ├── scripts/
│   │   └── run_ai.sh
│   └── service/                   # FastAPI AI assist (tags/summary/classify/curation)
│       ├── app/
│       ├── Dockerfile
│       └── requirements.txt
├── back/                          # Spring Boot API
│   ├── db/
│   │   └── README.md
│   ├── gradle/
│   │   └── wrapper/
│   ├── scripts/
│   │   ├── db-up.sh
│   │   └── db-down.sh
│   ├── src/
│   │   └── main/                  # java + resources + migration
│   ├── build.gradle.kts
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── gradlew*
├── da/                            # Data Analytics
│   ├── README.md
│   ├── catalog/
│   │   └── kpi.yaml
│   ├── docs/
│   │   └── analytics-refresh.md
│   ├── pipeline/                  # star build · KPI
│   ├── scripts/
│   │   └── run_analytics.sh
│   ├── sql/
│   │   └── kpi_queries.sql
│   └── reports/
├── de/                            # Data Engineering
│   ├── catalog/
│   │   └── datasets.yaml
│   ├── fixtures/                  # 상권 CSV
│   ├── data/                      # raw · quarantine · staging
│   ├── pipeline/                  # ingest → DQ → mart
│   ├── scripts/
│   │   └── run_pipeline.sh
│   └── reports/
├── front/                         # Next.js
│   ├── src/
│   │   ├── app/                   # page routes (admin/auth/curation/map/stories)
│   │   ├── components/            # Header, StoryCard, StoryMap...
│   │   ├── lib/                   # api-client, auth-context
│   │   └── types/
│   ├── package.json
│   ├── next.config.ts
│   └── Dockerfile
├── qa/
│   ├── catalog/
│   │   └── traceability.yaml
│   ├── evidence/
│   ├── reports/
│   │   └── latest_run.json
│   └── scripts/
│       └── run_gm_tc.{py,sh}
├── scripts/                       # deploy, health-check, rollback
├── docker-compose.yml
├── docker-compose.dev.yml
├── package.json                   # monorepo scripts
├── DEPLOYMENT.md
└── README.md
```

| 경로 | 역할 |
|------|------|
| `back/` | BE API (Auth·Story·Admin·Analytics·AI gateway) |
| `ai/` | FastAPI AI assist + policy catalog (제안만, 검수 대체 없음) |
| `front/` | FE (지도·큐레이션·등록·관리자) |
| `de/` | 상권 공공데이터 파이프라인 |
| `da/` | 이벤트·스타 스키마·KPI |
| `ai/` | AI 정책 카탈로그 (기능은 `back/.../ai`) |
| `qa/` | GM-TC 자동화·증거 팩 |

---

## 2. 역할별 문서 정리

Data Analyst 관련 문서는 루트 README에서 분리해 `da/` 아래로 이동했습니다.

| 문서 | 설명 |
|------|------|
| [`da/README.md`](./da/README.md) | DA 문서 허브, 실행 경로, 주요 파일 안내 |
| [`da/docs/analytics-refresh.md`](./da/docs/analytics-refresh.md) | 통계 갱신 구조, 성능 측정, 운영 포인트 |
| [`da/catalog/kpi.yaml`](./da/catalog/kpi.yaml) | KPI 정의/버전/세그먼트/개인정보 규칙 |
| [`da/sql/kpi_queries.sql`](./da/sql/kpi_queries.sql) | KPI 검증용 참조 SQL |
| [`back/src/main/resources/db/migration/V6__analytics_star_schema.sql`](./back/src/main/resources/db/migration/V6__analytics_star_schema.sql) | DA 스타 스키마 DDL |

---

## 3. 빠른 이동

- FE: `front/`
- BE: `back/`
- DE: `de/`
- DA: `da/`
- QA: `qa/`
- AI: `ai/`
