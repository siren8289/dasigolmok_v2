# RG05-024 Gemini 오안내

| 항목 | 내용 |
| --- | --- |
| TC ID | RG05-024 |
| 분야 | RG05_종합가이드 |
| 세부 기능 | 상권 진단·출처 결합 설명 |
| 원자 검증 항목 | Gemini 오안내 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/commercial_guidance/service.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/commercial_guidance/service.py |

## 검증 목적

상권 진단·출처 결합 설명에서 'Gemini 오안내' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

상권 진단·출처 결합 설명 모듈 준비; 입력 사례 'Gemini 오안내'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

LLM 결과='내일 100% 성공'

## 실행 절차

1. LLM 결과='내일 100% 성공' 준비
2. 상권 진단·출처 결합 설명의 'Gemini 오안내' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

근거 없는 보장·정책 마감 문구 후검증 필요

## 판정 기준

PASS: 근거 없는 보장·정책 마감 문구 후검증 필요 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | LLM 문구 '내일 100% 성공'이 후검증 없이 답변에 포함됨 |
| 결함 ID (Q) | DEF-RG05-024 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
