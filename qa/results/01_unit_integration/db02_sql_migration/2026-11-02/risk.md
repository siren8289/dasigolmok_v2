# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DB02-001 | SQL 스키마 버전·무결성 | V1 사용자 테이블 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-002 | SQL 스키마 버전·무결성 | V1 장소 테이블 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-003 | SQL 스키마 버전·무결성 | V1 지역 테이블 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-004 | SQL 스키마 버전·무결성 | V1 스토리 테이블 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-005 | SQL 스키마 버전·무결성 | V1 외래키 관계 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-006 | SQL 스키마 버전·무결성 | V1 유니크 이메일 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-008 | SQL 스키마 버전·무결성 | V6 이벤트 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-009 | SQL 스키마 버전·무결성 | V6 팩트 테이블 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-010 | SQL 스키마 버전·무결성 | V6 KPI 스냅샷 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-011 | SQL 스키마 버전·무결성 | V8 낙관잠금 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-012 | SQL 스키마 버전·무결성 | V1~V9 순서 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-013 | SQL 스키마 버전·무결성 | 기존 DB 재실행 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-018 | SQL 스키마 버전·무결성 | V9 extension | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-019 | SQL 스키마 버전·무결성 | V9 인덱스 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-020 | SQL 스키마 버전·무결성 | V9 정책 테이블 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-021 | SQL 스키마 버전·무결성 | V9 의존 플래그 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB02-023 | SQL 스키마 버전·무결성 | 정적 SQL 실패 리포트 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |

## DB02-001 V1 사용자 테이블
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: V1 적용 후 public.users 테이블이 있다.

## DB02-002 V1 장소 테이블
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: V1 적용 후 public.places 테이블이 있다.

## DB02-003 V1 지역 테이블
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: V1 적용 후 public.regions 테이블이 있다.

## DB02-004 V1 스토리 테이블
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: V1 적용 후 public.stories 테이블이 있다.

## DB02-005 V1 외래키 관계
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: places FK는 FOREIGN KEY (region_id) REFERENCES regions(id). 없는 region_id INSERT는 23503 insert or update on table "places" violates foreign key constraint "places_region_id_fkey".

## DB02-006 V1 유니크 이메일
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: users.email UNIQUE. 기존 이메일 admin@dasi-golmok.kr 재삽입이 23505 duplicate key value violates unique constraint "users_email_key"로 차단됐다.

## DB02-008 V6 이벤트
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: raw_events 테이블과 PK event_id, 인덱스 ['idx_raw_events_name_time', 'idx_raw_events_region', 'idx_raw_events_story']가 있다.

## DB02-009 V6 팩트 테이블
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: fact_story_lifecycle 생성됨. 컬럼 15개, PK 성격의 story_id 포함.

## DB02-010 V6 KPI 스냅샷
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: V6 적용 후 da_kpi_snapshot 테이블이 있다.

## DB02-011 V8 낙관잠금
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: V8이 stories.version을 추가했다. type=bigint nullable=NO default=0.

## DB02-012 V1~V9 순서
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 빈 DB에 V1부터 V9까지 psql ON_ERROR_STOP으로 순서대로 적용했고 모두 exit 0. server_version=16.15 (Debian 16.15-1.pgdg12+2).

## DB02-013 기존 DB 재실행
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 기존 데이터 디렉터리에서 docker restart. users 4건 유지, qa_reapply_probe 유지. Skipping initialization 로그=있음. entrypoint는 PG_VERSION이 있는 디렉터리에 초기화 SQL을 다시 적용하지 않는다.

## DB02-018 V9 extension
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: CREATE EXTENSION vector 성공. pgvector 0.8.7, PostgreSQL 16.15 (Debian 16.15-1.pgdg12+2).

## DB02-019 V9 인덱스
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: embedding vector(64) HNSW 코사인 색인이 있다. CREATE INDEX idx_market_knowledge_embedding ON public.market_knowledge_chunks USING hnsw (embedding vector_cosine_ops)

## DB02-020 V9 정책 테이블
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: V9가 support_policies 정책 보관 테이블을 만들었다.

## DB02-021 V9 의존 플래그
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: V7 ai_feature_flags가 먼저 있어 V9 INSERT가 성공했다. enabled=True description=RAG 기반 상권 분석 근거 및 창업 지원 정책 안내 (v2.1).

## DB02-023 정적 SQL 실패 리포트
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: psql -f 실패 로그가 파일 3행과 서버 오류를 가리킨다. exit=3. psql:/tmp/qa-db02-023.sql:3: ERROR:  relation "qa_missing_relation_db02_023" does not exist
