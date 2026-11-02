# AI08-009 0 예측

| 항목 | 내용 |
| --- | --- |
| TC ID | AI08-009 |
| 분야 | AI08_매출DL추론 |
| 세부 기능 | PyTorch MLP 매출 예측 |
| 원자 검증 항목 | 0 예측 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/dl_model.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/dl_model.py |

## 검증 목적

PyTorch MLP 매출 예측에서 '0 예측' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

PyTorch MLP 매출 예측 모듈 준비; 입력 사례 '0 예측'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

output log=0

## 실행 절차

1. output log=0 준비
2. PyTorch MLP 매출 예측의 '0 예측' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

매출 0만원

## 판정 기준

PASS: 매출 0만원 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 영 로그 복원 output log=0 → [0.0] |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
