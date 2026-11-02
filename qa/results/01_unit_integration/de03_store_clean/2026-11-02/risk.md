# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE03-001 | 점포 통계 clean_store | 공통 key 추출 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-002 | 점포 통계 clean_store | 서울 자치구 매핑 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-003 | 점포 통계 clean_store | 타 지역 코드 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-004 | 점포 통계 clean_store | 점포수 >0 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-005 | 점포 통계 clean_store | 점포수 0 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-006 | 점포 통계 clean_store | 점포수 음수 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-007 | 점포 통계 clean_store | 점포수 문자열 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-008 | 점포 통계 clean_store | 폐업률 문자열 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-009 | 점포 통계 clean_store | 개업률 문자열 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-010 | 점포 통계 clean_store | 프랜차이즈 비율 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-011 | 점포 통계 clean_store | 프랜차이즈 비율 >1 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-012 | 점포 통계 clean_store | 프랜차이즈 음수 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-014 | 점포 통계 clean_store | 동일 복제 행 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-015 | 점포 통계 clean_store | 다른 분기 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE03-016 | 점포 통계 clean_store | 업종 코드 다름 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |

## DE03-001 공통 key 추출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 공통 키가 quarter=20242, dong_code=11440740, industry_code=CS100001.

## DE03-002 서울 자치구 매핑
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 행정동 코드 11440100의 district는 마포구. 결과 1행.

## DE03-003 타 지역 코드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 코드 26110510은 district가 빈 문자열이라 결과 0행.

## DE03-004 점포수 >0
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: store_count=1은 포함. 결과 1행, 값 1.

## DE03-005 점포수 0
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: store_count=0은 제외. 결과 0행.

## DE03-006 점포수 음수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: store_count=-1은 제외. 결과 0행.

## DE03-007 점포수 문자열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 점포수 문자열 '1,000'은 1000. 결과 1행.

## DE03-008 폐업률 문자열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 폐업률 '5.25'는 float 5.25.

## DE03-009 개업률 문자열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 개업률 '3.20'은 float 3.20.

## DE03-010 프랜차이즈 비율
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 프랜차이즈 2, 점포 10 → franchise_ratio 0.2.

## DE03-011 프랜차이즈 비율 >1
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 프랜차이즈 12, 점포 10 → franchise_ratio 1로 클리핑.

## DE03-012 프랜차이즈 음수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 프랜차이즈 -1, 점포 10 → franchise_ratio 0으로 클리핑.

## DE03-014 동일 복제 행
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 quarter/dong_code/industry_code 2행이 1행으로 축소.

## DE03-015 다른 분기
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 분기 20241과 20242는 둘 다 유지. 결과 2행.

## DE03-016 업종 코드 다름
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 업종 CS100001과 CS100010이 각각 유지. 결과 2행.
