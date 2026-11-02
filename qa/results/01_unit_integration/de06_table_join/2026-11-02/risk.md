# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE06-001 | 4종 표 join·파생 변수 | 점포-매출 키 결합 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-002 | 4종 표 join·파생 변수 | 점포-인구 키 결합 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-003 | 4종 표 join·파생 변수 | 점포-변화 키 결합 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-005 | 4종 표 join·파생 변수 | 매출 결측 대체 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-006 | 4종 표 join·파생 변수 | 유동인구 결측 대체 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-007 | 4종 표 join·파생 변수 | 운영개월 결측 대체 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-008 | 4종 표 join·파생 변수 | 변화코드 결측 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-009 | 4종 표 join·파생 변수 | 변화명 결측 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-010 | 4종 표 join·파생 변수 | 점포당 매출 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-012 | 4종 표 join·파생 변수 | 점포 3개 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-013 | 4종 표 join·파생 변수 | 동일 동 다른 업종 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-014 | 4종 표 join·파생 변수 | 동일 업종 다른 동 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-015 | 4종 표 join·파생 변수 | 분기 다름 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-017 | 4종 표 join·파생 변수 | 매출 0원 대체 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-018 | 4종 표 join·파생 변수 | 최근 분기 선택 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-019 | 4종 표 join·파생 변수 | 동 중앙값 폐업률 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-020 | 4종 표 join·파생 변수 | 동 중앙값 매출 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-022 | 4종 표 join·파생 변수 | 상권변화 코드 공통 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE06-023 | 4종 표 join·파생 변수 | 전처리 통계 결과 수 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |

## DE06-001 점포-매출 키 결합
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 키 일치 시 sales_amount 1000이 점포 1행에 병합.

## DE06-002 점포-인구 키 결합
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: quarter·dong_code 일치 시 foot_traffic 80000이 병합.

## DE06-003 점포-변화 키 결합
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_code LH, change_name 상권확장, operate_months 12가 병합.

## DE06-005 매출 결측 대체
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한식 매출 100과 결측 1건. 결측 동 성산동의 sales_amount는 중앙값 100.

## DE06-006 유동인구 결측 대체
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 유동인구 500이 있는 동과 없는 동. 결측 동 foot_traffic은 중앙값 500.

## DE06-007 운영개월 결측 대체
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: operate_months 15가 있는 동 기준. 결측 동은 15로 채워짐.

## DE06-008 변화코드 결측
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 변화지표가 없으면 change_code는 HH. 결과 1행.

## DE06-009 변화명 결측
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_code HH이고 change_name이 비면 정체.

## DE06-010 점포당 매출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: sales_amount 1000, store_count 10 → sales_per_store 100.

## DE06-012 점포 3개
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: store_count=3은 최소 조건 통과. 결과 1행.

## DE06-013 동일 동 다른 업종
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 동 CS100001의 sales_count는 11, CS100010은 22. 업종이 섞이지 않음.

## DE06-014 동일 업종 다른 동
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 11440740 sales_count 111, 11680640은 222이고 foot_traffic 90000. 동이 섞이지 않음.

## DE06-015 분기 다름
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 20241 sales_count 111, 20242는 222. 분기가 섞이지 않음.

## DE06-017 매출 0원 대체
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 매출 0원 행은 제외되고 10000원(1만원)인 11680640 1행만 남음.

## DE06-018 최근 분기 선택
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: quarter 20241과 20242 중 dong_stats는 20242 1행.

## DE06-019 동 중앙값 폐업률
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 동 close_rate 2,4,6의 median_close_rate는 4.0.

## DE06-020 동 중앙값 매출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 같은 동 sales_per_store 100,300의 median은 200.

## DE06-022 상권변화 코드 공통
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_code HL은 원본명과 관계없이 change_name 상권축소.

## DE06-023 전처리 통계 결과 수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 3업종×2분기(20241,20242)의 dong_stats는 최신 20242 3행.
