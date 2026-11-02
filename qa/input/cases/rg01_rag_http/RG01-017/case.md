# RG01-017 RAG 장애 정보 마스킹

| 항목 | 내용 |
| --- | --- |
| TC ID | RG01-017 |
| 분야 | RG01_RAG_HTTP |
| 세부 기능 | 상권 RAG API |
| 원자 검증 항목 | RAG 장애 정보 마스킹 |
| 우선순위 | P0 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/router.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/router.py |

## 검증 목적

상권 RAG API에서 'RAG 장애 정보 마스킹' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

상권 RAG API 모듈 준비; 입력 사례 'RAG 장애 정보 마스킹'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

예외에 credential 텍스트

## 실행 절차

1. 예외에 credential 텍스트 준비
2. 상권 RAG API의 'RAG 장애 정보 마스킹' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

detail로 내부 정보 노출 방지

## 판정 기준

PASS: detail로 내부 정보 노출 방지 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | 500 detail에 비밀값이 노출됨: {"detail":"RAG 워크플로우 실행 실패: GEMINI_API_KEY=super-secret-RG01-017"} |
| 결함 ID (Q) | DEF-RG01-017 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
