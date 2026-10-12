-- AI adapter scaffold (MVP: no LLM/RAG/Agent). Proposals only; never auto-approve/reject.

CREATE TABLE ai_feature_flags (
    feature_key         VARCHAR(100) PRIMARY KEY,
    enabled             BOOLEAN NOT NULL DEFAULT FALSE,
    description         TEXT NOT NULL,
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE ai_proposal_logs (
    id                  VARCHAR(36) PRIMARY KEY,
    feature_key         VARCHAR(100) NOT NULL,
    story_id            VARCHAR(36),
    proposal_kind       VARCHAR(50) NOT NULL, -- tag_suggest | summary | similar | safety_filter
    input_hash          VARCHAR(64),
    output_json         TEXT,
    used_fallback       BOOLEAN NOT NULL DEFAULT TRUE,
    model_version       VARCHAR(100),
    prompt_version      VARCHAR(100),
    confidence          DOUBLE PRECISION,
    status              VARCHAR(30) NOT NULL DEFAULT 'PROPOSAL_ONLY',
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ai_proposal_logs_feature ON ai_proposal_logs (feature_key, created_at DESC);
CREATE INDEX idx_ai_proposal_logs_story ON ai_proposal_logs (story_id);

INSERT INTO ai_feature_flags (feature_key, enabled, description) VALUES
('tag_suggest', FALSE, '스토리 태그 자동 제안 (v1.1+). MVP OFF — 규칙 fallback만.'),
('similar_place', FALSE, '유사 장소/시대 추천 (embedding). MVP OFF.'),
('summary_card', FALSE, '짧은 요약 카드 (LLM). MVP OFF. explanation-only.'),
('safety_prefilter', FALSE, '부적절 콘텐츠 사전 필터. 최종 결정은 관리자. MVP OFF.');
