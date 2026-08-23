-- External Area Context (DE) — UGC와 분리된 공공 상권 Context 레이어
-- 출처: 서울시 상권분석서비스 (공공누리 1유형). Story 사실과 합치지 않음.

CREATE TABLE de_pipeline_runs (
    id                  VARCHAR(36) PRIMARY KEY,
    started_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    finished_at         TIMESTAMP,
    status              VARCHAR(50) NOT NULL DEFAULT 'RUNNING',
    area_mapping_version VARCHAR(50) NOT NULL,
    schema_version      VARCHAR(50) NOT NULL DEFAULT 'v1',
    standard_unit_zone_version VARCHAR(50) NOT NULL DEFAULT '2024',
    source_snapshot_dir TEXT,
    dq_report_path      TEXT,
    notes               TEXT
);

CREATE TABLE de_raw_snapshots (
    id                  VARCHAR(36) PRIMARY KEY,
    pipeline_run_id     VARCHAR(36) NOT NULL REFERENCES de_pipeline_runs(id),
    source_name         VARCHAR(255) NOT NULL,
    source_dataset      VARCHAR(255) NOT NULL,
    source_url          TEXT NOT NULL,
    base_period         VARCHAR(10) NOT NULL,
    license_type        VARCHAR(100) NOT NULL DEFAULT '공공누리 1유형',
    fetched_at          TIMESTAMP NOT NULL,
    checksum_sha256     VARCHAR(64) NOT NULL,
    storage_path        TEXT NOT NULL,
    row_count           INTEGER,
    UNIQUE (source_dataset, base_period, checksum_sha256)
);

CREATE TABLE area_zones (
    area_code           VARCHAR(20) PRIMARY KEY,
    area_name           VARCHAR(255) NOT NULL,
    area_type_code      VARCHAR(20),
    area_type_name      VARCHAR(100),
    gu_code             VARCHAR(10),
    dong_code           VARCHAR(10),
    centroid_lng        DOUBLE PRECISION NOT NULL,
    centroid_lat        DOUBLE PRECISION NOT NULL,
    area_sqm            DOUBLE PRECISION,
    area_mapping_version VARCHAR(50) NOT NULL,
    source_dataset      VARCHAR(255) NOT NULL,
    source_url          TEXT NOT NULL,
    base_period         VARCHAR(10) NOT NULL,
    fetched_at          TIMESTAMP NOT NULL,
    pipeline_run_id     VARCHAR(36) NOT NULL,
    license_type        VARCHAR(100) NOT NULL DEFAULT '공공누리 1유형'
);

CREATE TABLE area_store_stats (
    id                  VARCHAR(36) PRIMARY KEY,
    area_code           VARCHAR(20) NOT NULL REFERENCES area_zones(area_code),
    service_industry_code VARCHAR(20) NOT NULL,
    service_industry_name VARCHAR(255),
    store_count         INTEGER,
    similar_store_count INTEGER,
    open_rate           DOUBLE PRECISION,
    close_rate          DOUBLE PRECISION,
    franchise_store_count INTEGER,
    base_period         VARCHAR(10) NOT NULL,
    area_mapping_version VARCHAR(50) NOT NULL,
    source_dataset      VARCHAR(255) NOT NULL,
    source_url          TEXT NOT NULL,
    fetched_at          TIMESTAMP NOT NULL,
    pipeline_run_id     VARCHAR(36) NOT NULL,
    license_type        VARCHAR(100) NOT NULL DEFAULT '공공누리 1유형',
    UNIQUE (area_code, base_period, service_industry_code)
);

CREATE TABLE area_sales_stats (
    id                  VARCHAR(36) PRIMARY KEY,
    area_code           VARCHAR(20) NOT NULL REFERENCES area_zones(area_code),
    service_industry_code VARCHAR(20) NOT NULL,
    service_industry_name VARCHAR(255),
    monthly_sales_amount BIGINT,
    weekday_sales_amount BIGINT,
    weekend_sales_amount BIGINT,
    base_period         VARCHAR(10) NOT NULL,
    is_estimate         BOOLEAN NOT NULL DEFAULT TRUE,
    area_mapping_version VARCHAR(50) NOT NULL,
    source_dataset      VARCHAR(255) NOT NULL,
    source_url          TEXT NOT NULL,
    fetched_at          TIMESTAMP NOT NULL,
    pipeline_run_id     VARCHAR(36) NOT NULL,
    license_type        VARCHAR(100) NOT NULL DEFAULT '공공누리 1유형',
    UNIQUE (area_code, base_period, service_industry_code)
);

CREATE TABLE place_area_mappings (
    place_id            VARCHAR(36) PRIMARY KEY REFERENCES places(id),
    area_code           VARCHAR(20) NOT NULL REFERENCES area_zones(area_code),
    area_mapping_version VARCHAR(50) NOT NULL,
    distance_m          DOUBLE PRECISION,
    mapped_at           TIMESTAMP NOT NULL DEFAULT NOW(),
    pipeline_run_id     VARCHAR(36) NOT NULL
);

CREATE TABLE mart_area_context (
    area_code           VARCHAR(20) PRIMARY KEY REFERENCES area_zones(area_code),
    area_name           VARCHAR(255) NOT NULL,
    area_type_name      VARCHAR(100),
    base_period         VARCHAR(10) NOT NULL,
    store_count_total   INTEGER,
    open_rate_avg       DOUBLE PRECISION,
    close_rate_avg      DOUBLE PRECISION,
    monthly_sales_total BIGINT,
    sales_is_estimate   BOOLEAN NOT NULL DEFAULT TRUE,
    area_mapping_version VARCHAR(50) NOT NULL,
    source_dataset      VARCHAR(255) NOT NULL,
    source_url          TEXT NOT NULL,
    source_name         VARCHAR(255) NOT NULL,
    fetched_at          TIMESTAMP NOT NULL,
    pipeline_run_id     VARCHAR(36) NOT NULL,
    license_type        VARCHAR(100) NOT NULL DEFAULT '공공누리 1유형',
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_area_zones_centroid ON area_zones(centroid_lat, centroid_lng);
CREATE INDEX idx_place_area_mappings_area ON place_area_mappings(area_code);
CREATE INDEX idx_mart_area_context_period ON mart_area_context(base_period);
