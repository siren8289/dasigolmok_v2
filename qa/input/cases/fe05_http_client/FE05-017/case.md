# FE05-017 민감정보 에러 반사

| 항목 | 내용 |
| --- | --- |
| TC ID | FE05-017 |
| 분야 | FE05_HTTP클라이언트 |
| 세부 기능 | 프론트 fetch API 계약 |
| 원자 검증 항목 | 민감정보 에러 반사 |
| 우선순위 | P0 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Vitest/Playwright + 네트워크 검증 |
| 관련 코드 경로 | `front/src/api/api.ts` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/front/src/api/api.ts |

## 검증 목적

프론트 fetch API 계약에서 '민감정보 에러 반사' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

프론트 fetch API 계약 모듈 준비; 입력 사례 '민감정보 에러 반사'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

오류 message에 토큰 값

## 실행 절차

1. 오류 message에 토큰 값 준비
2. 프론트 fetch API 계약의 '민감정보 에러 반사' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

사용자 노출 전 민감정보 제거

## 판정 기준

PASS: 사용자 노출 전 민감정보 제거 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | 실제 메시지에 토큰이 남아 있다: token=SECRET-TOKEN-123 failed: expected 'token=SECRET-TOKEN-123 failed' not to contain 'SECRET-TOKEN-123' |
| 결함 ID (Q) | DEF-FE05-017 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
