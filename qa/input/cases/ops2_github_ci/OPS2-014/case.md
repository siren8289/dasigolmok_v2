# OPS2-014 Docker 빌드 누락

| 항목 | 내용 |
| --- | --- |
| TC ID | OPS2-014 |
| 분야 | OPS2_GitHubCI |
| 세부 기능 | CI 4잡·자동검증 |
| 원자 검증 항목 | Docker 빌드 누락 |
| 우선순위 | P0 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `.github/workflows/ci.yml` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/.github/workflows/ci.yml |

## 검증 목적

CI 4잡·자동검증에서 'Docker 빌드 누락' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

CI 4잡·자동검증 모듈 준비; 입력 사례 'Docker 빌드 누락'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

CI에서 docker compose build 없음

## 실행 절차

1. CI에서 docker compose build 없음 준비
2. CI 4잡·자동검증의 'Docker 빌드 누락' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

실행 이미지 빌드 검증 추가 검토

## 판정 기준

PASS: 실행 이미지 빌드 검증 추가 검토 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | ci.yml에 docker compose build 또는 docker build 스텝이 없다. |
| 결함 ID (Q) | DEF-OPS2-014 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
