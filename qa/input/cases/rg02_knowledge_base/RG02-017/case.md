# RG02-017 오프라인 임베딩

| 항목 | 내용 |
| --- | --- |
| TC ID | RG02-017 |
| 분야 | RG02_지식베이스 |
| 세부 기능 | 상권 문서 청킹·임베딩 |
| 원자 검증 항목 | 오프라인 임베딩 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/market_knowledge/service.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/market_knowledge/service.py |

## 검증 목적

상권 문서 청킹·임베딩에서 '오프라인 임베딩' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

상권 문서 청킹·임베딩 모듈 준비; 입력 사례 '오프라인 임베딩'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

GEMINI_API_KEY 없음

## 실행 절차

1. GEMINI_API_KEY 없음 준비
2. 상권 문서 청킹·임베딩의 '오프라인 임베딩' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

64차원 로컬 임베딩

## 판정 기준

PASS: 64차원 로컬 임베딩 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | API 키 없이 get_embedding 은 64차원 로컬 벡터를 반환한다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
