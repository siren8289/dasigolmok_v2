# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE07-001 | 선택 목록 옵션 생성 | 자치구 알파벳순 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-002 | 선택 목록 옵션 생성 | 동 지역순 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-003 | 선택 목록 옵션 생성 | 동 중복 제거 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-004 | 선택 목록 옵션 생성 | 업종 정렬 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-005 | 선택 목록 옵션 생성 | 업종 중복 제거 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-006 | 선택 목록 옵션 생성 | 업종 코드 다름 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-007 | 선택 목록 옵션 생성 | 지역 옵션 메타 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-008 | 선택 목록 옵션 생성 | SEMAS 자치구 카운트 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-009 | 선택 목록 옵션 생성 | SEMAS 업종 카운트 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-010 | 선택 목록 옵션 생성 | SEMAS 누락 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-011 | 선택 목록 옵션 생성 | 빈 데이터 train | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-012 | 선택 목록 옵션 생성 | train district null | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-013 | 선택 목록 옵션 생성 | 동 코드 앞자리 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-015 | 선택 목록 옵션 생성 | 옵션과 통계 일치 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE07-016 | 선택 목록 옵션 생성 | 구 바꾸면 다른 구 동 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |

## DE07-001 자치구 알파벳순
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 25개 자치구 districts가 sorted 결과와 같고 길이는 25.

## DE07-002 동 지역순
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 강남구·마포구 4동의 (district,dong) 순서가 정렬 결과와 같음.

## DE07-003 동 중복 제거
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 district/dong/dong_code 2행의 dongs는 1건.

## DE07-004 업종 정렬
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한식·커피·분식 industries가 industry 기준 sorted와 같음.

## DE07-005 업종 중복 제거
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 industry+code 2행의 industries는 1건.

## DE07-006 업종 코드 다름
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 이름 한식의 코드 CS100001과 CS100099가 둘 다 포함.

## DE07-007 지역 옵션 메타
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dongs 1건이 district=마포구, dong=연남동, dong_code=11440740.

## DE07-008 SEMAS 자치구 카운트
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: semas 행정동 5건 → semas_dong_count=5.

## DE07-009 SEMAS 업종 카운트
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: semas 업종 10건 → semas_upjong_count=10.

## DE07-010 SEMAS 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dongs=[], upjong=[]이면 두 카운트 모두 0.

## DE07-011 빈 데이터 train
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 컬럼만 있는 빈 train은 districts,dongs,industries가 모두 [].

## DE07-012 train district null
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district None은 districts에서 빠지고 마포구만 남음.

## DE07-013 동 코드 앞자리
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong_code '11680640'이 문자열 길이 8 그대로 보존.

## DE07-015 옵션과 통계 일치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 옵션의 동 2건·업종 2건이 같은 train의 dong_stats 행에 있음.

## DE07-016 구 바꾸면 다른 구 동
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마포구 동은 {연남동,합정동}, 강남구 동은 [역삼1동].
