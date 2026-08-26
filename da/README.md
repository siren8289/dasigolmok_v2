# Data Analytics

## 개요

`da/`는 Data Analyst 관점의 산출물을 모아둔 영역입니다. 이벤트 적재, 스타 스키마 구성, KPI 계산, 분석 리포트, 관련 문서를 이 폴더 기준으로 확인할 수 있습니다.

## 디렉터리 구조

```text
da/
├── README.md
├── catalog/
│   └── kpi.yaml                 # KPI 정의·버전·세그먼트·privacy rule
├── docs/
│   └── analytics-refresh.md     # 통계 갱신 구조/성능 개선 문서
├── pipeline/
│   ├── run.py                   # seed → star build → KPI snapshot
│   ├── seed_events.py           # GA4 스타일 이벤트 시드
│   ├── build_star.py            # raw/de mart → dim/fact 적재
│   └── compute_kpi.py           # da_kpi_snapshot + JSON report 생성
├── reports/                     # 실행 결과 리포트
├── scripts/
│   └── run_analytics.sh         # DA 파이프라인 실행 스크립트
└── sql/
    └── kpi_queries.sql          # KPI 기준 SQL 예시
```

## 주요 파일

| 경로 | 설명 |
|------|------|
| `catalog/kpi.yaml` | KPI 키, formula version, 세그먼트, privacy/attribution 규칙 |
| `pipeline/run.py` | 이벤트 시드 → 스타 스키마 적재 → KPI 스냅샷 생성 전체 실행 |
| `pipeline/build_star.py` | `raw_events`, `dim_*`, `fact_*`, `fact_area_context_snapshot` 적재 |
| `pipeline/compute_kpi.py` | `da_kpi_snapshot` 입력과 JSON 리포트 생성 |
| `sql/kpi_queries.sql` | KPI 검증용 참조 SQL |
| `docs/analytics-refresh.md` | DA 관점의 통계 갱신 구조, 측정 결과, 운영 포인트 |
| `../back/src/main/resources/db/migration/V6__analytics_star_schema.sql` | DA 스타 스키마 DDL |

## 실행

```bash
npm run da:analytics
```

실행 흐름:

```text
raw_events seed
→ dim/fact build
→ da_kpi_snapshot 적재
→ da/reports/*.json 생성
```

## 참고 문서

- DA 문서 허브: `./docs/analytics-refresh.md`
- KPI 카탈로그: `./catalog/kpi.yaml`
- KPI 기준 SQL: `./sql/kpi_queries.sql`
- 스타 스키마 DDL: `../back/src/main/resources/db/migration/V6__analytics_star_schema.sql`
