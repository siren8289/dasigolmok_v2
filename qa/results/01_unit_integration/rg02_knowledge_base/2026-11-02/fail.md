# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG02-012 | 상권 문서 청킹·임베딩 | 0글자 문서 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG02-013 | 상권 문서 청킹·임베딩 | chunk_size=overlap | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG02-014 | 상권 문서 청킹·임베딩 | chunk_size 음수 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG02-023 | 상권 문서 청킹·임베딩 | 다차원 불일치 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG02-024 | 상권 문서 청킹·임베딩 | 임베딩 차원 DB 일치 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG02-025 | 상권 문서 청킹·임베딩 | 실제 공개 자료 여부 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG02-026 | 상권 문서 청킹·임베딩 | 지식 문서 갱신 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## RG02-012 0글자 문서
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 빈 문서 검색 처리 정책
- 실제: 공백 문서가 검색 청크로 남음: ['']
- 결함ID: DEF-RG02-012
- 코드: ai/src/features/commercial_rag_001/market_knowledge/service.py

## RG02-013 chunk_size=overlap
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 무한루프 없이 입력 거절 필요
- 실제: chunk_size=overlap 인데 거절하지 않고 151개 청크를 생성함
- 결함ID: DEF-RG02-013
- 코드: ai/src/features/commercial_rag_001/market_knowledge/service.py

## RG02-014 chunk_size 음수
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 무한루프/잘못된 슬라이싱 차단
- 실제: chunk_size=-10 이 거절되지 않고 10개 청크를 생성함: ['가가가가가가가가가가', '가가가가가가가가가가', '가가가가가가가가가가', '가가가가가가가가가가', '가가가가가가가가가가', '가가가가가가가가가가', '가가가가가가가가가가', '가가가가가가가가가가', '가가가가가가가가가가', '가가가가가가가가가가']
- 결함ID: DEF-RG02-014
- 코드: ai/src/features/commercial_rag_001/market_knowledge/service.py

## RG02-023 다차원 불일치
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 명확한 경고/대체 차원 정책
- 실제: 64차원과 512차원을 경고 없이 유사도 1.0으로 잘랐다
- 결함ID: DEF-RG02-023
- 코드: ai/src/features/commercial_rag_001/market_knowledge/service.py

## RG02-024 임베딩 차원 DB 일치
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: DB 스키마와 모형 차원 정합성 확인
- 실제: API 768차원이 DB vector(64) 검증 없이 768차원으로 반환됨
- 결함ID: DEF-RG02-024
- 코드: ai/src/features/commercial_rag_001/market_knowledge/service.py

## RG02-025 실제 공개 자료 여부
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 실제 공시 확인 전 실데이터로 표기 금지
- 실제: 표본/미검증 표시 없는 문서 8건: rep-mapo-yeonnam-2024q4, rep-gangnam-yeoksam-2024q4, rep-jongno-ikseon-2024q4, pol-seoul-safe-loan-2026
- 결함ID: DEF-RG02-025
- 코드: ai/src/features/commercial_rag_001/market_knowledge/service.py

## RG02-026 지식 문서 갱신
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 캐시 갱신 정책 점검
- 실제: 보고서 추가 후에도 get_cached_chunks 가 기존 캐시만 반환함
- 결함ID: DEF-RG02-026
- 코드: ai/src/features/commercial_rag_001/market_knowledge/service.py
