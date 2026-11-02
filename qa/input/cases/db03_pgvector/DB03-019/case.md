# DB03-019 정책 갱신/삭제

| 항목 | 내용 |
| --- | --- |
| TC ID | DB03-019 |
| 분야 | DB03_pgvector전용 |
| 세부 기능 | RAG 데이터베이스 스키마 |
| 원자 검증 항목 | 정책 갱신/삭제 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `db/migration/V9__commercial_rag_pgvector.sql` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/db/migration/V9__commercial_rag_pgvector.sql |

## 검증 목적

RAG 데이터베이스 스키마에서 '정책 갱신/삭제' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RAG 데이터베이스 스키마 모듈 준비; 입력 사례 '정책 갱신/삭제'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

만료된 항목

## 실행 절차

1. 만료된 항목 준비
2. RAG 데이터베이스 스키마의 '정책 갱신/삭제' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

데이터 갱신 전략 명세 필요

## 판정 기준

PASS: 데이터 갱신 전략 명세 필요 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | 만료 정책(2024-01-01~2024-06-30)이 support_policies에 그대로 저장된다. 컬럼은 ['id', 'title', 'organization', 'target_district', 'target_industry', 'start_date', 'end_date', 'support_amount', 'description', 'eligibility', 'source_url', 'created_at']뿐이고 deleted_at/status/updated_at이 없다. support_policy/service.py는 정적 POLICY_DATABASE만 읽고 갱신·삭제 SQL이 없다. 갱신 전략이 명세되어 있지 않다. |
| 결함 ID (Q) | DEF-DB03-019 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
