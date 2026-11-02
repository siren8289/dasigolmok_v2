# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG01-008 | 상권 RAG API | RAG ask question 빈문자열 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG01-011 | 상권 RAG API | 지원 정책 top_k 음수 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG01-012 | 상권 RAG API | 시장 검색 top_k=0 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG01-013 | 상권 RAG API | 지원 정책 날짜 형식 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG01-017 | 상권 RAG API | RAG 장애 정보 마스킹 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG01-019 | 상권 RAG API | RAG 직접 공개 여부 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG01-020 | 상권 RAG API | RAG 과도한 요청 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## RG01-008 RAG ask question 빈문자열
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 빈 질문 가드레일 검증
- 실제: 빈 질문 question='' 이 200로 통과했다. 422 가드레일이 없다
- 결함ID: DEF-RG01-008
- 코드: ai/src/features/commercial_rag_001/router.py

## RG01-011 지원 정책 top_k 음수
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 유효한 1 이상 제한 필요
- 실제: top_k=-1 이 200로 수용되고 total_count=5. 1 이상 제한이 없다
- 결함ID: DEF-RG01-011
- 코드: ai/src/features/commercial_rag_001/router.py

## RG01-012 시장 검색 top_k=0
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 0건 요구에 대한 명확한 검증 필요
- 실제: top_k=0 이 200로 수용되고 documents=0. 0건 요구 검증이 없다
- 결함ID: DEF-RG01-012
- 코드: ai/src/features/commercial_rag_001/router.py

## RG01-013 지원 정책 날짜 형식
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 422 또는 유효성 에러 필요
- 실제: target_date=2026/11/02 가 200로 수용된다. 날짜 형식 검증이 없다
- 결함ID: DEF-RG01-013
- 코드: ai/src/features/commercial_rag_001/router.py

## RG01-017 RAG 장애 정보 마스킹
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: detail로 내부 정보 노출 방지
- 실제: 500 detail에 비밀값이 노출됨: {"detail":"RAG 워크플로우 실행 실패: GEMINI_API_KEY=super-secret-RG01-017"}
- 결함ID: DEF-RG01-017
- 코드: ai/src/features/commercial_rag_001/router.py

## RG01-019 RAG 직접 공개 여부
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 외부 공개 정책과 인증 통제 확인
- 실제: 인증 의존성 없이 GET /health 가 200이다. 라우터 dependencies=[]
- 결함ID: DEF-RG01-019
- 코드: ai/src/features/commercial_rag_001/router.py

## RG01-020 RAG 과도한 요청
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: timeout/요금폭증 방어
- 실제: 50회 연속 /ask 상태={200}. timeout/429 제한이 없다
- 결함ID: DEF-RG01-020
- 코드: ai/src/features/commercial_rag_001/router.py
