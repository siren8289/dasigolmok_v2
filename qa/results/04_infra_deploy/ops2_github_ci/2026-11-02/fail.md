# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| OPS2-012 | CI 4잡·자동검증 | 워크플로 권한 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS2-014 | CI 4잡·자동검증 | Docker 빌드 누락 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS2-015 | CI 4잡·자동검증 | DB 통합테스트 누락 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS2-017 | CI 4잡·자동검증 | 중복 실행 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS2-018 | CI 4잡·자동검증 | lint 여부 | Docker | FAIL | SQL | NOT_RUN | FAIL |

## OPS2-012 워크플로 권한
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 최소 권한 확인
- 실제: ci.yml에 permissions 최소 권한(contents: read 등) 선언이 없다.
- 결함ID: DEF-OPS2-012
- 코드: .github/workflows/ci.yml

## OPS2-014 Docker 빌드 누락
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 실행 이미지 빌드 검증 추가 검토
- 실제: ci.yml에 docker compose build 또는 docker build 스텝이 없다.
- 결함ID: DEF-OPS2-014
- 코드: .github/workflows/ci.yml

## OPS2-015 DB 통합테스트 누락
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 실제 JPA/SQL 통합테스트 추가 검토
- 실제: ci.yml에 Postgres 서비스가 없고 백엔드 테스트는 H2다. 실제 PostgreSQL JPA/SQL 통합테스트가 없다.
- 결함ID: DEF-OPS2-015
- 코드: .github/workflows/ci.yml

## OPS2-017 중복 실행
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: CI 결과 혼동 없음
- 실제: ci.yml에 concurrency가 없어 같은 커밋의 연속 push 실행이 겹치고 결과를 구분하는 장치가 없다.
- 결함ID: DEF-OPS2-017
- 코드: .github/workflows/ci.yml

## OPS2-018 lint 여부
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 정적 분석 게이트 유무 확인
- 실제: ci.yml에 ESLint, ruff, Checkstyle 등 정적 분석 게이트가 없다.
- 결함ID: DEF-OPS2-018
- 코드: .github/workflows/ci.yml
