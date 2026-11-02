# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DB03-001 | RAG 데이터베이스 스키마 | vector 확장 존재 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-002 | RAG 데이터베이스 스키마 | 청크 ID 기본키 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-003 | RAG 데이터베이스 스키마 | title NOT NULL | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-004 | RAG 데이터베이스 스키마 | content NOT NULL | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-005 | RAG 데이터베이스 스키마 | doc_type NOT NULL | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-006 | RAG 데이터베이스 스키마 | source optional | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-007 | RAG 데이터베이스 스키마 | region 필터 인덱스 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-008 | RAG 데이터베이스 스키마 | dong 필터 인덱스 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-009 | RAG 데이터베이스 스키마 | industry 필터 인덱스 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-010 | RAG 데이터베이스 스키마 | embedding 64차원 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-011 | RAG 데이터베이스 스키마 | embedding 512차원 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-012 | RAG 데이터베이스 스키마 | HNSW 인덱스 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-013 | RAG 데이터베이스 스키마 | 메타데이터 JSONB | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-014 | RAG 데이터베이스 스키마 | 마감 정책 테이블 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| DB03-018 | RAG 데이터베이스 스키마 | 외부 연결 차단 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |

## DB03-001 vector 확장 존재
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: pg_extension vector 활성. version=0.8.7.

## DB03-002 청크 ID 기본키
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: market_knowledge_chunks.id 중복 INSERT가 실패했다. 23505 duplicate key value violates unique constraint "market_knowledge_chunks_pkey"

## DB03-003 title NOT NULL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: title NULL 저장이 차단됐다. 23502 null value in column "title" of relation "market_knowledge_chunks" violates not-null constraint

## DB03-004 content NOT NULL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: content NULL 저장이 차단됐다. 23502 null value in column "content" of relation "market_knowledge_chunks" violates not-null constraint

## DB03-005 doc_type NOT NULL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: doc_type NULL 저장이 차단됐다. 23502 null value in column "doc_type" of relation "market_knowledge_chunks" violates not-null constraint

## DB03-006 source optional
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: source 컬럼 is_nullable=YES. NULL 저장 후 조회값=None. NULL을 허용한다.

## DB03-007 region 필터 인덱스
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: idx_market_knowledge_district indisvalid=True indisready=True method=btree.

## DB03-008 dong 필터 인덱스
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: idx_market_knowledge_dong indisvalid=True indisready=True method=btree.

## DB03-009 industry 필터 인덱스
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: idx_market_knowledge_industry indisvalid=True indisready=True method=btree.

## DB03-010 embedding 64차원
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: vector(64) 임베딩 저장 성공. vector_dims=64.

## DB03-011 embedding 512차원
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 512차원 벡터는 차원 불일치로 거절됐다. 22000 expected 64 dimensions, not 512

## DB03-012 HNSW 인덱스
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: embedding HNSW vector_cosine_ops 인덱스가 유효하다. CREATE INDEX idx_market_knowledge_embedding ON public.market_knowledge_chunks USING hnsw (embedding vector_cosine_ops)

## DB03-013 메타데이터 JSONB
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: metadata JSONB에 {"구역":"마포구","n":1}을 넣고 키 조회가 마포구, 1로 돌아왔다.

## DB03-014 마감 정책 테이블
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: start_date/end_date가 character varying로 '2026-01-05', '2026-12-31' 그대로 저장됐다.

## DB03-018 외부 연결 차단
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: compose.yaml db 서비스에 ports가 없고 5432:5432 바인딩도 없다. 호스트 공개 포트는 front 80:80뿐이고 DB는 컨테이너 내부 db:5432만 쓴다.
