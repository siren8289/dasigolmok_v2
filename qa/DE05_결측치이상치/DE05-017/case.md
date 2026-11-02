# DE05-017 outlier 결과 빈 그룹

| 항목 | 내용 |
| --- | --- |
| TC ID | DE05-017 |
| 분야 | DE05_결측치이상치 |
| 세부 기능 | 중앙값 결측·이상치 1% |
| 원자 검증 항목 | outlier 결과 빈 그룹 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | pytest/fixture + CSV검증 |
| 관련 코드 경로 | `data/etl/transform.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/data/etl/transform.py |

## 검증 목적

중앙값 결측·이상치 1%에서 'outlier 결과 빈 그룹' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

중앙값 결측·이상치 1% 모듈 준비; 입력 사례 'outlier 결과 빈 그룹'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

전부 제거되는 극단값 집합

## 실행 절차

1. 전부 제거되는 극단값 집합 준비
2. 중앙값 결측·이상치 1%의 'outlier 결과 빈 그룹' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

pd.concat(empty) 예외 방어

## 판정 기준

PASS: pd.concat(empty) 예외 방어 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | industry=None 2행 remove_outliers가 ValueError 'No objects to concatenate'. 빈 그룹 방어가 없음. |
| 결함 ID (Q) | DEF-DE05-017 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
