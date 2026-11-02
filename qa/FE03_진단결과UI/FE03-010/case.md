# FE03-010 모르는 상태

| 항목 | 내용 |
| --- | --- |
| TC ID | FE03-010 |
| 분야 | FE03_진단결과UI |
| 세부 기능 | 진단 결과 렌더링 |
| 원자 검증 항목 | 모르는 상태 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Vitest/Playwright + 네트워크 검증 |
| 관련 코드 경로 | `front/src/pages/ResultPage.tsx` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/front/src/pages/ResultPage.tsx |

## 검증 목적

진단 결과 렌더링에서 '모르는 상태' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

진단 결과 렌더링 모듈 준비; 입력 사례 '모르는 상태'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

status=weird

## 실행 절차

1. status=weird 준비
2. 진단 결과 렌더링의 '모르는 상태' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

unknown fallback 스타일

## 판정 기준

PASS: unknown fallback 스타일 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 알 수 없는 status=weird 는 unknown 스타일·판단 불가로 떨어진다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
