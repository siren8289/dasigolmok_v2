#!/usr/bin/env python3
"""Migrate Korean QA result folders to English snake_case layout."""

from __future__ import annotations

import csv
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / "qa"

AREA_MAP = {
    "단위·통합 테스트": "01_unit_integration",
    "웹·API 테스트": "02_web_api",
    "보안·품질 검사": "03_security_quality",
    "인프라·배포 검사": "04_infra_deploy",
}

SECTION_MAP = {
    "AI01_FastAPI계약": "ai01_fastapi_contract",
    "AI02_옵션조회": "ai02_options_query",
    "AI03_진단파이프라인": "ai03_diagnosis_pipeline",
    "AI04_추천파이프라인": "ai04_recommend_pipeline",
    "AI05_위험판정경계": "ai05_risk_boundary",
    "AI06_학습피처": "ai06_training_features",
    "AI07_폐업ML추론": "ai07_closure_ml_inference",
    "AI08_매출DL추론": "ai08_sales_dl_inference",
    "AI09_LLM기본설명": "ai09_llm_basic_explain",
    "BE01_진단요청DTO": "be01_diagnosis_request_dto",
    "BE02_진단CRUD": "be02_diagnosis_crud",
    "BE03_진단HTTP": "be03_diagnosis_http",
    "BE04_추천HTTP": "be04_recommend_http",
    "BE05_AI연동예외": "be05_ai_integration_errors",
    "BE06_전역예외": "be06_global_exception",
    "DB01_진단영속성": "db01_diagnosis_persistence",
    "DB02_SQL마이그레이션": "db02_sql_migration",
    "DB03_pgvector전용": "db03_pgvector",
    "DE01_공공API수집": "de01_public_api_ingest",
    "DE02_CSV인코딩": "de02_csv_encoding",
    "DE03_점포정제": "de03_store_clean",
    "DE04_매출인구정제": "de04_sales_pop_clean",
    "DE05_결측치이상치": "de05_missing_outlier",
    "DE06_테이블결합": "de06_table_join",
    "DE07_옵션생성": "de07_options_build",
    "DE08_ETL실행저장": "de08_etl_run_store",
    "FE01_공통라우팅": "fe01_common_routing",
    "FE02_진단입력UI": "fe02_diagnosis_input_ui",
    "FE03_진단결과UI": "fe03_diagnosis_result_ui",
    "FE04_추천UI": "fe04_recommend_ui",
    "FE05_HTTP클라이언트": "fe05_http_client",
    "OPS1_Docker연결": "ops1_docker_connect",
    "OPS2_GitHubCI": "ops2_github_ci",
    "OPS3_배포스크립트": "ops3_deploy_scripts",
    "QA01_보안비기능": "qa01_security_nfr",
    "QA02_문서추적회귀": "qa02_doc_trace_regression",
    "RG01_RAG_HTTP": "rg01_rag_http",
    "RG02_지식베이스": "rg02_knowledge_base",
    "RG03_상권근거검색": "rg03_market_evidence_search",
    "RG04_지원정책규칙": "rg04_support_policy_rules",
    "RG05_종합가이드": "rg05_commercial_guidance",
    "RG06_오케스트레이션": "rg06_orchestration",
    "RG07_보안하네스": "rg07_security_harness",
    "RG08_RAG정량평가": "rg08_rag_eval",
}

SECTION_TO_AREA = {
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

MASTER_HEADER = [
    "tc_id",
    "area",
    "section",
    "feature",
    "item",
    "verify_a",
    "verify_a_result",
    "verify_b",
    "verify_b_result",
    "final_status",
    "expected",
    "actual",
    "defect_id",
    "code_path",
    "executed_on",
]


def flatten(value: object) -> str:
    return " ".join(str(value or "").replace("\t", " ").split())


def rewrite_summary(path: Path, area: str, section: str) -> None:
    if not path.exists():
        return
    rows = list(csv.DictReader(path.read_text(encoding="utf-8-sig").splitlines(), delimiter="\t"))
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MASTER_HEADER, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "tc_id": row.get("TC_ID") or row.get("tc_id") or "",
                    "area": area,
                    "section": section,
                    "feature": row.get("기능") or row.get("feature") or "",
                    "item": row.get("항목") or row.get("item") or "",
                    "verify_a": row.get("검증A") or row.get("verify_a") or "",
                    "verify_a_result": row.get("검증A결과") or row.get("verify_a_result") or "",
                    "verify_b": row.get("검증B") or row.get("verify_b") or "",
                    "verify_b_result": row.get("검증B결과") or row.get("verify_b_result") or "",
                    "final_status": row.get("최종상태") or row.get("final_status") or "",
                    "expected": row.get("예상결과") or row.get("expected") or "",
                    "actual": row.get("실제결과") or row.get("actual") or "",
                    "defect_id": row.get("결함ID") or row.get("defect_id") or "",
                    "code_path": row.get("코드경로") or row.get("code_path") or "",
                    "executed_on": row.get("실행일") or row.get("executed_on") or "",
                }
            )


