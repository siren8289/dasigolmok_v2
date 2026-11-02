# OPS1-025 리빌드 후 데이터

| 항목 | 내용 |
| --- | --- |
| TC ID | OPS1-025 |
| 분야 | OPS1_Docker연결 |
| 세부 기능 | Docker Compose 4서비스 |
| 원자 검증 항목 | 리빌드 후 데이터 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `compose.yaml` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/compose.yaml |

## 검증 목적

Docker Compose 4서비스에서 '리빌드 후 데이터' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

Docker Compose 4서비스 모듈 준비; 입력 사례 '리빌드 후 데이터'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

docker compose up --build

## 실행 절차

1. docker compose up --build 준비
2. Docker Compose 4서비스의 '리빌드 후 데이터' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

db-data 소실 없음

## 판정 기준

PASS: db-data 소실 없음 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | db-data는 named volume이고 up --build 경로(deploy.sh, CD)에 down -v가 없어 리빌드만으로 볼륨이 지워지지 않는다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
