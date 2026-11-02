# AI07-015 빈 입력

| 항목 | 내용 |
| --- | --- |
| TC ID | AI07-015 |
| 분야 | AI07_폐업ML추론 |
| 세부 기능 | RandomForest 폐업률 예측 |
| 원자 검증 항목 | 빈 입력 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/ml_model.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/ml_model.py |

## 검증 목적

RandomForest 폐업률 예측에서 '빈 입력' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

RandomForest 폐업률 예측 모듈 준비; 입력 사례 '빈 입력'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

0행 프레임

## 실행 절차

1. 0행 프레임 준비
2. RandomForest 폐업률 예측의 '빈 입력' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

안전한 빈 리스트/오류 정책

## 판정 기준

PASS: 안전한 빈 리스트/오류 정책 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 0행 프레임 → ValueError: Found array with 0 sample(s) (shape=(0,)) while a minimum of 1 is required. |
| 결함 ID (Q) | — |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
