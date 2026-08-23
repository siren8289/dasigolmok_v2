-- DA: event store + star schema (UGC + Area Context analysis mart)
-- Metric formulas versioned in da_metric_versions. Area facts join DE mart (Context only).

CREATE TABLE da_metric_versions (
    metric_key          VARCHAR(100) PRIMARY KEY,
    formula_version     VARCHAR(20) NOT NULL,
    formula_text        TEXT NOT NULL,
    grain               VARCHAR(50) NOT NULL,
    owner_team          VARCHAR(50) NOT NULL,
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE raw_events (
    event_id            VARCHAR(36) PRIMARY KEY,
    event_name          VARCHAR(100) NOT NULL,
    occurred_at         TIMESTAMP NOT NULL,
    user_id_hash        VARCHAR(64),
    session_id          VARCHAR(64),
    story_id            VARCHAR(36),
    region_id           VARCHAR(36),
    area_code           VARCHAR(20),
    source              VARCHAR(50),
    channel             VARCHAR(50),
    sort_type           VARCHAR(50),
    position            INTEGER,
    action              VARCHAR(50),
    has_area_context    BOOLEAN,
    has_image           BOOLEAN,
    category            VARCHAR(100),
    zoom                INTEGER,
    props_json          TEXT,
    ingested_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    pipeline_run_id     VARCHAR(36)
);

CREATE INDEX idx_raw_events_name_time ON raw_events (event_name, occurred_at);
CREATE INDEX idx_raw_events_story ON raw_events (story_id);
CREATE INDEX idx_raw_events_region ON raw_events (region_id);

-- Dimensions
CREATE TABLE dim_date (
    date_key            INTEGER PRIMARY KEY, -- YYYYMMDD
    full_date           DATE NOT NULL UNIQUE,
    year                INTEGER NOT NULL,
    quarter             INTEGER NOT NULL,
    month               INTEGER NOT NULL,
    week_of_year        INTEGER NOT NULL,
    day_of_week         INTEGER NOT NULL
);

CREATE TABLE dim_region (
    region_sk           SERIAL PRIMARY KEY,
    region_id           VARCHAR(36) NOT NULL UNIQUE,
    region_name         VARCHAR(255) NOT NULL,
    region_slug         VARCHAR(255) NOT NULL
);

CREATE TABLE dim_place (
    place_sk            SERIAL PRIMARY KEY,
    place_id            VARCHAR(36) NOT NULL UNIQUE,
    place_name          VARCHAR(255) NOT NULL,
    region_id           VARCHAR(36),
    area_mapping_segment VARCHAR(20) NOT NULL DEFAULT '미매핑'
);

CREATE TABLE dim_user (
    user_sk             SERIAL PRIMARY KEY,
    user_id_hash        VARCHAR(64) NOT NULL UNIQUE,
    role_masked         VARCHAR(20) NOT NULL
);

CREATE TABLE dim_tag (
    tag_sk              SERIAL PRIMARY KEY,
    tag_id              VARCHAR(36) NOT NULL UNIQUE,
    tag_name            VARCHAR(255) NOT NULL,
    tag_type            VARCHAR(50) NOT NULL
);

CREATE TABLE dim_status (
    status_sk           SERIAL PRIMARY KEY,
    status_code         VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE dim_area (
    area_sk             SERIAL PRIMARY KEY,
    area_code           VARCHAR(20) NOT NULL UNIQUE,
    area_name           VARCHAR(255) NOT NULL,
    area_type_name      VARCHAR(100),
    area_mapping_version VARCHAR(50) NOT NULL,
    standard_unit_zone_version VARCHAR(50) NOT NULL DEFAULT '2024',
    source_name         VARCHAR(255),
    source_url          TEXT,
    license_type        VARCHAR(100),
    base_period         VARCHAR(10)
);

-- Facts
CREATE TABLE fact_story_lifecycle (
    story_id            VARCHAR(36) PRIMARY KEY,
    region_sk           INTEGER REFERENCES dim_region(region_sk),
    place_sk            INTEGER REFERENCES dim_place(place_sk),
    user_sk             INTEGER REFERENCES dim_user(user_sk),
    status_sk           INTEGER REFERENCES dim_status(status_sk),
    area_sk             INTEGER REFERENCES dim_area(area_sk),
    register_date_key   INTEGER REFERENCES dim_date(date_key),
    approve_date_key    INTEGER REFERENCES dim_date(date_key),
    has_area_context    BOOLEAN NOT NULL DEFAULT FALSE,
    like_count          INTEGER NOT NULL DEFAULT 0,
    category            VARCHAR(100),
    period_tag          VARCHAR(100),
    created_at          TIMESTAMP NOT NULL,
    approved_at         TIMESTAMP,
    metric_formula_version VARCHAR(20) NOT NULL DEFAULT 'v1'
);

CREATE TABLE fact_user_engagement (
    engagement_id       VARCHAR(36) PRIMARY KEY,
    event_id            VARCHAR(36) NOT NULL UNIQUE REFERENCES raw_events(event_id),
    event_name          VARCHAR(100) NOT NULL,
    date_key            INTEGER REFERENCES dim_date(date_key),
    region_sk           INTEGER REFERENCES dim_region(region_sk),
    story_id            VARCHAR(36),
    user_sk             INTEGER REFERENCES dim_user(user_sk),
    area_sk             INTEGER REFERENCES dim_area(area_sk),
    has_area_context    BOOLEAN,
    source              VARCHAR(50),
    channel             VARCHAR(50),
    sort_type           VARCHAR(50),
    occurred_at         TIMESTAMP NOT NULL,
    metric_formula_version VARCHAR(20) NOT NULL DEFAULT 'v1'
);

CREATE TABLE fact_admin_review (
    review_id           VARCHAR(36) PRIMARY KEY,
    story_id            VARCHAR(36) NOT NULL,
    date_key            INTEGER REFERENCES dim_date(date_key),
    before_status       VARCHAR(50) NOT NULL,
    after_status        VARCHAR(50) NOT NULL,
    reviewer_user_sk    INTEGER REFERENCES dim_user(user_sk),
    hours_to_decision   DOUBLE PRECISION,
    occurred_at         TIMESTAMP NOT NULL,
    metric_formula_version VARCHAR(20) NOT NULL DEFAULT 'v1'
);

CREATE TABLE fact_area_context_snapshot (
    area_code           VARCHAR(20) PRIMARY KEY,
    area_sk             INTEGER REFERENCES dim_area(area_sk),
    base_period         VARCHAR(10) NOT NULL,
    store_count_total   INTEGER,
    open_rate_avg       DOUBLE PRECISION,
    close_rate_avg      DOUBLE PRECISION,
    monthly_sales_total BIGINT,
    sales_is_estimate   BOOLEAN NOT NULL DEFAULT TRUE,
    source_name         VARCHAR(255) NOT NULL,
    source_url          TEXT NOT NULL,
    license_type        VARCHAR(100) NOT NULL,
    fetched_at          TIMESTAMP NOT NULL,
    area_mapping_version VARCHAR(50) NOT NULL,
    metric_formula_version VARCHAR(20) NOT NULL DEFAULT 'v1'
);

CREATE TABLE da_kpi_snapshot (
    id                  VARCHAR(36) PRIMARY KEY,
    metric_key          VARCHAR(100) NOT NULL,
    grain_label         VARCHAR(50) NOT NULL,
    segment_json        TEXT,
    metric_value        DOUBLE PRECISION,
    numerator           DOUBLE PRECISION,
    denominator         DOUBLE PRECISION,
    formula_version     VARCHAR(20) NOT NULL,
    computed_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    pipeline_run_id     VARCHAR(36) NOT NULL,
    notes               TEXT
);

CREATE INDEX idx_da_kpi_snapshot_metric ON da_kpi_snapshot (metric_key, computed_at DESC);

INSERT INTO da_metric_versions (metric_key, formula_version, formula_text, grain, owner_team) VALUES
('story_registration', 'v1', 'count(story where status<>DELETED)', 'day/region', 'Product'),
('map_to_detail', 'v1', 'detail_views / map_sessions', 'day', 'Product'),
('participation_rate', 'v1', 'content_creators / registered_users', 'week', 'Product'),
('share_count', 'v1', 'count(share events)', 'day', 'Growth'),
('approval_rate', 'v1', 'APPROVED / (APPROVED+REJECTED)', 'week', 'Ops'),
('time_to_approve', 'v1', 'avg(approved_at - created_at) hours', 'week', 'Ops'),
('curation_ctr', 'v1', 'clicks / impressions', 'day', 'Product'),
('area_context_coverage', 'v1', 'stories_with_area / total_approved', 'month', 'DE'),
('area_engagement_lift', 'v1', 'avg(engagement|has_area) / avg(engagement|no_area) — association only, not causal', 'month', 'Product');

INSERT INTO dim_status (status_code) VALUES
('PENDING'), ('APPROVED'), ('REJECTED'), ('HIDDEN'), ('DELETED');
