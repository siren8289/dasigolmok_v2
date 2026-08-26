-- Optimistic locking for concurrent admin review (GM-TC-007)
ALTER TABLE stories ADD COLUMN IF NOT EXISTS version BIGINT NOT NULL DEFAULT 0;
