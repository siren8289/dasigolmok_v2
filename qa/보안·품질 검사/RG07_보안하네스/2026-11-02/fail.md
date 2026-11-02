# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG07-024 | RAG 입력 검증·가드레일 | 서버 연산 중단 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG07-027 | RAG 입력 검증·가드레일 | 민감정보 로그 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG07-029 | RAG 입력 검증·가드레일 | 대규모 요청 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## RG07-024 서버 연산 중단
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 실제 중단 여부 검증
- 실제: timeout 판정 뒤에도 작업이 끝까지 실행되어 done=True
- 결함ID: DEF-RG07-024
- 코드: ai/src/features/commercial_rag_001/harness/runtime.py

## RG07-027 민감정보 로그
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 로그 비밀키 마스킹 필요
- 실제: 실행 로그에 비밀키가 마스킹 없이 남음
- 결함ID: DEF-RG07-027
- 코드: ai/src/features/commercial_rag_001/harness/runtime.py

## RG07-029 대규모 요청
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: DoS 제한 및 latency 측정
- 실제: 100회 /ask 상태={200} 이고 라우터에 429/레이트리밋이 없음
- 결함ID: DEF-RG07-029
- 코드: ai/src/features/commercial_rag_001/harness/runtime.py
