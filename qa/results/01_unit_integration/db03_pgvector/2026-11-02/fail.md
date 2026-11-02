# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DB03-015 | RAG 데이터베이스 스키마 | DB 정책 실시간 소스 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| DB03-016 | RAG 데이터베이스 스키마 | 정책 날짜 CHECK | Docker | FAIL | SQL | NOT_RUN | FAIL |
| DB03-017 | RAG 데이터베이스 스키마 | 정책 source_url 검증 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| DB03-019 | RAG 데이터베이스 스키마 | 정책 갱신/삭제 | Docker | FAIL | SQL | NOT_RUN | FAIL |

## DB03-015 DB 정책 실시간 소스
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 실제 DB 정책과 연결되어 있는지 검증
- 실제: search_policies/get_all_policy_items는 support_policies가 아니라 service.py의 POLICY_DATABASE 정적 목록을 순회한다. 마이그레이션 직후 support_policies 행 수는 테스트 삽입을 포함해 1건이며 RAG 조회 경로와 연결되어 있지 않다.
- 결함ID: DEF-DB03-015
- 코드: db/migration/V9__commercial_rag_pgvector.sql

## DB03-016 정책 날짜 CHECK
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: DB 검증 제약 필요
- 실제: support_policies에 end_date>=start_date CHECK가 없다. start_date='2026-12-31', end_date='2026-01-01' INSERT가 성공했다. 날짜 검증 제약이 필요하다.
- 결함ID: DEF-DB03-016
- 코드: db/migration/V9__commercial_rag_pgvector.sql

## DB03-017 정책 source_url 검증
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 원본 검증 정책 필요
- 실제: support_policies.source_url에 URI 형식 CHECK가 없다. 'not a uri'가 저장됐다. 원본 URL 검증 정책이 없다.
- 결함ID: DEF-DB03-017
- 코드: db/migration/V9__commercial_rag_pgvector.sql

## DB03-019 정책 갱신/삭제
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 데이터 갱신 전략 명세 필요
- 실제: 만료 정책(2024-01-01~2024-06-30)이 support_policies에 그대로 저장된다. 컬럼은 ['id', 'title', 'organization', 'target_district', 'target_industry', 'start_date', 'end_date', 'support_amount', 'description', 'eligibility', 'source_url', 'created_at']뿐이고 deleted_at/status/updated_at이 없다. support_policy/service.py는 정적 POLICY_DATABASE만 읽고 갱신·삭제 SQL이 없다. 갱신 전략이 명세되어 있지 않다.
- 결함ID: DEF-DB03-019
- 코드: db/migration/V9__commercial_rag_pgvector.sql
