# OPS1-020 상태 Up 의미

| 항목 | 내용 |
| --- | --- |
| TC ID | OPS1-020 |
| 분야 | OPS1_Docker연결 |
| 세부 기능 | Docker Compose 4서비스 |
| 원자 검증 항목 | 상태 Up 의미 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `compose.yaml` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/compose.yaml |

## 검증 목적

Docker Compose 4서비스에서 '상태 Up 의미' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

Docker Compose 4서비스 모듈 준비; 입력 사례 '상태 Up 의미'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

docker compose ps Up

## 실행 절차

1. docker compose ps Up 준비
2. Docker Compose 4서비스의 '상태 Up 의미' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

실제 health/API 확인 별도 수행

## 판정 기준

PASS: 실제 health/API 확인 별도 수행 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | RISK |
| 실제 결과/증적 (P) | RISK: 기동 중인 스택이 없어 docker compose ps Up과 /api/health를 대조하지 못했다. compose up은 범위 밖이다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
