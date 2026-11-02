# PASS

## 20261103-025928

- 실행 시각: 2026-11-03T02:59:28+0900
- Git Commit: b2120bc-dirty
### TC-WEB-API-001 FastAPI HTTP 계약

- 실행 시각: 2026-11-03T02:59:28+0900
- Git Commit: b2120bc-dirty
- 영역: 02_web_api
- 섹션: ai01_fastapi_contract
- 테스트 종류: api
- 검증 목적: httpx TestClient와 Schemathesis OpenAPI ASGI로 헬스·옵션 API를 교차
- 도구 A: httpx_contract / 결과 PASS
- 도구 A 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 qa/runner/tools/api_contract_httpx.py`
- 도구 B: schemathesis / 결과 PASS
- 도구 B 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 qa/runner/tools/api_smoke_curl.py`
- 최종 상태: PASS
- 기대 결과: health status=ok 이고 options에 districts/dongs/industries
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] hecks": [{"name": "health", "status": 200, "body": {"status": "ok", "version": "2.1.0"}}, {"name": "options", "status": 200, "keys": ["districts", "dongs", "industries", "semas_dong_count", "semas_upjong_count"]}]}

/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
  from starlette.testclient import TestClient as TestClient  # noqa || B[PASS] {"status": "PASS", "checked": [{"path": "/health", "status": 200}, {"path": "/api/v1/options", "status": 200}], "failures": [], "engine": "schemathesis"}
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: RISK-20261103-025928-2
