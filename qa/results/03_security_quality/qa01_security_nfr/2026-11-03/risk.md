# RISK

## 20261103-010421

- 실행 시각: 2026-11-03T01:04:21+0900
- Git Commit: 16c28b4-dirty
이 RUN에서 새 위험은 없다.

## 20261103-015837

- 실행 시각: 2026-11-03T01:58:37+0900
- Git Commit: fdfdce7-dirty
이 RUN에서 새 위험은 없다.

## 20261103-025928

- 실행 시각: 2026-11-03T02:59:28+0900
- Git Commit: b2120bc-dirty

### RISK-20261103-025928-1 MEDIUM OPEN

- 기능: CodeQL CI
- 관련 TC_ID: TC-SEC-001
- 발생 가능성: 중간
- 영향: 로컬 게이트에는 CodeQL CLI가 없어 CI codeql 잡이 2차 엔진 역할을 한다.
- 내용: CodeQL은 GitHub Actions에서 실행한다. 로컬은 Semgrep+secret_scan으로 교차한다.
- 권장 조치: PR에서 codeql 잡 PASS를 필수 상태로 유지한다.
- 처리 상태: OPEN
- 파일: .github/workflows/qa-gate.yml
- 함수: codeql
- 줄 번호: UNKNOWN
