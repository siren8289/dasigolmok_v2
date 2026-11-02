# OPS3-026 오류 로그 수집

| 항목 | 내용 |
| --- | --- |
| TC ID | OPS3-026 |
| 분야 | OPS3_배포스크립트 |
| 세부 기능 | CD SSH·Compose 자동배포 |
| 원자 검증 항목 | 오류 로그 수집 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `.github/workflows/deploy.yml` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/.github/workflows/deploy.yml |

## 검증 목적

CD SSH·Compose 자동배포에서 '오류 로그 수집' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

CD SSH·Compose 자동배포 모듈 준비; 입력 사례 '오류 로그 수집'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

curl 실패

## 실행 절차

1. curl 실패 준비
2. CD SSH·Compose 자동배포의 '오류 로그 수집' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

실패 시 docker compose logs 자동 출력 필요

## 판정 기준

PASS: 실패 시 docker compose logs 자동 출력 필요 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | curl 실패 때 docker compose logs를 출력하는 단계가 배포 스크립트에 없다. |
| 결함 ID (Q) | DEF-OPS3-026 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
