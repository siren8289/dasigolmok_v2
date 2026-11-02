# DB02-009 V6 팩트 테이블

| 항목 | 내용 |
| --- | --- |
| TC ID | DB02-009 |
| 분야 | DB02_SQL마이그레이션 |
| 세부 기능 | SQL 스키마 버전·무결성 |
| 원자 검증 항목 | V6 팩트 테이블 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `db/migration/V1__init_schema.sql` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/db/migration/V1__init_schema.sql |

## 검증 목적

SQL 스키마 버전·무결성에서 'V6 팩트 테이블' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

SQL 스키마 버전·무결성 모듈 준비; 입력 사례 'V6 팩트 테이블'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

fact_story_lifecycle

## 실행 절차

1. fact_story_lifecycle 준비
2. SQL 스키마 버전·무결성의 'V6 팩트 테이블' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

스키마 생성

## 판정 기준

PASS: 스키마 생성 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | fact_story_lifecycle 생성됨. 컬럼 15개, PK 성격의 story_id 포함. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
