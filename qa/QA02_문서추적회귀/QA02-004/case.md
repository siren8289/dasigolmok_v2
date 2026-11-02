# QA02-004 현재 API 표

| 항목 | 내용 |
| --- | --- |
| TC ID | QA02-004 |
| 분야 | QA02_문서추적회귀 |
| 세부 기능 | 문서·구현 일치성·테스트 회귀 |
| 원자 검증 항목 | 현재 API 표 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `README.md` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/README.md |

## 검증 목적

문서·구현 일치성·테스트 회귀에서 '현재 API 표' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

문서·구현 일치성·테스트 회귀 모듈 준비; 입력 사례 '현재 API 표'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

Readme.md

## 실행 절차

1. Readme.md 준비
2. 문서·구현 일치성·테스트 회귀의 '현재 API 표' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

GET options,POST diagnose,POST recommend로 동기화

## 판정 기준

PASS: GET options,POST diagnose,POST recommend로 동기화 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | README에 GET /api/options, POST /api/diagnoses, POST /api/recommendations 표가 없다. 코드 컨트롤러에는 있다. |
| 결함 ID (Q) | DEF-QA02-004 |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
