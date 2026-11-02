# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| OPS1-013 | Docker Compose 4서비스 | AI started≠healthy | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS1-024 | Docker Compose 4서비스 | 컨테이너 메모리 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| OPS1-026 | Docker Compose 4서비스 | 동시 배포 | Docker | FAIL | SQL | NOT_RUN | FAIL |

## OPS1-013 AI started≠healthy
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: back 호출 성공이 보장되지 않음; readiness 검증
- 실제: ai에는 healthcheck가 없고 back은 ai를 service_started만 본다. 모델 로딩 실패여도 back이 기동되어 readiness가 보장되지 않는다.
- 결함ID: DEF-OPS1-013
- 코드: compose.yaml

## OPS1-024 컨테이너 메모리
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 메모리 상한/압박 측정
- 실제: compose.yaml와 config 어디에도 AI/서비스 메모리 상한(mem_limit, deploy.resources)이 없다.
- 결함ID: DEF-OPS1-024
- 코드: compose.yaml

## OPS1-026 동시 배포
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 배포 충돌/락 검증
- 실제: compose.yaml과 scripts/deploy.sh에 docker compose up 병렬 실행을 막는 락이 없다.
- 결함ID: DEF-OPS1-026
- 코드: compose.yaml
