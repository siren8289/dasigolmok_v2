# RISK

## 20261103-025928

- 실행 시각: 2026-11-03T02:59:28+0900
- Git Commit: b2120bc-dirty

### RISK-20261103-025928-2 MEDIUM OPEN

- 기능: web_api 도구 확장
- 관련 TC_ID: TC-WEB-API-001
- 발생 가능성: 중간
- 영향: 브라우저 E2E가 없으면 UI 사용 흐름 회귀가 남을 수 있다.
- 내용: Playwright UI E2E는 아직 없다. API는 httpx TestClient와 Schemathesis(OpenAPI)로 교차한다.
- 권장 조치: front에 Playwright를 추가해 02_web_api UI 흐름 TC를 연결한다.
- 처리 상태: OPEN
- 파일: qa/config/test_map.json
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
