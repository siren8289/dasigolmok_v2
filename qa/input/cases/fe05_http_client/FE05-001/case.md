# FE05-001 baseURL 기본값

| 항목 | 내용 |
| --- | --- |
| TC ID | FE05-001 |
| 분야 | FE05_HTTP클라이언트 |
| 세부 기능 | 프론트 fetch API 계약 |
| 원자 검증 항목 | baseURL 기본값 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Vitest/Playwright + 네트워크 검증 |
| 관련 코드 경로 | `front/src/api/api.ts` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/front/src/api/api.ts |

## 검증 목적

프론트 fetch API 계약에서 'baseURL 기본값' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

프론트 fetch API 계약 모듈 준비; 입력 사례 'baseURL 기본값'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

VITE_API_URL 미설정

## 실행 절차

1. VITE_API_URL 미설정 준비
2. 프론트 fetch API 계약의 'baseURL 기본값' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

http://localhost:8080 사용

## 판정 기준

PASS: http://localhost:8080 사용 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | VITE_API_URL 미설정 시 fetch URL이 http://localhost:8080/api/options 이다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
