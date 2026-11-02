# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| OPS3-020 | CD SSH·Compose 자동배포 | AI health 미검증 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS3-021 | CD SSH·Compose 자동배포 | BE health 미검증 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS3-022 | CD SSH·Compose 자동배포 | rollback 없음 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS3-023 | CD SSH·Compose 자동배포 | main push 배포 실패 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS3-026 | CD SSH·Compose 자동배포 | 오류 로그 수집 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS3-027 | CD SSH·Compose 자동배포 | 앱 헬스 실사용 | Docker | FAIL | SQL | NOT_RUN | FAIL |

## OPS3-020 AI health 미검증
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 내부 AI API 직접 readiness 검증 추가 필요
- 실제: 배포 검증은 curl http://localhost/ 뿐이고 내부 AI 8000 readiness 확인이 없다.
- 결함ID: DEF-OPS3-020
- 코드: .github/workflows/deploy.yml

## OPS3-021 BE health 미검증
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: API 성공 확인 추가 필요
- 실제: 배포 스크립트에 /api/health 확인이 없다. 프론트 HTML curl만 있다.
- 결함ID: DEF-OPS3-021
- 코드: .github/workflows/deploy.yml

## OPS3-022 rollback 없음
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 자동 이전 버전 복귀 설계 필요
- 실제: deploy.yml에 배포 실패 시 이전 커밋으로 되돌리는 rollback 단계가 없다.
- 결함ID: DEF-OPS3-022
- 코드: .github/workflows/deploy.yml

## OPS3-023 main push 배포 실패
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: CI 성공 게이트 없이 자동 배포되는지 검증
- 실제: deploy.yml은 push main이면 CI 성공 여부와 무관하게 배포한다. workflow_run 성공 게이트가 없다.
- 결함ID: DEF-OPS3-023
- 코드: .github/workflows/deploy.yml

## OPS3-026 오류 로그 수집
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 실패 시 docker compose logs 자동 출력 필요
- 실제: curl 실패 때 docker compose logs를 출력하는 단계가 배포 스크립트에 없다.
- 결함ID: DEF-OPS3-026
- 코드: .github/workflows/deploy.yml

## OPS3-027 앱 헬스 실사용
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 실제 사용자 요청 성공 여부도 확인
- 실제: 배포 헬스체크가 http://localhost/ HTML뿐이고 GET /api/options 사용자 요청 확인이 없다.
- 결함ID: DEF-OPS3-027
- 코드: .github/workflows/deploy.yml
