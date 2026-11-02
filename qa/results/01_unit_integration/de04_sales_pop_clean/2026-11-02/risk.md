# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE04-001 | 매출·유동인구 정제 | 매출 원→만원 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-002 | 매출·유동인구 정제 | 매출 1원 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-003 | 매출·유동인구 정제 | 매출 0원 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-004 | 매출·유동인구 정제 | 매출 음수 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-005 | 매출·유동인구 정제 | 매출 null | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-006 | 매출·유동인구 정제 | 매출 1,000 문자열 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-007 | 매출·유동인구 정제 | 매출 건수 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-008 | 매출·유동인구 정제 | 타지역 매출 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-009 | 매출·유동인구 정제 | 매출 중복 분기 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-010 | 매출·유동인구 정제 | 유동인구 양수 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-011 | 매출·유동인구 정제 | 유동인구 0 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-012 | 매출·유동인구 정제 | 유동인구 음수 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-013 | 매출·유동인구 정제 | 유동인구 문자열 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-014 | 매출·유동인구 정제 | 유동인구 동일 동/분기 중복 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-015 | 매출·유동인구 정제 | 변화코드 HH | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-016 | 매출·유동인구 정제 | 변화코드 HL | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-017 | 매출·유동인구 정제 | 변화코드 LH | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-018 | 매출·유동인구 정제 | 변화코드 LL | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-019 | 매출·유동인구 정제 | 모르는 변화코드 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-020 | 매출·유동인구 정제 | 운영 개월 문자열 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-021 | 매출·유동인구 정제 | 서울 외 변화지표 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE04-022 | 매출·유동인구 정제 | CSV 스키마 누락 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |

## DE04-001 매출 원→만원
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 매출 10000000원은 1000만원(sales_amount=1000).

## DE04-002 매출 1원
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 매출 1원은 0.0001만원.

## DE04-003 매출 0원
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 매출 0원은 필터 제외. 결과 0행.

## DE04-004 매출 음수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 매출 -100원은 필터 제외. 결과 0행.

## DE04-005 매출 null
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 매출 None은 필터 제외. 결과 0행.

## DE04-006 매출 1,000 문자열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 매출 문자열 '1,000'은 0.1만원.

## DE04-007 매출 건수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: sales_count '3,000'은 3000.

## DE04-008 타지역 매출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 행정동 26110510(district 빈 값) 매출은 0행.

## DE04-009 매출 중복 분기
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 quarter/dong/업종 매출 2행이 1행.

## DE04-010 유동인구 양수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: foot_traffic=100은 포함. 결과 1행.

## DE04-011 유동인구 0
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: foot_traffic=0은 제외. 결과 0행.

## DE04-012 유동인구 음수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: foot_traffic=-1은 제외. 결과 0행.

## DE04-013 유동인구 문자열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 유동인구 '50,000'은 50000.

## DE04-014 유동인구 동일 동/분기 중복
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 동/분기 유동인구 2행이 1행.

## DE04-015 변화코드 HH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_code HH의 change_name은 정체.

## DE04-016 변화코드 HL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_code HL의 change_name은 상권축소.

## DE04-017 변화코드 LH
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_code LH의 change_name은 상권확장.

## DE04-018 변화코드 LL
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_code LL의 change_name은 다이나믹.

## DE04-019 모르는 변화코드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_code XX는 코드표에 없고 change_name은 원본변화명.

## DE04-020 운영 개월 문자열
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 운영 개월 '15.5'는 15.5.

## DE04-021 서울 외 변화지표
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 타시도 코드 26110510 변화지표는 0행.

## DE04-022 CSV 스키마 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 총_유동인구_수 컬럼이 없으면 KeyError. 메시지에 총_유동인구_수가 있음.
