# RG02-011 중첩량 보존

| 항목 | 내용 |
| --- | --- |
| TC ID | RG02-011 |
| 분야 | RG02_지식베이스 |
| 세부 기능 | 상권 문서 청킹·임베딩 |
| 원자 검증 항목 | 중첩량 보존 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/market_knowledge/service.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/market_knowledge/service.py |

## 검증 목적

상권 문서 청킹·임베딩에서 '중첩량 보존' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

상권 문서 청킹·임베딩 모듈 준비; 입력 사례 '중첩량 보존'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

chunk_size=250 overlap=50

## 실행 절차

1. chunk_size=250 overlap=50 준비
2. 상권 문서 청킹·임베딩의 '중첩량 보존' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

서로 겹치는 본문 50자

## 판정 기준

PASS: 서로 겹치는 본문 50자 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | overlap=50 이면 인접 청크 본문이 50자 겹친다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
