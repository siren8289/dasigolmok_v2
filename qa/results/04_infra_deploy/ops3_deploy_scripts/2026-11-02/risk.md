# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| OPS3-001 | CD SSH·Compose 자동배포 | main 푸시 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-002 | CD SSH·Compose 자동배포 | 수동 배포 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-003 | CD SSH·Compose 자동배포 | 누락 SSH 키 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-004 | CD SSH·Compose 자동배포 | 누락 EC2_HOST | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-005 | CD SSH·Compose 자동배포 | SSH 키 권한 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-006 | CD SSH·Compose 자동배포 | SSH 디렉터리 권한 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-007 | CD SSH·Compose 자동배포 | SSH key parse | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-008 | CD SSH·Compose 자동배포 | SSH host fingerprint | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-009 | CD SSH·Compose 자동배포 | SSH ConnectTimeout | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-010 | CD SSH·Compose 자동배포 | 서버 경로 첫 후보 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-011 | CD SSH·Compose 자동배포 | 서버 경로 HOME | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-012 | CD SSH·Compose 자동배포 | 서버 경로 없음 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-013 | CD SSH·Compose 자동배포 | git fetch | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-014 | CD SSH·Compose 자동배포 | git pull ff only | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-015 | CD SSH·Compose 자동배포 | 환경파일 없음 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-016 | CD SSH·Compose 자동배포 | compose config 오류 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-017 | CD SSH·Compose 자동배포 | compose up | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-018 | CD SSH·Compose 자동배포 | 배포 ps | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-019 | CD SSH·Compose 자동배포 | Front health curl | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-024 | CD SSH·Compose 자동배포 | 동시 배포 제한 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS3-025 | CD SSH·Compose 자동배포 | SSH 호스트 신뢰 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |

## OPS3-001 main 푸시
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: deploy.yml on.push.branches에 main이 있어 main 푸시가 CD를 트리거한다.

## OPS3-002 수동 배포
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: deploy.yml on.workflow_dispatch가 있어 수동 배포 트리거가 있다.

## OPS3-003 누락 SSH 키
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: SSH_KEY가 비면 Setup SSH 스크립트가 EC2_SSH_KEY 오류를 내고 종료코드 1로 멈춘다.

## OPS3-004 누락 EC2_HOST
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: EC2_HOST가 비면 스크립트가 EC2_HOST 오류를 내고 0이 아닌 코드로 멈춘다.

## OPS3-005 SSH 키 권한
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 임시 키로 Setup SSH를 실행하니 $HOME/.ssh/deploy_key 모드가 600이다.

## OPS3-006 SSH 디렉터리 권한
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: Setup SSH 실행 후 $HOME/.ssh 디렉터리 모드가 700이다.

## OPS3-007 SSH key parse
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 쓰레기 문자열 키는 ssh-keygen -y 단계에서 실패하고 set -eu 때문에 스크립트가 중단된다.

## OPS3-008 SSH host fingerprint
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ssh-keyscan 스텁 결과가 known_hosts에 추가됐다. 워크플로 원문도 ssh-keyscan -H >> known_hosts 이다.

## OPS3-009 SSH ConnectTimeout
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 배포 ssh 명령에 -o ConnectTimeout=30 이 있다.

## OPS3-010 서버 경로 첫 후보
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 원문 if 순서는 /home/ubuntu/dasigolmok_v2가 먼저다. 두 디렉터리가 있으면 그 분기가 선택된다.

## OPS3-011 서버 경로 HOME
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 첫 경로가 없으면 원문 elif의 $HOME/dasigolmok_v2 분기가 선택된다.

## OPS3-012 서버 경로 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 두 후보 디렉터리가 없으면 원문 else가 오류 문구를 내고 종료코드 1이다.

## OPS3-013 git fetch
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 배포 스크립트에 git fetch origin main이 있고, 임시 origin에서 그 명령이 새 커밋 참조를 받았다.

## OPS3-014 git pull ff only
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 배포 스크립트는 git pull --ff-only origin main이다. 갈라진 임시 저장소에서 그 명령은 머지 커밋 없이 실패했다.

## OPS3-015 환경파일 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 서버 스크립트와 scripts/deploy.sh 모두 .env가 없으면 기동 전에 오류로 종료한다. 저장소 루트 .env는 없다.

## OPS3-016 compose config 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 배포 스크립트는 up 전에 docker compose config --quiet를 호출한다. 깨진 compose.yaml로 config를 실행하면 종료코드가 0이 아니다.

## OPS3-017 compose up
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 원격 스크립트에 docker compose up -d --build --remove-orphans 가 있다. 스택은 기동하지 않았다.

## OPS3-018 배포 ps
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: up 다음에 docker compose ps가 있어 서비스 상태를 출력하도록 되어 있다.

## OPS3-019 Front health curl
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 배포 스크립트가 http://localhost/ 를 curl --fail --retry 10 --retry-delay 3 으로 확인한다.

## OPS3-024 동시 배포 제한
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: concurrency.group=dasigolmok-production, cancel-in-progress=false 라 배포가 취소되지 않고 직렬로 기다린다.

## OPS3-025 SSH 호스트 신뢰
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ssh는 StrictHostKeyChecking=accept-new 다. known_hosts와 다른 기존 키는 OpenSSH가 거부한다.
