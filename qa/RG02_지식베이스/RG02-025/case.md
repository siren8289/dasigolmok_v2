# RG02-025 실제 공개 자료 여부

| 항목 | 내용 |
| --- | --- |
| TC ID | RG02-025 |
| 분야 | RG02_지식베이스 |
| 세부 기능 | 상권 문서 청킹·임베딩 |
| 원자 검증 항목 | 실제 공개 자료 여부 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/market_knowledge/service.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/market_knowledge/service.py |

## 검증 목적

상권 문서 청킹·임베딩에서 '실제 공개 자료 여부' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

상권 문서 청킹·임베딩 모듈 준비; 입력 사례 '실제 공개 자료 여부'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

하드코딩 샘플 문서

## 실행 절차

1. 하드코딩 샘플 문서 준비
2. 상권 문서 청킹·임베딩의 '실제 공개 자료 여부' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

실제 공시 확인 전 실데이터로 표기 금지

## 판정 기준

PASS: 실제 공시 확인 전 실데이터로 표기 금지 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | 표본/미검증 표시 없는 문서 8건: rep-mapo-yeonnam-2024q4, rep-gangnam-yeoksam-2024q4, rep-jongno-ikseon-2024q4, pol-seoul-safe-loan-2026 |
| 결함 ID (Q) | DEF-RG02-025 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
