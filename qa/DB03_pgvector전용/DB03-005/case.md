# DB03-005 doc_type NOT NULL

| 항목 | 내용 |
| --- | --- |
| TC ID | DB03-005 |
| 분야 | DB03_pgvector전용 |
| 세부 기능 | RAG 데이터베이스 스키마 |
| 원자 검증 항목 | doc_type NOT NULL |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `db/migration/V9__commercial_rag_pgvector.sql` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/db/migration/V9__commercial_rag_pgvector.sql |

## 검증 목적

RAG 데이터베이스 스키마에서 'doc_type NOT NULL' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RAG 데이터베이스 스키마 모듈 준비; 입력 사례 'doc_type NOT NULL'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

doc_type=null

## 실행 절차

1. doc_type=null 준비
2. RAG 데이터베이스 스키마의 'doc_type NOT NULL' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

저장 차단

## 판정 기준

PASS: 저장 차단 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | doc_type NULL 저장이 차단됐다. 23502 null value in column "doc_type" of relation "market_knowledge_chunks" violates not-null constraint |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
