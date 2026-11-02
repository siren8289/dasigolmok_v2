# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DB02-007 | SQL 스키마 버전·무결성 | V1 인덱스 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| DB02-014 | SQL 스키마 버전·무결성 | 마이그레이션 별도 앱 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| DB02-015 | SQL 스키마 버전·무결성 | 레거시 스키마와 현재 JPA | Docker | FAIL | SQL | NOT_RUN | FAIL |
| DB02-016 | SQL 스키마 버전·무결성 | V4 시드 개발 데이터 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| DB02-017 | SQL 스키마 버전·무결성 | V6 MV 존재 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| DB02-022 | SQL 스키마 버전·무결성 | V9 트랜잭션 롤백 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| DB02-024 | SQL 스키마 버전·무결성 | 마이그레이션 히스토리 | Docker | FAIL | SQL | NOT_RUN | FAIL |

## DB02-007 V1 인덱스
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 인덱스 존재
- 실제: V1은 CREATE INDEX idx_stories_status ON stories(status)를 만들지만, V3__efficiency_optimization.sql이 DROP INDEX IF EXISTS idx_stories_status를 실행한 뒤 같은 이름으로 다시 만들지 않는다. 최종 DB pg_indexes에 idx_stories_status가 없다.
- 결함ID: DEF-DB02-007
- 코드: db/migration/V1__init_schema.sql

## DB02-014 마이그레이션 별도 앱
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 실제 실행 경로 검증 필요
- 실제: V1 주석 '-- PostgreSQL 16 + Flyway'와 달리 런타임 의존성에 Flyway가 없다. compose는 ./db/migration을 docker-entrypoint-initdb.d에만 마운트하고, application.yml은 ddl-auto: update 이다. 앱이 마이그레이션을 실행하는 경로가 없다.
- 결함ID: DEF-DB02-014
- 코드: db/migration/V1__init_schema.sql

## DB02-015 레거시 스키마와 현재 JPA
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 서로 다른 기능 구현·테이블 사용처 정리
- 실제: stories는 V1 SQL에만 있고 현재 Spring 엔터티가 없다. diagnosis는 JPA @Table만 있고 V1~V9 CREATE TABLE이 없다. 레거시 스토리 스키마와 진단 엔터티의 테이블 사용처가 정리되어 있지 않다.
- 결함ID: DEF-DB02-015
- 코드: db/migration/V1__init_schema.sql

## DB02-016 V4 시드 개발 데이터
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 운영 DB에 더미 데이터 혼입 방지
- 실제: V4 mock INSERT가 스키마와 같은 initdb.d 경로로 실행돼 archive@example.com, retro@example.com 2건이 들어갔다. 운영/개발 분기나 프로파일이 없어 더미 데이터 혼입을 막지 않는다.
- 결함ID: DEF-DB02-016
- 코드: db/migration/V1__init_schema.sql

## DB02-017 V6 MV 존재
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 현재 스키마/실행 코드 존재 확인
- 실제: 스키마 MV=['mv_region_story_stats', 'mv_story_curation_summary']. back/ai/front/data 실행 코드에서 mv_region_story_stats·mv_story_curation_summary 참조=없음. docs/portfolio-materialized-view.md가 말하는 Refresh 실행 코드는 저장소에 없다.
- 결함ID: DEF-DB02-017
- 코드: db/migration/V1__init_schema.sql

## DB02-022 V9 트랜잭션 롤백
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: DB 일부 상태 방지
- 실제: V9에는 BEGIN/COMMIT이 없다. psql은 문장마다 커밋하므로 HNSW 인덱스 실패(embedding_missing) 뒤에도 market_knowledge_chunks=market_knowledge_chunks가 남고 이후 support_policies=None는 없다. 일부 상태가 방지되지 않는다. ERROR:  column "embedding_missing" does not exist
- 결함ID: DEF-DB02-022
- 코드: db/migration/V1__init_schema.sql

## DB02-024 마이그레이션 히스토리
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 이력/재시도 체계 확립
- 실제: V1~V9 적용 후 flyway_schema_history·schema_migrations 같은 추적 테이블이 없다. 실패한 버전을 기록하거나 그 버전만 재시도하는 체계가 없다.
- 결함ID: DEF-DB02-024
- 코드: db/migration/V1__init_schema.sql
