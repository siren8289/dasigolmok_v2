# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG05-001 | 상권 진단·출처 결합 설명 | 진단 동·업종 있음 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-002 | 상권 진단·출처 결합 설명 | 진단 업종 없음 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-003 | 상권 진단·출처 결합 설명 | 진단 동 없음 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-004 | 상권 진단·출처 결합 설명 | 진단에 오류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-005 | 상권 진단·출처 결합 설명 | 기본 자치구 fallback | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-006 | 상권 진단·출처 결합 설명 | 상권 stable 설명 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-007 | 상권 진단·출처 결합 설명 | 상권 warning 설명 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-008 | 상권 진단·출처 결합 설명 | 상권 danger 설명 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-009 | 상권 진단·출처 결합 설명 | 상권 수치 인용 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-010 | 상권 진단·출처 결합 설명 | 상권 변화명 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-011 | 상권 진단·출처 결합 설명 | 보고서 있는 경우 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-013 | 상권 진단·출처 결합 설명 | 지원사업 open | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-014 | 상권 진단·출처 결합 설명 | 지원사업 마감 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-016 | 상권 진단·출처 결합 설명 | 보고서 citation | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-017 | 상권 진단·출처 결합 설명 | 정책 citation | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-018 | 상권 진단·출처 결합 설명 | 근거 120자 초과 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-019 | 상권 진단·출처 결합 설명 | 키 없음 fallback | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-020 | 상권 진단·출처 결합 설명 | Gemini 정상 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-021 | 상권 진단·출처 결합 설명 | Gemini 에러 fallback | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-022 | 상권 진단·출처 결합 설명 | 필수 추정치 경고 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG05-023 | 상권 진단·출처 결합 설명 | 현장 실사 문구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## RG05-001 진단 동·업종 있음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong 과 industry 가 있으면 base_diagnose 를 호출한다.

## RG05-002 진단 업종 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industry 가 없으면 진단은 None 이고 base_diagnose 를 호출하지 않는다.

## RG05-003 진단 동 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong 이 없으면 진단은 None 이다.

## RG05-004 진단에 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: base_diagnose 가 error 를 반환하면 진단은 None 이다.

## RG05-005 기본 자치구 fallback
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district 가 없으면 base_diagnose 에 마포구를 넣는다.

## RG05-006 상권 stable 설명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=stable 은 안정으로 표기된다.

## RG05-007 상권 warning 설명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=warning 은 주의로 표기된다.

## RG05-008 상권 danger 설명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=danger 는 위험으로 표기된다.

## RG05-009 상권 수치 인용
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 폐업률 5, 예측 4, 매출 500 이 본문에 그대로 들어간다.

## RG05-010 상권 변화명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_name 상권축소가 상권변화 안내로 들어간다.

## RG05-011 보고서 있는 경우
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 근거 문서 2개의 제목과 출처가 본문에 포함된다.

## RG05-013 지원사업 open
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 접수 중 정책은 신청 기간과 지원 혜택을 안내한다.

## RG05-014 지원사업 마감
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마감 정책은 신청 가능으로 안내하지 않는다.

## RG05-016 보고서 citation
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 보고서 인용에 제목, 출처, 분기, 발췌가 들어간다.

## RG05-017 정책 citation
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 정책 인용에 기간과 주관 기관이 들어간다.

## RG05-018 근거 120자 초과
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 200자 본문 인용 snippet 은 120자 더하기 말줄임이다.

## RG05-019 키 없음 fallback
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GEMINI_API_KEY 가 없으면 템플릿 답변과 고지 문구를 쓴다.

## RG05-020 Gemini 정상
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: LLM response.text 가 있으면 그 본문을 반환한다.

## RG05-021 Gemini 에러 fallback
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: LLM 이 예외를 내면 템플릿 답변으로 폴백한다.

## RG05-022 필수 추정치 경고
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 진단만, 문서만, 빈 입력 템플릿 모두 수익 미보장을 적는다.

## RG05-023 현장 실사 문구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 모든 템플릿이 현장 실사와 임대차 계약 검토를 적는다.
