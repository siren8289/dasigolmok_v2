# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG01-001 | 상권 RAG API | RAG health | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-002 | 상권 RAG API | RAG ask 정상 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-003 | 상권 RAG API | 시장 검색 정상 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-004 | 상권 RAG API | 정책 검색 정상 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-005 | 상권 RAG API | 평가 정상 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-006 | 상권 RAG API | RAG ask question 누락 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-007 | 상권 RAG API | RAG ask question null | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-009 | 상권 RAG API | 시장 검색 query 누락 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-010 | 상권 RAG API | 정책 검색 입력 없음 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-014 | 상권 RAG API | RAG ask 내부 예외 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-015 | 상권 RAG API | 지원 정책 내부 예외 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-016 | 상권 RAG API | 평가 내부 예외 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG01-018 | 상권 RAG API | RAG JSON 응답 타입 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## RG01-001 RAG health
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GET /health 가 status=ok, feature=commercial_rag_001 을 반환한다.

## RG01-002 RAG ask 정상
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: question='연남동 창업은?' POST /ask 가 200 CommercialRagResponse 이다.

## RG01-003 시장 검색 정상
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 시장 검색 POST /market-search 가 200 MarketSearchResponse 이다.

## RG01-004 정책 검색 정상
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 정책 검색 POST /support-policies 가 200 SupportPolicyResponse 이다.

## RG01-005 평가 정상
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST /evaluate 가 200 EvaluationMetrics 이다.

## RG01-006 RAG ask question 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: question 필드 누락 POST /ask 는 422 이다.

## RG01-007 RAG ask question null
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: question=null POST /ask 는 422 이다.

## RG01-009 시장 검색 query 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 시장 검색 query 누락은 422 이다.

## RG01-010 정책 검색 입력 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 본문 없는 정책 검색은 기본값으로 200과 정책 목록을 반환한다.

## RG01-014 RAG ask 내부 예외
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: RAG ask 내부 예외는 HTTP 500 detail 로 반환된다.

## RG01-015 지원 정책 내부 예외
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 지원 정책 내부 예외는 HTTP 500 detail 이다.

## RG01-016 평가 내부 예외
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 평가 내부 예외는 HTTP 500 detail 이다.

## RG01-018 RAG JSON 응답 타입
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST /ask JSON 필수 필드 타입이 스키마와 일치한다.
