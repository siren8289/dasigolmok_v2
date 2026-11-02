# RG04-012 종료 정책 포함

| 항목 | 내용 |
| --- | --- |
| TC ID | RG04-012 |
| 분야 | RG04_지원정책규칙 |
| 세부 기능 | 지원정책 기간·적합성 |
| 원자 검증 항목 | 종료 정책 포함 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/support_policy/service.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/support_policy/service.py |

## 검증 목적

지원정책 기간·적합성에서 '종료 정책 포함' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

지원정책 기간·적합성 모듈 준비; 입력 사례 '종료 정책 포함'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

only_open=False,target=2026-11-02

## 실행 절차

1. only_open=False,target=2026-11-02 준비
2. 지원정책 기간·적합성의 '종료 정책 포함' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

마감 상태 표기한 조회 허용

## 판정 기준

PASS: 마감 상태 표기한 조회 허용 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | only_open=False 는 마감 상태를 표기한 채 종료 공고를 포함한다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
