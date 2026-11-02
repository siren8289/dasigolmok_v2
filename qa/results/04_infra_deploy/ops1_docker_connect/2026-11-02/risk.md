# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| OPS1-001 | Docker Compose 4서비스 | compose config | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-002 | Docker Compose 4서비스 | DB_PASSWORD 미설정 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-003 | Docker Compose 4서비스 | 서비스 4개 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-004 | Docker Compose 4서비스 | Postgres 16 pgvector | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-005 | Docker Compose 4서비스 | DB named volume | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-006 | Docker Compose 4서비스 | DB 자격 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-007 | Docker Compose 4서비스 | DB 헬스 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-008 | Docker Compose 4서비스 | DB 다운 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-009 | Docker Compose 4서비스 | AI 서비스명 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-010 | Docker Compose 4서비스 | DB 서비스명 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-011 | Docker Compose 4서비스 | AI depends_on | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-012 | Docker Compose 4서비스 | Back depends_on | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-014 | Docker Compose 4서비스 | Nginx proxy | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-015 | Docker Compose 4서비스 | Host 80 노출 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-016 | Docker Compose 4서비스 | AI 호스트 비공개 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-017 | Docker Compose 4서비스 | Back 호스트 비공개 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-018 | Docker Compose 4서비스 | DB 호스트 비공개 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-019 | Docker Compose 4서비스 | V1~V9 initdb | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-020 | Docker Compose 4서비스 | 상태 Up 의미 | Docker | RISK | SQL | NOT_RUN | RISK |
| OPS1-021 | Docker Compose 4서비스 | ENV 문자열 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-022 | Docker Compose 4서비스 | 로그 확인 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-023 | Docker Compose 4서비스 | front nginx upstream | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS1-025 | Docker Compose 4서비스 | 리빌드 후 데이터 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |

## OPS1-001 compose config
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: DB_PASSWORD=pass docker compose config 종료코드 0. 서비스 ['ai', 'back', 'db', 'front'] 스키마가 해석됐다.

## OPS1-002 DB_PASSWORD 미설정
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: DB_PASSWORD 미설정 시 docker compose config가 required variable DB_PASSWORD 오류로 종료코드 1이다.

## OPS1-003 서비스 4개
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: docker compose config --services 기준 서비스는 db, ai, back, front 네 개다.

## OPS1-004 Postgres 16 pgvector
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: compose config의 db image는 pgvector/pgvector:pg16이다.

## OPS1-005 DB named volume
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: db-data named volume이 /var/lib/postgresql/data에 마운트되어 컨테이너 재생성과 분리된 영속 볼륨이다.

## OPS1-006 DB 자격
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: compose config에서 POSTGRES_USER=dasi, DB=dasigolmok, 비밀번호가 보간되고 JDBC/AI URL이 db:5432를 가리킨다.

## OPS1-007 DB 헬스
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: db healthcheck는 pg_isready -U dasi -d dasigolmok 이며 interval 5s, retries 20이다.

## OPS1-008 DB 다운
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ai와 back 모두 depends_on.db.condition=service_healthy라 pg_isready 실패 시 기동이 막힌다.

## OPS1-009 AI 서비스명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: back 환경변수 APP_AI_BASE_URL=http://ai:8000이고 compose 서비스 이름이 ai라 내부 DNS 대상이 맞다.

## OPS1-010 DB 서비스명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: SPRING_DATASOURCE_URL=jdbc:postgresql://db:5432/dasigolmok 이고 db 서비스가 같은 네트워크에 있다.

## OPS1-011 AI depends_on
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ai.depends_on.db.condition은 service_healthy라 DB 준비 후에 AI가 생성된다.

## OPS1-012 Back depends_on
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: back은 db service_healthy, ai service_started에 의존한다.

## OPS1-014 Nginx proxy
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: front/nginx.conf location /api/ 가 proxy_pass http://back:8080 으로 연결된다.

## OPS1-015 Host 80 노출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: front ports는 published 80, target 80이라 호스트 80으로 웹에 접근하는 구성이다.

## OPS1-016 AI 호스트 비공개
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: compose config에서 ai.ports가 없어 호스트 8000으로 직접 붙는 매핑이 없다.

## OPS1-017 Back 호스트 비공개
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: compose config에서 back.ports가 없어 호스트 8080 직접 매핑이 없다.

## OPS1-018 DB 호스트 비공개
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: compose config에서 db.ports가 없어 외부 5432 매핑이 없다.

## OPS1-019 V1~V9 initdb
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: db/migration 9개 SQL이 /docker-entrypoint-initdb.d 읽기전용 마운트다: V1__init_schema.sql, V2__seed_data.sql, V3__efficiency_optimization.sql, V4__mock_data_extended.sql, V5__area_context_external.sql, V6__analytics_star_schema.sql, V7__ai_adapter_scaffold.sql, V8__story_optimistic_lock.sql, V9__commercial_rag_pgvector.sql.

## OPS1-020 상태 Up 의미
- 상태: 검증A RISK / 검증B NOT_RUN / 최종 RISK
- 내용: 측정하지 못했거나 잠재 위험으로 남긴 항목이다.
- 실제: RISK: 기동 중인 스택이 없어 docker compose ps Up과 /api/health를 대조하지 못했다. compose up은 범위 밖이다.

## OPS1-021 ENV 문자열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GEMINI_API_KEY 미설정 시 compose 값은 빈 문자열이고 explain()은 basic 문장으로 떨어진다.

## OPS1-022 로그 확인
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: DB_PASSWORD를 넣고 docker compose logs --tail=50 ai back 이 종료코드 0이다. 컨테이너가 없으면 본문은 비어도 서비스 로그 조회는 된다.

## OPS1-023 front nginx upstream
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: nginx.conf upstream이 http://back:8080 이고 compose 서비스 이름 back과 같다.

## OPS1-025 리빌드 후 데이터
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: db-data는 named volume이고 up --build 경로(deploy.sh, CD)에 down -v가 없어 리빌드만으로 볼륨이 지워지지 않는다.
