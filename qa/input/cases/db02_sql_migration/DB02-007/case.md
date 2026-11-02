# DB02-007 V1 인덱스

| 항목 | 내용 |
| --- | --- |
| TC ID | DB02-007 |
| 분야 | DB02_SQL마이그레이션 |
| 세부 기능 | SQL 스키마 버전·무결성 |
| 원자 검증 항목 | V1 인덱스 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `db/migration/V1__init_schema.sql` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/db/migration/V1__init_schema.sql |

## 검증 목적

SQL 스키마 버전·무결성에서 'V1 인덱스' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

SQL 스키마 버전·무결성 모듈 준비; 입력 사례 'V1 인덱스'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

idx_stories_status

## 실행 절차

1. idx_stories_status 준비
2. SQL 스키마 버전·무결성의 'V1 인덱스' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

인덱스 존재

## 판정 기준

PASS: 인덱스 존재 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | V1은 CREATE INDEX idx_stories_status ON stories(status)를 만들지만, V3__efficiency_optimization.sql이 DROP INDEX IF EXISTS idx_stories_status를 실행한 뒤 같은 이름으로 다시 만들지 않는다. 최종 DB pg_indexes에 idx_stories_status가 없다. |
| 결함 ID (Q) | DEF-DB02-007 |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
