# AI07-009 범주 미등록

| 항목 | 내용 |
| --- | --- |
| TC ID | AI07-009 |
| 분야 | AI07_폐업ML추론 |
| 세부 기능 | RandomForest 폐업률 예측 |
| 원자 검증 항목 | 범주 미등록 |
| 우선순위 | P0 |
| 테스트 구분 | 경계/예외 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/ml_model.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/ml_model.py |

## 검증 목적

RandomForest 폐업률 예측에서 '범주 미등록' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RandomForest 폐업률 예측 모듈 준비; 입력 사례 '범주 미등록'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

신규 industry

## 실행 절차

1. 신규 industry 준비
2. RandomForest 폐업률 예측의 '범주 미등록' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

파이프라인 unknown 처리/실패 정책

## 판정 기준

PASS: 파이프라인 unknown 처리/실패 정책 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 신규 industry 예측=[2.88] handle_unknown='ignore' |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
