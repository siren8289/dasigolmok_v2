# RG04-001 모집 시작 전

| 항목 | 내용 |
| --- | --- |
| TC ID | RG04-001 |
| 분야 | RG04_지원정책규칙 |
| 세부 기능 | 지원정책 기간·적합성 |
| 원자 검증 항목 | 모집 시작 전 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/support_policy/service.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/support_policy/service.py |

## 검증 목적

지원정책 기간·적합성에서 '모집 시작 전' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

지원정책 기간·적합성 모듈 준비; 입력 사례 '모집 시작 전'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

start=2026-11-10,end=2026-12-01,target=2026-11-02

## 실행 절차

1. start=2026-11-10,end=2026-12-01,target=2026-11-02 준비
2. 지원정책 기간·적합성의 '모집 시작 전' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

upcoming,false

## 판정 기준

PASS: upcoming,false 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 기준일 2026-11-02, 시작 2026-12-01 은 upcoming, false 이다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
