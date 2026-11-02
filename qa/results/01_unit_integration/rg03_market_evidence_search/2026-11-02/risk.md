# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG03-001 | 하이브리드 검색·재순위화 | 보고서만 검색 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-002 | 하이브리드 검색·재순위화 | 지역 일치 필터 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-003 | 하이브리드 검색·재순위화 | 지역 다름 배제 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-004 | 하이브리드 검색·재순위화 | 행정동 선택 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-005 | 하이브리드 검색·재순위화 | 구 선택 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-006 | 하이브리드 검색·재순위화 | 업종 선택 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-007 | 하이브리드 검색·재순위화 | 키워드 일치 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-008 | 하이브리드 검색·재순위화 | 유사도 원본 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-009 | 하이브리드 검색·재순위화 | rerank 정렬 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-010 | 하이브리드 검색·재순위화 | top_k 1 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-011 | 하이브리드 검색·재순위화 | top_k 3 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-012 | 하이브리드 검색·재순위화 | top_k 20 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-014 | 하이브리드 검색·재순위화 | 없는 자치구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-020 | 하이브리드 검색·재순위화 | 문서 캐시 재사용 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-021 | 하이브리드 검색·재순위화 | 임베딩 캐시 재사용 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-022 | 하이브리드 검색·재순위화 | pgvector SQL | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-023 | 하이브리드 검색·재순위화 | pgvector SQL 파라미터 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG03-024 | 하이브리드 검색·재순위화 | pgvector 연결 실패 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## RG03-001 보고서만 검색
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마포구 검색 결과는 market_report 만 포함한다.

## RG03-002 지역 일치 필터
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district=마포구 1차 결과는 마포구 보고서만 담는다.

## RG03-003 지역 다름 배제
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district=마포구 결과에서 강남구 문서는 빠진다.

## RG03-004 행정동 선택
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 행정동 연남동 일치는 rerank 점수에 0.3 을 더한다.

## RG03-005 구 선택
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 자치구 일치는 rerank 점수에 0.2 를 더한다.

## RG03-006 업종 선택
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 업종 일치는 rerank 점수에 0.2 를 더한다.

## RG03-007 키워드 일치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 쿼리 토큰 2개 중 1개 일치는 0.1(비율 0.5×0.2)을 더한다.

## RG03-008 유사도 원본
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 가산이 없으면 원본 score 0.75 가 유지된다.

## RG03-009 rerank 정렬
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: rerank 결과는 score 내림차순이다.

## RG03-010 top_k 1
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: top_k=1 이면 문서 1개만 반환한다.

## RG03-011 top_k 3
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 후보 5개에 top_k=3 이면 최대 3개다.

## RG03-012 top_k 20
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: top_k=20 이어도 마포구 보고서 후보 수를 넘지 않는다.

## RG03-014 없는 자치구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 없는 자치구는 전체 상권 보고서 fallback 으로 여러 구 문서를 반환한다.

## RG03-020 문서 캐시 재사용
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 청크 캐시가 있으면 build_document_chunks 는 한 번만 호출된다.

## RG03-021 임베딩 캐시 재사용
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 임베딩 캐시가 있으면 두 번째 조회에서 get_embedding 을 다시 호출하지 않는다.

## RG03-022 pgvector SQL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: pgvector SQL 이 district, dong, industry, quarter 를 바인딩한다.

## RG03-023 pgvector SQL 파라미터
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: DROP 문자열이 SQL 본문에 이어 붙지 않고 파라미터로만 전달된다.

## RG03-024 pgvector 연결 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 연결이 없거나 execute 가 실패하면 빈 목록을 반환한다.
