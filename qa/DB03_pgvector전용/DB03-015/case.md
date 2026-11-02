# DB03-015 DB 정책 실시간 소스

| 항목 | 내용 |
| --- | --- |
| TC ID | DB03-015 |
| 분야 | DB03_pgvector전용 |
| 세부 기능 | RAG 데이터베이스 스키마 |
| 원자 검증 항목 | DB 정책 실시간 소스 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `db/migration/V9__commercial_rag_pgvector.sql` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/db/migration/V9__commercial_rag_pgvector.sql |

## 검증 목적

RAG 데이터베이스 스키마에서 'DB 정책 실시간 소스' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RAG 데이터베이스 스키마 모듈 준비; 입력 사례 'DB 정책 실시간 소스'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

RAG는 정적 샘플 데이터 사용

## 실행 절차

1. RAG는 정적 샘플 데이터 사용 준비
2. RAG 데이터베이스 스키마의 'DB 정책 실시간 소스' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

실제 DB 정책과 연결되어 있는지 검증

## 판정 기준

PASS: 실제 DB 정책과 연결되어 있는지 검증 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | search_policies/get_all_policy_items는 support_policies가 아니라 service.py의 POLICY_DATABASE 정적 목록을 순회한다. 마이그레이션 직후 support_policies 행 수는 테스트 삽입을 포함해 1건이며 RAG 조회 경로와 연결되어 있지 않다. |
| 결함 ID (Q) | DEF-DB03-015 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
