# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI06-001 | ML·DL 피처 공통 | district 문자 피처 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-002 | ML·DL 피처 공통 | industry 문자 피처 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-003 | ML·DL 피처 공통 | change_code 문자 피처 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-004 | ML·DL 피처 공통 | store_count 수치 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-005 | ML·DL 피처 공통 | open_rate 수치 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-006 | ML·DL 피처 공통 | franchise_ratio 수치 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-007 | ML·DL 피처 공통 | foot_traffic 수치 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-008 | ML·DL 피처 공통 | operate_months 수치 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-009 | ML·DL 피처 공통 | 열 목록 순서 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-010 | ML·DL 피처 공통 | 예측 종속값 누출 방지 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-011 | ML·DL 피처 공통 | 단일 입력 행수 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-012 | ML·DL 피처 공통 | 피처 열 개수 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-014 | ML·DL 피처 공통 | unknown category | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-015 | ML·DL 피처 공통 | NaN 유동인구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-017 | ML·DL 피처 공통 | 범주 순서 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI06-018 | ML·DL 피처 공통 | 숫자 정밀도 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## AI06-001 district 문자 피처
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: columns=['district', 'industry', 'change_code', 'store_count', 'open_rate', 'franchise_ratio', 'foot_traffic', 'operate_months'] district='마포구' dtype=object

## AI06-002 industry 문자 피처
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industry='한식음식점'

## AI06-003 change_code 문자 피처
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 변화코드 change_code='HL'

## AI06-004 store_count 수치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 점포수 store_count=np.int64(13)

## AI06-005 open_rate 수치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 개업률 open_rate=np.float64(1.1)

## AI06-006 franchise_ratio 수치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 가맹비율 franchise_ratio=np.float64(0.33)

## AI06-007 foot_traffic 수치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 유동인구 foot_traffic=np.int64(50000)

## AI06-008 operate_months 수치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 운영개월 operate_months=np.int64(18)

## AI06-009 열 목록 순서
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 특성 순서 FEATURE=['district', 'industry', 'change_code', 'store_count', 'open_rate', 'franchise_ratio', 'foot_traffic', 'operate_months'] CATEGORY+NUMBER=['district', 'industry', 'change_code', 'store_count', 'open_rate', 'franchise_ratio', 'foot_traffic', 'operate_months']

## AI06-010 예측 종속값 누출 방지
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: columns=['district', 'industry', 'change_code', 'store_count', 'open_rate', 'franchise_ratio', 'foot_traffic', 'operate_months'] ML_TARGET/DL_TARGET 포함여부 close_rate=False sales=False

## AI06-011 단일 입력 행수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 단일 행 shape=(1, 8)

## AI06-012 피처 열 개수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 열 구성 shape=(1, 8) columns=['district', 'industry', 'change_code', 'store_count', 'open_rate', 'franchise_ratio', 'foot_traffic', 'operate_months']

## AI06-014 unknown category
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 미등록 업종 industry=UNKNOWN → pred=[3.07] handle_unknown='ignore'

## AI06-015 NaN 유동인구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 결측 유동인구 foot_traffic=NaN frame=np.float64(nan) → ValueError: Input X contains NaN. RandomForestRegressor does not accept missing values encoded as NaN natively. For supervised learning, you might want to consider sklearn.ensemble.HistGradientBoostingClassifier and Regr

## AI06-017 범주 순서
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 행 결합 rows=100 columns=['district', 'industry', 'change_code', 'store_count', 'open_rate', 'franchise_ratio', 'foot_traffic', 'operate_months']

## AI06-018 숫자 정밀도
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: store_count=1e9 저장값=np.int64(1000000000) dtype=int64
