# OPS1-018 DB 호스트 비공개

| 항목 | 내용 |
| --- | --- |
| TC ID | OPS1-018 |
| 분야 | OPS1_Docker연결 |
| 세부 기능 | Docker Compose 4서비스 |
| 원자 검증 항목 | DB 호스트 비공개 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `compose.yaml` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/compose.yaml |

## 검증 목적

Docker Compose 4서비스에서 'DB 호스트 비공개' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

Docker Compose 4서비스 모듈 준비; 입력 사례 'DB 호스트 비공개'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

db ports 미노출

## 실행 절차

1. db ports 미노출 준비
2. Docker Compose 4서비스의 'DB 호스트 비공개' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

외부 5432 연결 불가

## 판정 기준

PASS: 외부 5432 연결 불가 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | compose config에서 db.ports가 없어 외부 5432 매핑이 없다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
