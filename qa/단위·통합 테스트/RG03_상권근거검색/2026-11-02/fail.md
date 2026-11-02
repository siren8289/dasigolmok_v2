# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG03-013 | 하이브리드 검색·재순위화 | 중복 문서 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG03-015 | 하이브리드 검색·재순위화 | 없는 자치구 fallback 교차오염 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG03-016 | 하이브리드 검색·재순위화 | 동 매칭 불일치 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG03-017 | 하이브리드 검색·재순위화 | 업종 불일치 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG03-018 | 하이브리드 검색·재순위화 | 분기 조건 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG03-019 | 하이브리드 검색·재순위화 | 시점 최신성 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG03-025 | 하이브리드 검색·재순위화 | pgvector 임베딩 차원 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG03-026 | 하이브리드 검색·재순위화 | pgvector 백엔드 미연결 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG03-027 | 하이브리드 검색·재순위화 | 콘텐츠 타입 비정상 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## RG03-013 중복 문서
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 중복 제거 여부 확인
- 실제: 동일 id가 중복 반환됨: ['dup', 'dup']
- 결함ID: DEF-RG03-013
- 코드: ai/src/features/commercial_rag_001/market_search/service.py

## RG03-015 없는 자치구 fallback 교차오염
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 타구 문서가 동일 지역 근거로 오안내되지 않도록 차단
- 실제: 없는구 검색이 타구 ['종로구', '강남구', '마포구', '강남구', '마포구'] 문서를 불일치 표시 없이 반환함
- 결함ID: DEF-RG03-015
- 코드: ai/src/features/commercial_rag_001/market_search/service.py

## RG03-016 동 매칭 불일치
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 다른 동 문서에 근거해 단정하지 않기
- 실제: 없는동 검색이 다른 동 ['연남동', '연남동'] 문서를 경고 없이 반환함
- 결함ID: DEF-RG03-016
- 코드: ai/src/features/commercial_rag_001/market_search/service.py

## RG03-017 업종 불일치
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 타업종 보고서 표시 정책 검증
- 실제: 없는업종 검색이 타업종 ['한식음식점', '한식음식점'] 보고서를 표시 없이 반환함
- 결함ID: DEF-RG03-017
- 코드: ai/src/features/commercial_rag_001/market_search/service.py

## RG03-018 분기 조건
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 분기 조건이 실제 필터로 반영되어야 한다
- 실제: quarter=1999-1 필터가 무시되고 ['2024-4', '2024-4'] 문서가 반환됨
- 결함ID: DEF-RG03-018
- 코드: ai/src/features/commercial_rag_001/market_search/service.py

## RG03-019 시점 최신성
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 오래된 문서 최신 통계처럼 오안내 방지
- 실제: 2019-1 문서가 최신성 표시 없이 반환됨 metadata={}
- 결함ID: DEF-RG03-019
- 코드: ai/src/features/commercial_rag_001/market_search/service.py

## RG03-025 pgvector 임베딩 차원
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 실제 색인과 쿼리 벡터 차원 일치
- 실제: 768차원 쿼리 벡터가 vector(64) 검사 없이 execute 로 전달됨
- 결함ID: DEF-RG03-025
- 코드: ai/src/features/commercial_rag_001/market_search/service.py

## RG03-026 pgvector 백엔드 미연결
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: DB 경로 미사용 여부 확인
- 실제: search_market_evidence 가 search_pgvector 를 호출하지 않음
- 결함ID: DEF-RG03-026
- 코드: ai/src/features/commercial_rag_001/market_search/service.py

## RG03-027 콘텐츠 타입 비정상
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 검색 중 타입 에러 방어
- 실제: content=None 타입 에러 미방어: TypeError: can only concatenate str (not "NoneType") to str
- 결함ID: DEF-RG03-027
- 코드: ai/src/features/commercial_rag_001/market_search/service.py
