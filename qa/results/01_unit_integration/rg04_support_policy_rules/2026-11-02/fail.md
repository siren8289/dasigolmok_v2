# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG04-009 | 지원정책 기간·적합성 | 기준 날짜 잘못된 형식 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG04-026 | 지원정책 기간·적합성 | top_k=-1 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG04-028 | 지원정책 기간·적합성 | 정책 원천 진위 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG04-029 | 지원정책 기간·적합성 | 소진 조기마감 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG04-030 | 지원정책 기간·적합성 | 날짜 범위 역전 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG04-031 | 지원정책 기간·적합성 | 정책 중복 제목 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| RG04-032 | 지원정책 기간·적합성 | today timezone | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## RG04-009 기준 날짜 잘못된 형식
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 오류를 사용자에 알리고 현시점 fallback 오판 방지
- 실제: 기준일 2026/11/02 가 오류 없이 ('open', True)로 판정됨
- 결함ID: DEF-RG04-009
- 코드: ai/src/features/commercial_rag_001/support_policy/service.py

## RG04-026 top_k=-1
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 잘못된 결과 슬라이싱 방어
- 실제: top_k=-1 이 검증 없이 5건 반환(전체 6)
- 결함ID: DEF-RG04-026
- 코드: ai/src/features/commercial_rag_001/support_policy/service.py

## RG04-028 정책 원천 진위
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 실제 공식 공고 확인 전 실시간 공고 단정 금지
- 실제: 정책 검색 결과에 공식 공고 미확인 표시가 없음
- 결함ID: DEF-RG04-028
- 코드: ai/src/features/commercial_rag_001/support_policy/service.py

## RG04-029 소진 조기마감
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 출처 최신 상태 확인 경고 필요
- 실제: 접수중 정책 결과에 예산 소진·출처 최신 확인 경고가 없음
- 결함ID: DEF-RG04-029
- 코드: ai/src/features/commercial_rag_001/support_policy/service.py

## RG04-030 날짜 범위 역전
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 잘못된 데이터 차단
- 실제: 시작>종료 범위가 ('upcoming', False)로 통과함
- 결함ID: DEF-RG04-030
- 코드: ai/src/features/commercial_rag_001/support_policy/service.py

## RG04-031 정책 중복 제목
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: id 기준 중복 정리 정책
- 실제: 동일 id 정책이 2건 반환됨
- 결함ID: DEF-RG04-031
- 코드: ai/src/features/commercial_rag_001/support_policy/service.py

## RG04-032 today timezone
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 시점 일관성 보장
- 실제: KST 2026-11-02 00:00 상당 시각인데 마감일 11-01 정책이 open,True
- 결함ID: DEF-RG04-032
- 코드: ai/src/features/commercial_rag_001/support_policy/service.py
