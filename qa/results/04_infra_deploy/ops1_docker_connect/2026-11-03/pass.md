# PASS

## 20261103-025928

- 실행 시각: 2026-11-03T02:59:28+0900
- Git Commit: b2120bc-dirty
### TC-INFRA-001 Compose·HTTP 스모크

- 실행 시각: 2026-11-03T02:59:28+0900
- Git Commit: b2120bc-dirty
- 영역: 04_infra_deploy
- 섹션: ops1_docker_connect
- 테스트 종류: infra
- 검증 목적: docker compose config/healthcheck와 curl HTTP 스모크 교차
- 도구 A: compose_config / 결과 PASS
- 도구 A 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 qa/runner/tools/infra_compose_check.py`
- 도구 B: curl_health / 결과 PASS
- 도구 B 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 qa/runner/tools/infra_curl_smoke.py`
- 최종 상태: PASS
- 기대 결과: compose config PASS 이고 최소 1개 엔드포인트 HTTP 성공
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] {"status": "PASS", "missing": [], "compose_config_exit": 0} || B[PASS] {"status": "PASS", "results": [{"url": "http://127.0.0.1:5173", "http_code": "000", "curl_exit": 7}, {"url": "http://127.0.0.1:8080/actuator/health", "http_code": "500", "curl_exit": 0}, {"url": "http://127.0.0.1:8000/health", "http_code": "200", "curl_exit": 0}]}
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
