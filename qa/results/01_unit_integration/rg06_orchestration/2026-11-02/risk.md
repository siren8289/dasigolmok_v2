# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG06-001 | RAG 의도분류·분기 | 상권 질문 분류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-002 | RAG 의도분류·분기 | 지원 질문 분류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-003 | RAG 의도분류·분기 | 혼합 질문 분류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-004 | RAG 의도분류·분기 | 일반 질문 분류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-005 | RAG 의도분류·분기 | 검증 노드 입력 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-006 | RAG 의도분류·분기 | 지원 의도 도구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-007 | RAG 의도분류·분기 | 상권 의도 도구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-008 | RAG 의도분류·분기 | 혼합 의도 도구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-009 | RAG 의도분류·분기 | 검색 결과 결합 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-010 | RAG 의도분류·분기 | 진단 자동 결합 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-011 | RAG 의도분류·분기 | 진단정보 누락 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-012 | RAG 의도분류·분기 | 지원 날짜 전파 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-013 | RAG 의도분류·분기 | top_k 전파 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-014 | RAG 의도분류·분기 | 질문 원문 보존 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-015 | RAG 의도분류·분기 | 결과 인용 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-016 | RAG 의도분류·분기 | 실행 메타 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-017 | RAG 의도분류·분기 | 검증 경고 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-018 | RAG 의도분류·분기 | 프롬프트 인젝션 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-019 | RAG 의도분류·분기 | 검색 도구 권한 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-022 | RAG 의도분류·분기 | 다른 회사 데이터 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG06-023 | RAG 의도분류·분기 | 반복 실행 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## RG06-001 상권 질문 분류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: '연남동 매출이 어떨까' 의도는 market_analysis 이다.

## RG06-002 지원 질문 분류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: '지원금 신청 방법 알려줘' 의도는 support_policy 이다.

## RG06-003 혼합 질문 분류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: '연남동 폐업률과 지원금' 의도는 hybrid 이다.

## RG06-004 일반 질문 분류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 키워드가 없는 '안녕하세요' 의 기본 의도는 hybrid 이다.

## RG06-005 검증 노드 입력
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 유효한 마포구 질문은 node_validate 로그를 남긴다.

## RG06-006 지원 의도 도구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: support_policy 의도는 정책 검색만 실행한다.

## RG06-007 상권 의도 도구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: market_analysis 의도는 상권 근거 검색만 실행한다.

## RG06-008 혼합 의도 도구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: hybrid 의도는 상권 검색과 정책 검색을 모두 실행한다.

## RG06-009 검색 결과 결합
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 상권 2건과 정책 3건이 evidence_documents 와 policies 로 분리된다.

## RG06-010 진단 자동 결합
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong=연남동, industry=한식 이면 진단 결과가 market_diagnosis 에 붙는다.

## RG06-011 진단정보 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong 만 있고 industry 가 없으면 진단을 생략한다.

## RG06-012 지원 날짜 전파
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: target_date=2026-11-02 가 정책 검색 쿼리에 그대로 전달된다.

## RG06-013 top_k 전파
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: top_k=2 이면 상권 문서와 정책이 각각 2건 이하다.

## RG06-014 질문 원문 보존
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한글과 영문이 섞인 question 이 응답 question 에 보존된다.

## RG06-015 결과 인용
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 검색 문서 2건이면 citations 목록이 만들어진다.

## RG06-016 실행 메타
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 실행 메타데이터에 latency_ms 와 단계 로그가 있다.

## RG06-017 검증 경고
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district=부산시 는 warnings 에 검증 오류로 남는다.

## RG06-018 프롬프트 인젝션
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ignore previous instructions 는 실행을 거절한다.

## RG06-019 검색 도구 권한
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: market_search 권한이 없으면 도구 실행이 차단되고 문서가 비어 있다.

## RG06-022 다른 회사 데이터
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district=강남구 검색 결과에 마포구 문서가 섞이지 않는다.

## RG06-023 반복 실행
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 요청 두 번의 답변·문서·정책이 같다.
