# FE05-016 API 경로 이중 슬래시

| 항목 | 내용 |
| --- | --- |
| TC ID | FE05-016 |
| 분야 | FE05_HTTP클라이언트 |
| 세부 기능 | 프론트 fetch API 계약 |
| 원자 검증 항목 | API 경로 이중 슬래시 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Vitest/Playwright + 네트워크 검증 |
| 관련 코드 경로 | `front/src/api/api.ts` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/front/src/api/api.ts |

## 검증 목적

프론트 fetch API 계약에서 'API 경로 이중 슬래시' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

프론트 fetch API 계약 모듈 준비; 입력 사례 'API 경로 이중 슬래시'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

baseURL='https://host/'

## 실행 절차

1. baseURL='https://host/' 준비
2. 프론트 fetch API 계약의 'API 경로 이중 슬래시' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

//api 중복 처리 확인

## 판정 기준

PASS: //api 중복 처리 확인 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | 실제 URL https://host//api/options: expected 'https://host//api/options' not to contain '//api' |
| 결함 ID (Q) | DEF-FE05-016 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
