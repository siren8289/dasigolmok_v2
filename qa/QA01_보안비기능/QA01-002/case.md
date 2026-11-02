# QA01-002 XSS React 렌더링

| 항목 | 내용 |
| --- | --- |
| TC ID | QA01-002 |
| 분야 | QA01_보안비기능 |
| 세부 기능 | 보안·성능·사용자 품질 |
| 원자 검증 항목 | XSS React 렌더링 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Vitest/Playwright + 네트워크 검증 |
| 관련 코드 경로 | `front/src/api/api.ts` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/front/src/api/api.ts |

## 검증 목적

보안·성능·사용자 품질에서 'XSS React 렌더링' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

보안·성능·사용자 품질 모듈 준비; 입력 사례 'XSS React 렌더링'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

explanation='<img onerror=alert(1)>'

## 실행 절차

1. explanation='<img onerror=alert(1)>' 준비
2. 보안·성능·사용자 품질의 'XSS React 렌더링' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

스크립트 실행 안 됨

## 판정 기준

PASS: 스크립트 실행 안 됨 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | vitest FE03-023 통과. explanation의 img/script 문자열이 텍스트로만 보이고 script·img 요소는 생기지 않는다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
