# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI03-001 | 상권 진단 오케스트레이션 | 정상 조회 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-002 | 상권 진단 오케스트레이션 | 없는 업종 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-003 | 상권 진단 오케스트레이션 | 없는 동 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-005 | 상권 진단 오케스트레이션 | 특성 추출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-006 | 상권 진단 오케스트레이션 | ML 모델 호출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-007 | 상권 진단 오케스트레이션 | DL 모델 호출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-008 | 상권 진단 오케스트레이션 | 실제 폐업률 상태판정 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-009 | 상권 진단 오케스트레이션 | 예측 폐업률과 상태 분리 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-010 | 상권 진단 오케스트레이션 | 상권변화 HL 우선 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-011 | 상권 진단 오케스트레이션 | 분기 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-012 | 상권 진단 오케스트레이션 | 점포 수 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-013 | 상권 진단 오케스트레이션 | 개업률 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-014 | 상권 진단 오케스트레이션 | 폐업률 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-015 | 상권 진단 오케스트레이션 | 유동인구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-016 | 상권 진단 오케스트레이션 | 상권변화명 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-017 | 상권 진단 오케스트레이션 | 프랜차이즈 비중 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-018 | 상권 진단 오케스트레이션 | 영업 개월 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-019 | 상권 진단 오케스트레이션 | 점포당 매출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-020 | 상권 진단 오케스트레이션 | LLM 설명 호출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-021 | 상권 진단 오케스트레이션 | 설명에서 수치 확인 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI03-025 | 상권 진단 오케스트레이션 | 중복 호출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## AI03-001 정상 조회
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 매칭행=1 error=None close_rate=3 store=183 quarter=20254

## AI03-002 없는 업종
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 없는 업종 결과={'error': '해당 행정동·업종 데이터가 없습니다.'}

## AI03-003 없는 동
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 없는 동 결과={'error': '해당 행정동·업종 데이터가 없습니다.'}

## AI03-005 특성 추출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 입력 열 columns=['district', 'industry', 'change_code', 'store_count', 'open_rate', 'franchise_ratio', 'foot_traffic', 'operate_months'] shape=(1, 8) store_count=10

## AI03-006 ML 모델 호출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 예측 폐업률 ml_close_rate=3.33

## AI03-007 DL 모델 호출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 예측 매출 dl_sales_per_store=450.0

## AI03-008 실제 폐업률 상태판정
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 고폐업 판정 close_rate=9.2 status=danger is_danger=True

## AI03-009 예측 폐업률과 상태 분리
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 실제 close_rate=2 ml=9 status=stable

## AI03-010 상권변화 HL 우선
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 상권축소 판정 close_rate=1 change=HL status=danger is_danger=True

## AI03-011 분기
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: quarter 입력=20244 출력=20244

## AI03-012 점포 수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 점포수 store_count=12

## AI03-013 개업률
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 개업률 open_rate=2.2

## AI03-014 폐업률
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 폐업률 close_rate=3.2

## AI03-015 유동인구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 유동인구 foot_traffic=35000

## AI03-016 상권변화명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_name=상권축소

## AI03-017 프랜차이즈 비중
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 가맹비율 franchise_ratio=0.15

## AI03-018 영업 개월
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 운영개월 operate_months=50

## AI03-019 점포당 매출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 점포당매출 sales_per_store=700

## AI03-020 LLM 설명 호출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 설명 출처 explanation='text' source='basic'

## AI03-021 설명에서 수치 확인
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: explanation=연남동 한식음식점 상권은 '주의' 단계입니다. 최근 폐업률은 6%이고, AI가 예상한 폐업률은 7%입니다. 점포당 예상 매출은 약 100만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI03-025 중복 호출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 동일호출=True 원본불변=True status=stable ml=2.5
