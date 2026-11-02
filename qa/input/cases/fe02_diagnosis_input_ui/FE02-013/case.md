# FE02-013 분석 버튼

| 항목 | 내용 |
| --- | --- |
| TC ID | FE02-013 |
| 분야 | FE02_진단입력UI |
| 세부 기능 | 진단 페이지 입력·셀렉트 |
| 원자 검증 항목 | 분석 버튼 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Vitest/Playwright + 네트워크 검증 |
| 관련 코드 경로 | `front/src/pages/DiagnosePage.tsx` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/front/src/pages/DiagnosePage.tsx |

## 검증 목적

진단 페이지 입력·셀렉트에서 '분석 버튼' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

진단 페이지 입력·셀렉트 모듈 준비; 입력 사례 '분석 버튼'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

유효한 3개 값

## 실행 절차

1. 유효한 3개 값 준비
2. 진단 페이지 입력·셀렉트의 '분석 버튼' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

POST /api/diagnoses로 세 필드 전송

## 판정 기준

PASS: POST /api/diagnoses로 세 필드 전송 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | POST /api/diagnoses body에 district, dong, industry 세 필드가 실렸다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
