# DB03-016 정책 날짜 CHECK

| 항목 | 내용 |
| --- | --- |
| TC ID | DB03-016 |
| 분야 | DB03_pgvector전용 |
| 세부 기능 | RAG 데이터베이스 스키마 |
| 원자 검증 항목 | 정책 날짜 CHECK |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `db/migration/V9__commercial_rag_pgvector.sql` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/db/migration/V9__commercial_rag_pgvector.sql |

## 검증 목적

RAG 데이터베이스 스키마에서 '정책 날짜 CHECK' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RAG 데이터베이스 스키마 모듈 준비; 입력 사례 '정책 날짜 CHECK'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

end_date<start_date

## 실행 절차

1. end_date<start_date 준비
2. RAG 데이터베이스 스키마의 '정책 날짜 CHECK' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

DB 검증 제약 필요

## 판정 기준

PASS: DB 검증 제약 필요 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | support_policies에 end_date>=start_date CHECK가 없다. start_date='2026-12-31', end_date='2026-01-01' INSERT가 성공했다. 날짜 검증 제약이 필요하다. |
| 결함 ID (Q) | DEF-DB03-016 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
