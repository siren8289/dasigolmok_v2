# RG05-002 진단 업종 없음

| 항목 | 내용 |
| --- | --- |
| TC ID | RG05-002 |
| 분야 | RG05_종합가이드 |
| 세부 기능 | 상권 진단·출처 결합 설명 |
| 원자 검증 항목 | 진단 업종 없음 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/모킹 + HTTPX |
| 관련 코드 경로 | `ai/src/features/commercial_rag_001/commercial_guidance/service.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/ai/src/features/commercial_rag_001/commercial_guidance/service.py |

## 검증 목적

상권 진단·출처 결합 설명에서 '진단 업종 없음' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

상권 진단·출처 결합 설명 모듈 준비; 입력 사례 '진단 업종 없음'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

industry=None

## 실행 절차

1. industry=None 준비
2. 상권 진단·출처 결합 설명의 '진단 업종 없음' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

진단 None 반환

## 판정 기준

PASS: 진단 None 반환 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | industry 가 없으면 진단은 None 이고 base_diagnose 를 호출하지 않는다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
