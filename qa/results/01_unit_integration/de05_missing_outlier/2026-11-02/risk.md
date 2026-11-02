# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE05-001 | 중앙값 결측·이상치 1% | 소수 쉼표 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-002 | 중앙값 결측·이상치 1% | 빈 문자열 숫자 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-003 | 중앙값 결측·이상치 1% | 잘못된 문자열 숫자 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-004 | 중앙값 결측·이상치 1% | 전체 중앙값 대체 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-005 | 중앙값 결측·이상치 1% | 업종 중앙값 대체 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-006 | 중앙값 결측·이상치 1% | 업종 외 값 유지 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-008 | 중앙값 결측·이상치 1% | 업종 하나만 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-009 | 중앙값 결측·이상치 1% | 업종 100행 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-010 | 중앙값 결측·이상치 1% | 상위 극단값 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-011 | 중앙값 결측·이상치 1% | 하위 극단값 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-012 | 중앙값 결측·이상치 1% | 중앙값 일관성 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-014 | 중앙값 결측·이상치 1% | 업종별 독립 제거 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-015 | 중앙값 결측·이상치 1% | 결측 열 이름 오타 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-018 | 중앙값 결측·이상치 1% | 상하위 같은 값 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE05-019 | 중앙값 결측·이상치 1% | NaN quantile | pytest | PASS | fixture | NOT_RUN | NOT_RUN |

## DE05-001 소수 쉼표
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: to_number('1,234.5')=1234.5.

## DE05-002 빈 문자열 숫자
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: to_number('')는 NaN.

## DE05-003 잘못된 문자열 숫자
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: to_number('오류')는 NaN.

## DE05-004 전체 중앙값 대체
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한식 값이 모두 NaN, 카페가 10과 30이면 한식 2행이 전체 median 20.0.

## DE05-005 업종 중앙값 대체
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 업종 [1, NaN, 3]의 결측이 중앙값 2로 채워져 [1,2,3].

## DE05-006 업종 외 값 유지
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 이미 있는 값 50은 50으로 유지.

## DE05-008 업종 하나만
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 업종 1행 값 42는 이상치 제거 후에도 1행.

## DE05-009 업종 100행
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 0부터 99까지 100행. 1% 경계 밖인 0과 99가 제거되고 나머지 98행은 경계 안.

## DE05-010 상위 극단값
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 1..100에 10000000을 더한 집합에서 10000000은 제거되고 50은 남음.

## DE05-011 하위 극단값
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: -100과 1..100에서 -100은 제거되고 50은 남음.

## DE05-012 중앙값 일관성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: [1,2,3,4]와 결측 1개의 채움값은 중앙값 2.5.

## DE05-014 업종별 독립 제거
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한식 99개가 10이고 1000 1개는 제거. 카페 1000은 100건 모두 유지.

## DE05-015 결측 열 이름 오타
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 없는 열 no_such는 KeyError. 메시지에 no_such가 있음.

## DE05-018 상하위 같은 값
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 값이 모두 5인 5행은 한 행도 빠지지 않음.

## DE05-019 NaN quantile
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 대상 열 2행이 모두 NaN이면 예외 없이 0행으로 정리됨.
