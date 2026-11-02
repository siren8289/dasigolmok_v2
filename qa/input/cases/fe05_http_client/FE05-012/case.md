# FE05-012 422 detail 대체

| 항목 | 내용 |
| --- | --- |
| TC ID | FE05-012 |
| 분야 | FE05_HTTP클라이언트 |
| 세부 기능 | 프론트 fetch API 계약 |
| 원자 검증 항목 | 422 detail 대체 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Vitest/Playwright + 네트워크 검증 |
| 관련 코드 경로 | `front/src/api/api.ts` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/front/src/api/api.ts |

## 검증 목적

프론트 fetch API 계약에서 '422 detail 대체' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

프론트 fetch API 계약 모듈 준비; 입력 사례 '422 detail 대체'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

{detail:'검증 실패'}

## 실행 절차

1. {detail:'검증 실패'} 준비
2. 프론트 fetch API 계약의 '422 detail 대체' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

detail로 대체

## 판정 기준

PASS: detail로 대체 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | message가 없으면 detail '검증 실패'를 쓴다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
