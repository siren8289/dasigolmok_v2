# DB02-022 V9 트랜잭션 롤백

| 항목 | 내용 |
| --- | --- |
| TC ID | DB02-022 |
| 분야 | DB02_SQL마이그레이션 |
| 세부 기능 | SQL 스키마 버전·무결성 |
| 원자 검증 항목 | V9 트랜잭션 롤백 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `db/migration/V1__init_schema.sql` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/db/migration/V1__init_schema.sql |

## 검증 목적

SQL 스키마 버전·무결성에서 'V9 트랜잭션 롤백' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

SQL 스키마 버전·무결성 모듈 준비; 입력 사례 'V9 트랜잭션 롤백'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

인덱스 생성 실패

## 실행 절차

1. 인덱스 생성 실패 준비
2. SQL 스키마 버전·무결성의 'V9 트랜잭션 롤백' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

DB 일부 상태 방지

## 판정 기준

PASS: DB 일부 상태 방지 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | V9에는 BEGIN/COMMIT이 없다. psql은 문장마다 커밋하므로 HNSW 인덱스 실패(embedding_missing) 뒤에도 market_knowledge_chunks=market_knowledge_chunks가 남고 이후 support_policies=None는 없다. 일부 상태가 방지되지 않는다. ERROR:  column "embedding_missing" does not exist |
| 결함 ID (Q) | DEF-DB02-022 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
