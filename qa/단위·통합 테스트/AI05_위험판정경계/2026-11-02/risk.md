# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI05-001 | classify 규칙·경계 | 폐업률 3.99% HH | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-002 | classify 규칙·경계 | 폐업률 4.00% HH | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-003 | classify 규칙·경계 | 폐업률 4.01% HH | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-004 | classify 규칙·경계 | 폐업률 7.99% HH | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-005 | classify 규칙·경계 | 폐업률 8.00% HH | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-006 | classify 규칙·경계 | 폐업률 8.01% HH | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-007 | classify 규칙·경계 | 폐업률 0% HH | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-008 | classify 규칙·경계 | 폐업률 2% HL | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-009 | classify 규칙·경계 | 폐업률 4% HL | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-010 | classify 규칙·경계 | 폐업률 9% HL | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-011 | classify 규칙·경계 | 폐업률 2% LL | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-012 | classify 규칙·경계 | 폐업률 8% LL | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-013 | classify 규칙·경계 | 폐업률 2% LH | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-014 | classify 규칙·경계 | 폐업률 8% LH | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-015 | classify 규칙·경계 | 폐업률 None | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-016 | classify 규칙·경계 | 변화코드 기타 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-019 | classify 규칙·경계 | 문자열 폐업률 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-021 | classify 규칙·경계 | 정수 4 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-022 | classify 규칙·경계 | 실수 정밀도 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI05-023 | classify 규칙·경계 | 예상 폐업률 사용 여부 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## AI05-001 폐업률 3.99% HH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(3.99,'HH')=('stable', False) 기대=('stable',False)

## AI05-002 폐업률 4.00% HH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(4.0,'HH')=('warning', False) 기대=('warning',False)

## AI05-003 폐업률 4.01% HH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(4.01,'HH')=('warning', False) 기대=('warning',False)

## AI05-004 폐업률 7.99% HH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(7.99,'HH')=('warning', False) 기대=('warning',False)

## AI05-005 폐업률 8.00% HH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(8.0,'HH')=('danger', True) 기대=('danger',True)

## AI05-006 폐업률 8.01% HH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(8.01,'HH')=('danger', True) 기대=('danger',True)

## AI05-007 폐업률 0% HH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(0,'HH')=('stable', False) 기대=('stable',False)

## AI05-008 폐업률 2% HL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(2,'HL')=('danger', True) 기대=('danger',True)

## AI05-009 폐업률 4% HL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(4,'HL')=('danger', True) 기대=('danger',True)

## AI05-010 폐업률 9% HL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(9,'HL')=('danger', True) 기대=('danger',True)

## AI05-011 폐업률 2% LL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(2,'LL')=('warning', False) 기대=('warning',False)

## AI05-012 폐업률 8% LL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(8,'LL')=('danger', True) 기대=('danger',True)

## AI05-013 폐업률 2% LH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(2,'LH')=('stable', False) 기대=('stable',False)

## AI05-014 폐업률 8% LH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(8,'LH')=('danger', True) 기대=('danger',True)

## AI05-015 폐업률 None
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(None,'HL')=('unknown', False) 기대=('unknown',False)

## AI05-016 변화코드 기타
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(2,'XX')=('stable', False) 기대=('stable',False)

## AI05-019 문자열 폐업률
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 문자열 폐업률 classify('5','HH')="TypeError: '>=' not supported between instances of 'str' and 'int'"

## AI05-021 정수 4
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(4,'HH')=('warning', False) 기대=('warning',False)

## AI05-022 실수 정밀도
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: classify(3.999999,'HH')=('stable', False) 기대=('stable',False)

## AI05-023 예상 폐업률 사용 여부
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 진단 status=stable close_rate=2 ml=10 / 추천 status=danger close_rate=2 ml=10
