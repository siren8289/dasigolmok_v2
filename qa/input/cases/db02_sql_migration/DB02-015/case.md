# DB02-015 레거시 스키마와 현재 JPA

| 항목 | 내용 |
| --- | --- |
| TC ID | DB02-015 |
| 분야 | DB02_SQL마이그레이션 |
| 세부 기능 | SQL 스키마 버전·무결성 |
| 원자 검증 항목 | 레거시 스키마와 현재 JPA |
| 우선순위 | P0 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `db/migration/V1__init_schema.sql` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/db/migration/V1__init_schema.sql |

## 검증 목적

SQL 스키마 버전·무결성에서 '레거시 스키마와 현재 JPA' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

SQL 스키마 버전·무결성 모듈 준비; 입력 사례 '레거시 스키마와 현재 JPA'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

stories vs diagnosis 엔터티

## 실행 절차

1. stories vs diagnosis 엔터티 준비
2. SQL 스키마 버전·무결성의 '레거시 스키마와 현재 JPA' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

서로 다른 기능 구현·테이블 사용처 정리

## 판정 기준

PASS: 서로 다른 기능 구현·테이블 사용처 정리 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | stories는 V1 SQL에만 있고 현재 Spring 엔터티가 없다. diagnosis는 JPA @Table만 있고 V1~V9 CREATE TABLE이 없다. 레거시 스토리 스키마와 진단 엔터티의 테이블 사용처가 정리되어 있지 않다. |
| 결함 ID (Q) | DEF-DB02-015 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
