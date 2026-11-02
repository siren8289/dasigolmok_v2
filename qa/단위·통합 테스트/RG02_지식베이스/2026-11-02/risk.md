# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG02-001 | 상권 문서 청킹·임베딩 | 지식 문서 로드 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-002 | 상권 문서 청킹·임베딩 | 문서 종류 분류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-003 | 상권 문서 청킹·임베딩 | 행정동 메타데이터 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-004 | 상권 문서 청킹·임베딩 | 업종 메타데이터 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-005 | 상권 문서 청킹·임베딩 | 분기 메타데이터 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-006 | 상권 문서 청킹·임베딩 | 출처 URL | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-007 | 상권 문서 청킹·임베딩 | 공고 날짜 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-008 | 상권 문서 청킹·임베딩 | 짧은 문서 청킹 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-009 | 상권 문서 청킹·임베딩 | 경계 딱 맞는 문서 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-010 | 상권 문서 청킹·임베딩 | 긴 문서 청킹 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-011 | 상권 문서 청킹·임베딩 | 중첩량 보존 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-015 | 상권 문서 청킹·임베딩 | 청크 출처 보존 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-016 | 상권 문서 청킹·임베딩 | 문서 ID 유일 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-017 | 상권 문서 청킹·임베딩 | 오프라인 임베딩 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-018 | 상권 문서 청킹·임베딩 | 외부 API 임베딩 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-019 | 상권 문서 청킹·임베딩 | Gemini 오류 fallback | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-020 | 상권 문서 청킹·임베딩 | 빈 문자열 임베딩 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-021 | 상권 문서 청킹·임베딩 | 벡터 유사도 자기일치 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG02-022 | 상권 문서 청킹·임베딩 | 벡터 유사도 영벡터 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## RG02-001 지식 문서 로드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 원본 지식 문서에 상권 보고서와 지원사업이 함께 있다.

## RG02-002 문서 종류 분류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 청크 doc_type 이 원본 market_report/support_policy 를 유지한다.

## RG02-003 행정동 메타데이터
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 연남동 보고서 청크는 district=마포구, dong=연남동 으로 분리된다.

## RG02-004 업종 메타데이터
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 연남동 보고서 청크 industry 가 한식음식점으로 보존된다.

## RG02-005 분기 메타데이터
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 연남동 보고서 청크 quarter 가 2024-4 로 보존된다.

## RG02-006 출처 URL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 출처 URL https://golmok.seoul.go.kr 이 청크에 보존된다.

## RG02-007 공고 날짜
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 안심창업 공고 청크가 start_date=2026-01-05, end_date=2026-12-31 을 유지한다.

## RG02-008 짧은 문서 청킹
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: max_chunk_size 보다 짧은 본문은 청크 1개다.

## RG02-009 경계 딱 맞는 문서
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 길이가 max_chunk_size 와 같은 본문은 청크 1개다.

## RG02-010 긴 문서 청킹
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: max_chunk_size 를 넘는 본문은 중첩 청크가 2개 이상이다.

## RG02-011 중첩량 보존
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: overlap=50 이면 인접 청크 본문이 50자 겹친다.

## RG02-015 청크 출처 보존
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한 문서의 모든 청크가 title, source, dong 을 유지한다.

## RG02-016 문서 ID 유일
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: build_document_chunks 청크 ID 가 중복되지 않는다.

## RG02-017 오프라인 임베딩
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: API 키 없이 get_embedding 은 64차원 로컬 벡터를 반환한다.

## RG02-018 외부 API 임베딩
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GEMINI_API_KEY 가 있으면 Gemini 임베딩 값을 그대로 반환한다.

## RG02-019 Gemini 오류 fallback
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: Gemini 호출이 실패하면 64차원 로컬 임베딩으로 폴백한다.

## RG02-020 빈 문자열 임베딩
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 빈 문자열 임베딩은 64차원 영벡터이고 0으로 나누지 않는다.

## RG02-021 벡터 유사도 자기일치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 벡터의 코사인 유사도는 1.0 이다.

## RG02-022 벡터 유사도 영벡터
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 영벡터와의 코사인 유사도는 0.0 이다.
