"""DE pipeline configuration (stdlib only). Catalog YAML is the human-readable twin."""
from pathlib import Path

DE_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = DE_ROOT / "fixtures"
DATA_RAW = DE_ROOT / "data" / "raw"
DATA_QUARANTINE = DE_ROOT / "data" / "quarantine"
DATA_STAGING = DE_ROOT / "data" / "staging"
REPORTS = DE_ROOT / "reports"

AREA_MAPPING_VERSION = "2024-standard-unit-zone"
STANDARD_UNIT_ZONE_VERSION = "2024"
SCHEMA_VERSION = "v1"
MIN_YEAR = 2021

DQ_COMPLETENESS_MIN = 0.98
DQ_SCHEMA_PASS_MIN = 0.99
DQ_ROW_RECONCILE_MAX_DIFF = 0.001

DATASETS = {
    "seoul_area_geometry": {
        "name": "서울시 상권분석서비스(영역-상권)",
        "source_url": "https://www.data.go.kr/data/15076394/fileData.do",
        "license_type": "공공누리 1유형",
        "fixture": "areas_geometry.csv",
        "kind": "geometry",
    },
    "seoul_store_area": {
        "name": "서울시 상권분석서비스(점포-상권)",
        "source_url": "https://data.seoul.go.kr/dataList/OA-15577/S/1/datasetView.do",
        "license_type": "공공누리 1유형",
        "fixture": "stores_area_2024Q1.csv",
        "kind": "stores",
    },
    "seoul_sales_area": {
        "name": "서울시 상권분석서비스(추정매출-상권)",
        "source_url": "https://data.seoul.go.kr/dataList/OA-15572/S/1/datasetView.do",
        "license_type": "공공누리 1유형",
        "fixture": "sales_area_2024Q1.csv",
        "kind": "sales",
    },
}

# Seoul bbox for mapping eligibility (approx)
SEOUL_BBOX = (126.76, 37.42, 127.18, 37.70)
MAPPING_MAX_DISTANCE_M = 1500.0
