"""QA four-area and section mapping.

Result path: qa/results/{area}/{section}/{YYYY-MM-DD}/
"""

from __future__ import annotations

AREAS = (
    "01_unit_integration",
    "02_web_api",
    "03_security_quality",
    "04_infra_deploy",
)

SECTION_TO_AREA: dict[str, str] = {
    "ai05_risk_boundary": "01_unit_integration",
    "ai06_training_features": "01_unit_integration",
    "ai07_closure_ml_inference": "01_unit_integration",
    "ai08_sales_dl_inference": "01_unit_integration",
    "ai09_llm_basic_explain": "01_unit_integration",
    "be01_diagnosis_request_dto": "01_unit_integration",
    "be02_diagnosis_crud": "01_unit_integration",
    "db01_diagnosis_persistence": "01_unit_integration",
    "db02_sql_migration": "01_unit_integration",
    "db03_pgvector": "01_unit_integration",
    "de01_public_api_ingest": "01_unit_integration",
    "de02_csv_encoding": "01_unit_integration",
    "de03_store_clean": "01_unit_integration",
    "de04_sales_pop_clean": "01_unit_integration",
    "de05_missing_outlier": "01_unit_integration",
    "de06_table_join": "01_unit_integration",
    "de07_options_build": "01_unit_integration",
    "de08_etl_run_store": "01_unit_integration",
    "rg02_knowledge_base": "01_unit_integration",
    "rg03_market_evidence_search": "01_unit_integration",
    "rg04_support_policy_rules": "01_unit_integration",
    "rg05_commercial_guidance": "01_unit_integration",
    "rg06_orchestration": "01_unit_integration",
    "rg08_rag_eval": "01_unit_integration",
    "ai01_fastapi_contract": "02_web_api",
    "ai02_options_query": "02_web_api",
    "ai03_diagnosis_pipeline": "02_web_api",
    "ai04_recommend_pipeline": "02_web_api",
    "be03_diagnosis_http": "02_web_api",
    "be04_recommend_http": "02_web_api",
    "fe01_common_routing": "02_web_api",
    "fe02_diagnosis_input_ui": "02_web_api",
    "fe03_diagnosis_result_ui": "02_web_api",
    "fe04_recommend_ui": "02_web_api",
    "fe05_http_client": "02_web_api",
    "rg01_rag_http": "02_web_api",
    "be05_ai_integration_errors": "03_security_quality",
    "be06_global_exception": "03_security_quality",
    "qa01_security_nfr": "03_security_quality",
    "qa02_doc_trace_regression": "03_security_quality",
    "rg07_security_harness": "03_security_quality",
    "ops1_docker_connect": "04_infra_deploy",
    "ops2_github_ci": "04_infra_deploy",
    "ops3_deploy_scripts": "04_infra_deploy",
}

# Gate check → (area, section)
CHECK_TO_SECTION: dict[str, tuple[str, str]] = {
    "record": ("03_security_quality", "qa02_doc_trace_regression"),
    "security": ("03_security_quality", "qa01_security_nfr"),
    "front": ("02_web_api", "fe01_common_routing"),
    "python": ("01_unit_integration", "de05_missing_outlier"),
    "java": ("01_unit_integration", "be01_diagnosis_request_dto"),
    "regression": ("01_unit_integration", "de05_missing_outlier"),
}


def resolve_area_section(section: str, area: str = "") -> tuple[str, str]:
    if area and section:
        return area, section
    mapped = SECTION_TO_AREA.get(section)
    if not mapped:
        raise ValueError(f"unknown QA section: {section}")
    return mapped, section
