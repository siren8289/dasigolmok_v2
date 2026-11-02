# AI07-013 불변 입력

| 항목 | 내용 |
| --- | --- |
| TC ID | AI07-013 |
| 분야 | AI07_폐업ML추론 |
| 세부 기능 | RandomForest 폐업률 예측 |
| 원자 검증 항목 | 불변 입력 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/ml_model.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/ml_model.py |

## 검증 목적

RandomForest 폐업률 예측에서 '불변 입력' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RandomForest 폐업률 예측 모듈 준비; 입력 사례 '불변 입력'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

predict 반복

## 실행 절차

1. predict 반복 준비
2. RandomForest 폐업률 예측의 '불변 입력' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

입력 DataFrame 원본 불변

## 판정 기준

PASS: 입력 DataFrame 원본 불변 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 예측 후 원본 동일=True columns=['district', 'industry', 'change_code', 'store_count', 'open_rate', 'franchise_ratio', 'foot_traffic', 'operate_months'] |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
