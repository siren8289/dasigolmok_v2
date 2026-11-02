# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG08-001 | RAG 품질 지표·평가 | Recall 완전 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-002 | RAG 품질 지표·평가 | Recall 절반 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-003 | RAG 품질 지표·평가 | Recall 0 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-004 | RAG 품질 지표·평가 | Recall 기준 없음 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-005 | RAG 품질 지표·평가 | 인용 정확 100% | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-006 | RAG 품질 지표·평가 | 인용 정확 50% | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-007 | RAG 품질 지표·평가 | 인용 정확 0% | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-008 | RAG 품질 지표·평가 | 인용 없음 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-009 | RAG 품질 지표·평가 | 지역 적합성 완전 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-010 | RAG 품질 지표·평가 | 지역 적합성 절반 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-011 | RAG 품질 지표·평가 | 타구 근거만 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-012 | RAG 품질 지표·평가 | 지역 선택 없음 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-013 | RAG 품질 지표·평가 | 종료 정책 오안내 없음 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-014 | RAG 품질 지표·평가 | 종료 정책 오안내 1건 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-015 | RAG 품질 지표·평가 | 마감 지원 없음 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-016 | RAG 품질 지표·평가 | 샘플 평가 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-017 | RAG 품질 지표·평가 | 지표 범위 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-018 | RAG 품질 지표·평가 | 자료 없음 분모 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-019 | RAG 품질 지표·평가 | 재현성 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-020 | RAG 품질 지표·평가 | 평가 결과 노출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG08-022 | RAG 품질 지표·평가 | 인용 위조 회귀 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## RG08-001 Recall 완전
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: retrieved [A,B], relevant [A,B] 의 Recall@K 는 1.0 이다.

## RG08-002 Recall 절반
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: retrieved [A], relevant [A,B] 의 Recall@K 는 0.5 이다.

## RG08-003 Recall 0
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: retrieved 가 비고 relevant 가 [A] 이면 Recall@K 는 0 이다.

## RG08-004 Recall 기준 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: relevant 가 비면 Recall@K 정의값은 1.0 이다.

## RG08-005 인용 정확 100%
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 인용 제목이 모두 실제 문서에 있으면 인용 정확도는 1.0 이다.

## RG08-006 인용 정확 50%
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 인용 2개 중 1개만 실제 문서이면 인용 정확도는 0.5 이다.

## RG08-007 인용 정확 0%
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 인용이 모두 실제 문서에 없으면 인용 정확도는 0 이다.

## RG08-008 인용 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 인용이 없으면 인용 정확도 분모 정책은 1.0 이다.

## RG08-009 지역 적합성 완전
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 문서가 모두 마포구이면 지역 적합성은 1.0 이다.

## RG08-010 지역 적합성 절반
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 문서 2개 중 1개만 마포구이면 지역 적합성은 0.5 이다.

## RG08-011 타구 근거만
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 문서가 모두 강남구이고 질문이 마포구이면 지역 적합성은 0 이다.

## RG08-012 지역 선택 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: target_district 가 없으면 지역 적합성 기본값은 1.0 이다.

## RG08-013 종료 정책 오안내 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: closed 이고 is_open=False 이면 종료 정책 오안내율은 0.0 이다.

## RG08-014 종료 정책 오안내 1건
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: closed 인데 is_open=True 가 1건이면 오안내율은 1/N 이다.

## RG08-015 마감 지원 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 정책이 없으면 종료 정책 오안내율은 0.0 이다.

## RG08-016 샘플 평가
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: run_evaluation_suite 는 4개 지표와 total_evaluated, items 를 반환한다.

## RG08-017 지표 범위
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 평가 지표 4개는 모두 0 이상 1 이하다.

## RG08-018 자료 없음 분모
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 빈 test_cases 로 평가해도 ZeroDivisionError 가 나지 않는다.

## RG08-019 재현성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 기본 스위트를 두 번 실행하면 4개 지표와 건수가 같다.

## RG08-020 평가 결과 노출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST /evaluate 의 items 길이와 total_evaluated 가 같다.

## RG08-022 인용 위조 회귀
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 실제 문서 제목이 아닌 인용은 인용 정확도 0 으로 검출된다.