def sync_xlsx(folder: Path) -> None:
    summary = folder / "summary.tsv"
    if not summary.exists():
        return
    try:
        from openpyxl import Workbook
    except ImportError:
        return
    rows = list(csv.DictReader(summary.read_text(encoding="utf-8-sig").splitlines(), delimiter="\t"))
    wb = Workbook()
    ws = wb.active
    ws.title = "results"
    ws.append(MASTER_HEADER)
    for row in rows:
        ws.append([row.get(col, "") for col in MASTER_HEADER])
    target = folder / "test_sheet.xlsx"
    old = folder / "테스트_시트.xlsx"
    wb.save(target)
    if old.exists() and old != target:
        old.unlink()


def migrate_results() -> None:
    results = QA / "results"
    for area_ko, area_en in AREA_MAP.items():
        src_area = QA / area_ko
        if not src_area.is_dir():
            continue
        for section_dir in sorted(src_area.iterdir()):
            if not section_dir.is_dir():
                continue
            section_en = SECTION_MAP.get(section_dir.name)
            if not section_en:
                raise SystemExit(f"unknown section {section_dir.name}")
            for day_dir in sorted(section_dir.iterdir()):
                if not day_dir.is_dir() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day_dir.name):
                    continue
                dest = results / area_en / section_en / day_dir.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(day_dir, dest)
                rewrite_summary(dest / "summary.tsv", area_en, section_en)
                sync_xlsx(dest)
        shutil.rmtree(src_area)


def migrate_case_cards() -> None:
    cases_root = QA / "input" / "cases"
    for old_name, section_en in SECTION_MAP.items():
        src = QA / old_name
        if not src.is_dir():
            continue
        dest = cases_root / section_en
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        shutil.rmtree(src)


def write_master_and_input() -> None:
    source = QA / "전체_파트_시트.tsv"
    if not source.exists():
        source = QA / "QA_MASTER.tsv"
    rows_out: list[dict[str, str]] = []
    if source.name.startswith("전체") or source.name == "전체_파트_시트.tsv":
        with source.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                section_ko = row.get("섹션") or ""
                area_ko = row.get("영역") or ""
                section_en = SECTION_MAP.get(section_ko, section_ko)
                area_en = AREA_MAP.get(area_ko) or SECTION_TO_AREA.get(section_en, "")
                rows_out.append(
                    {
                        "tc_id": row.get("TC_ID") or "",
                        "area": area_en,
                        "section": section_en,
                        "feature": row.get("기능") or "",
                        "item": row.get("항목") or "",
                        "verify_a": row.get("검증A") or "",
                        "verify_a_result": row.get("검증A결과") or "",
                        "verify_b": row.get("검증B") or "",
                        "verify_b_result": row.get("검증B결과") or "",
                        "final_status": row.get("최종상태") or "",
                        "expected": row.get("예상결과") or "",
                        "actual": row.get("실제결과") or "",
                        "defect_id": row.get("결함ID") or "",
                        "code_path": row.get("코드경로") or "",
                        "executed_on": row.get("실행일") or "",
                    }
                )
    else:
        with source.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                section_ko = row.get("분야") or ""
                section_en = SECTION_MAP.get(section_ko, section_ko)
                rows_out.append(
                    {
                        "tc_id": row.get("TC ID") or "",
                        "area": SECTION_TO_AREA.get(section_en, ""),
                        "section": section_en,
                        "feature": section_en,
                        "item": row.get("원자 검증 항목") or "",
                        "verify_a": "",
                        "verify_a_result": row.get("실행 상태") or "",
                        "verify_b": "",
                        "verify_b_result": "NOT_RUN",
                        "final_status": row.get("실행 상태") or "",
                        "expected": "",
                        "actual": row.get("실제 결과/증적") or "",
                        "defect_id": row.get("결함 ID") or "",
                        "code_path": "",
                        "executed_on": "",
                    }
                )

    master = QA / "master_test_sheet.tsv"
    with master.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MASTER_HEADER, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows_out:
            writer.writerow({k: flatten(row.get(k, "")) for k in MASTER_HEADER})

    input_dir = QA / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    testcases = input_dir / "testcases.tsv"
    tc_header = ["tc_id", "area", "section", "feature", "item", "expected", "code_path"]
    with testcases.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tc_header, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows_out:
            writer.writerow({k: flatten(row.get(k, "")) for k in tc_header})

    for stale in [
        QA / "전체_파트_시트.tsv",
        QA / "전체_파트_시트.xlsx",
        QA / "master_test_sheet.xlsx",
    ]:
        if stale.exists():
            stale.unlink()


def main() -> None:
    (QA / "results").mkdir(parents=True, exist_ok=True)
    (QA / "input").mkdir(parents=True, exist_ok=True)
    for area in AREA_MAP.values():
        (QA / "results" / area).mkdir(parents=True, exist_ok=True)
    migrate_results()
    migrate_case_cards()
    write_master_and_input()
    print("migrated to English QA layout")
    print(f"areas={[p.name for p in (QA / 'results').iterdir() if p.is_dir()]}")
    print(f"master_rows={sum(1 for _ in (QA / 'master_test_sheet.tsv').open(encoding='utf-8-sig')) - 1}")


if __name__ == "__main__":
    main()
