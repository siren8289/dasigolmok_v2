# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI07-001 | RandomForest 폐업률 예측 | 모델 첫 로드 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-002 | RandomForest 폐업률 예측 | 모델 캐시 재사용 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-003 | RandomForest 폐업률 예측 | 단일 행 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-004 | RandomForest 폐업률 예측 | 여러 행 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-005 | RandomForest 폐업률 예측 | 소수 둘째자리 반올림 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-006 | RandomForest 폐업률 예측 | 모델 파일 누락 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-008 | RandomForest 폐업률 예측 | 스키마 누락 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-009 | RandomForest 폐업률 예측 | 범주 미등록 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-013 | RandomForest 폐업률 예측 | 불변 입력 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-014 | RandomForest 폐업률 예측 | 모델 순서 정합성 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-015 | RandomForest 폐업률 예측 | 빈 입력 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-016 | RandomForest 폐업률 예측 | 메모리 증폭 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-017 | RandomForest 폐업률 예측 | 동시 추론 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI07-018 | RandomForest 폐업률 예측 | 설명 재현성 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## AI07-001 모델 첫 로드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: joblib.load 호출=1 model=Pipeline path=close_rf.joblib

## AI07-002 모델 캐시 재사용
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 2회 호출 load횟수=1 same=True

## AI07-003 단일 행
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 1행 결과=[2.98] types=['float']

## AI07-004 여러 행
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 일괄과 단건 batch=[2.98, 2.99, 2.99] singles=[2.98, 2.99, 2.99]

## AI07-005 소수 둘째자리 반올림
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 모델출력 4.125 → [4.12] round(4.125,2)=4.12

## AI07-006 모델 파일 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 파일 없음 → FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/qp/wtpnyvgn0kx_759hkfcdztw80000gn/T/pytest-of-jeong-yelim/pytest-3/test_AI07_0060/close_rf.joblib'

## AI07-008 스키마 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: open_rate 누락 → ValueError: columns are missing: {'open_rate'}

## AI07-009 범주 미등록
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 신규 industry 예측=[2.88] handle_unknown='ignore'

## AI07-013 불변 입력
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 예측 후 원본 동일=True columns=['district', 'industry', 'change_code', 'store_count', 'open_rate', 'franchise_ratio', 'foot_traffic', 'operate_months']

## AI07-014 모델 순서 정합성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 5행 batch=[2.98, 2.99, 2.99, 3.03, 3.03] singles=[2.98, 2.99, 2.99, 3.03, 3.03]

## AI07-015 빈 입력
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 0행 프레임 → ValueError: Found array with 0 sample(s) (shape=(0,)) while a minimum of 1 is required.

## AI07-016 메모리 증폭
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 10000행 결과=10000 latency=0.051s peak_memory=3.3MB

## AI07-017 동시 추론
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 순차=[[2.98], [2.99], [2.99], [3.03], [3.03], [3.0], [3.04], [3.04], [3.04], [3.04]] 병렬=[[2.98], [2.99], [2.99], [3.03], [3.03], [3.0], [3.04], [3.04], [3.04], [3.04]]

## AI07-018 설명 재현성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 1회=[3.04] 2회=[3.04]
