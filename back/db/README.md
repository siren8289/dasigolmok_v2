# 다시, 골목 — 데이터베이스

## 기술 스택 선정 이유

| 구성 | 선택 | 이유 |
|------|------|------|
| **DBMS** | PostgreSQL 16 | 사용자·스토리·지역·태그·신고·감사로그 등 **관계형 데이터**가 핵심이며, FK·트랜잭션·동시성이 필요함. Spring Data JPA와 운영 환경에서 검증된 조합. |
| **마이그레이션** | Flyway | 스키마를 **버전 관리된 SQL**로 관리해 팀 협업·배포 시 `ddl-auto: update`의 비가역 변경 위험을 제거. |
| **ORM** | Spring Data JPA | 백엔드 레이어드 아키텍처와 맞고, 엔티티 기반 도메인 모델 유지에 적합. |
| **로컬 실행** | Docker Compose | OS에 PostgreSQL을 직접 설치하지 않고 **동일한 DB 버전**으로 개발 가능. |

## 디렉터리 구조

```
back/
├── docker-compose.yml          # 로컬 PostgreSQL
├── db/
│   └── README.md               # 이 문서
├── scripts/
│   ├── db-up.sh                # DB 컨테이너 기동
│   └── db-down.sh              # DB 컨테이너 중지
└── src/main/resources/db/migration/
    ├── V1__init_schema.sql              # 핵심 도메인 스키마
    ├── V2__seed_data.sql                # 기본 시드
    ├── V3__efficiency_optimization.sql  # 제약·인덱스·Materialized View
    ├── V4__mock_data_extended.sql       # 확장 목업 데이터
    ├── V5__area_context_external.sql    # 외부 상권 컨텍스트 적재 스키마
    ├── V6__analytics_star_schema.sql    # DA 스타 스키마/이벤트 mart
    ├── V7__ai_adapter_scaffold.sql      # AI 어댑터용 스키마
    └── V8__story_optimistic_lock.sql    # 스토리 낙관적 락
```

## 빠른 시작

```bash
# 1. DB 컨테이너 실행
cd back
docker compose up -d

# 2. 환경변수 (선택)
cp .env.example .env

# 3. 백엔드 실행 — Flyway가 마이그레이션 자동 적용
./gradlew bootRun
```

루트에서 실행:

```bash
npm run db:up      # back/docker-compose.yml 사용
npm run dev:back   # 마이그레이션 후 API 기동
```

## 연결 정보 (기본값)

| 항목 | 값 |
|------|-----|
| Host | `localhost` |
| Port | `5432` |
| Database | `dasi_golmok` |
| User | `app_user` |
| Password | `app_password` |
| JDBC URL | `jdbc:postgresql://localhost:5432/dasi_golmok` |

## 시드 계정

| 역할 | 이메일 | 비밀번호 |
|------|--------|----------|
| 관리자 | admin@dasi-golmok.kr | admin1234 |
| 사용자 | user@example.com | user1234 |

## 마이그레이션 규칙

- 파일명: `V{버전}__{설명}.sql` (예: `V3__add_story_view_count.sql`)
- 스키마 변경은 **반드시 새 마이그레이션 파일**로 추가
- `ddl-auto`는 `validate` — Hibernate가 Flyway 스키마와 일치하는지 검증만 수행

## 데이터베이스 범위

이 문서는 `back/` 기준의 운영 DB 실행과 Flyway 마이그레이션에 집중합니다.

DA(Data Analyst) 관련 항목은 `da/` 아래로 분리했습니다.

| 항목 | 문서 |
|------|------|
| DA 문서 허브 | [`../../da/README.md`](../../da/README.md) |
| 통계 갱신 구조 | [`../../da/docs/analytics-refresh.md`](../../da/docs/analytics-refresh.md) |
| KPI 정의 | [`../../da/catalog/kpi.yaml`](../../da/catalog/kpi.yaml) |
| 스타 스키마 DDL | [`../src/main/resources/db/migration/V6__analytics_star_schema.sql`](../src/main/resources/db/migration/V6__analytics_star_schema.sql) |

### 확장 목업 (V4)

- 추가 사용자 2명, 승인 스토리 4건
- 검수 대기(PENDING) 3건 — 관리자 페이지 테스트용
- 신고 3건, 좋아요 반응, 숨김 스토리 1건

```bash
npm run db:reset   # 볼륨 삭제 후 재기동 → 전체 Flyway 마이그레이션 재적용
```
