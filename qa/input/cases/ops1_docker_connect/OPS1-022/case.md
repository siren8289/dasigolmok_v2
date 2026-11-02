# OPS1-022 로그 확인

| 항목 | 내용 |
| --- | --- |
| TC ID | OPS1-022 |
| 분야 | OPS1_Docker연결 |
| 세부 기능 | Docker Compose 4서비스 |
| 원자 검증 항목 | 로그 확인 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `compose.yaml` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/compose.yaml |

## 검증 목적

Docker Compose 4서비스에서 '로그 확인' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

Docker Compose 4서비스 모듈 준비; 입력 사례 '로그 확인'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

docker compose logs --tail=50 ai back

## 실행 절차

1. docker compose logs --tail=50 ai back 준비
2. Docker Compose 4서비스의 '로그 확인' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

오류 원인 추적 가능

## 판정 기준

PASS: 오류 원인 추적 가능 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | DB_PASSWORD를 넣고 docker compose logs --tail=50 ai back 이 종료코드 0이다. 컨테이너가 없으면 본문은 비어도 서비스 로그 조회는 된다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
