-- V9: RAG 기반 상권 분석 근거 및 창업 지원 정책 안내 (pgvector 스키마)
-- 확정된 미래 결과 단정 금지 및 마감 지원사업 필터링 지원

CREATE EXTENSION IF NOT EXISTS vector;

-- 상권 지식 베이스 청크 테이블 (보고서 및 공고 벡터 저장)
CREATE TABLE IF NOT EXISTS market_knowledge_chunks (
    id              VARCHAR(100) PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    content         TEXT NOT NULL,
    doc_type        VARCHAR(50) NOT NULL, -- market_report | support_policy
    district        VARCHAR(50),
    dong            VARCHAR(50),
    industry        VARCHAR(50),
    quarter         VARCHAR(20),
    source          VARCHAR(100),
    source_url      TEXT,
    published_at    VARCHAR(20),
    start_date      VARCHAR(20),
    end_date        VARCHAR(20),
    metadata        JSONB,
    embedding       vector(64),
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_market_knowledge_district ON market_knowledge_chunks (district);
CREATE INDEX IF NOT EXISTS idx_market_knowledge_dong ON market_knowledge_chunks (dong);
CREATE INDEX IF NOT EXISTS idx_market_knowledge_industry ON market_knowledge_chunks (industry);
CREATE INDEX IF NOT EXISTS idx_market_knowledge_embedding ON market_knowledge_chunks USING hnsw (embedding vector_cosine_ops);

-- 창업 지원 정책 정보 테이블
CREATE TABLE IF NOT EXISTS support_policies (
    id                  VARCHAR(100) PRIMARY KEY,
    title               VARCHAR(255) NOT NULL,
    organization        VARCHAR(100) NOT NULL,
    target_district     VARCHAR(50),
    target_industry     VARCHAR(100),
    start_date          VARCHAR(20) NOT NULL,
    end_date            VARCHAR(20) NOT NULL,
    support_amount      TEXT,
    description         TEXT NOT NULL,
    eligibility         TEXT,
    source_url          TEXT,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- AI Feature Flags 에 commercial_rag 기능 활성화 등록
INSERT INTO ai_feature_flags (feature_key, enabled, description) VALUES
('commercial_rag', TRUE, 'RAG 기반 상권 분석 근거 및 창업 지원 정책 안내 (v2.1).')
ON CONFLICT (feature_key) DO UPDATE SET enabled = TRUE, description = EXCLUDED.description;
