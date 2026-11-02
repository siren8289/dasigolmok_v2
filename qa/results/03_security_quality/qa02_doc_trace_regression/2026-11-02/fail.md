# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| QA02-002 | 문서·구현 일치성·테스트 회귀 | 레거시 MV 개선 주장 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-003 | 문서·구현 일치성·테스트 회귀 | 레거시 API 문서 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-004 | 문서·구현 일치성·테스트 회귀 | 현재 API 표 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-005 | 문서·구현 일치성·테스트 회귀 | 버전 기록 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-006 | 문서·구현 일치성·테스트 회귀 | RAG 기능 표기 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-007 | 문서·구현 일치성·테스트 회귀 | 배포 방법 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-008 | 문서·구현 일치성·테스트 회귀 | 테스트 방법 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-009 | 문서·구현 일치성·테스트 회귀 | 모델 평가 자료 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-010 | 문서·구현 일치성·테스트 회귀 | 상권통계 데이터 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-011 | 문서·구현 일치성·테스트 회귀 | 지원 정책 원천 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-012 | 문서·구현 일치성·테스트 회귀 | 오류 사례 추가 | Docker | FAIL | SQL | NOT_RUN | FAIL |
| QA02-013 | 문서·구현 일치성·테스트 회귀 | 각 소스 경로 | Docker | FAIL | SQL | NOT_RUN | FAIL |

## QA02-002 레거시 MV 개선 주장
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 실제 최신 코드/측정 로그의 재현 가능성 확인
- 실제: README의 96.2% 문장은 빠져 있고 포트폴리오 문서에만 남았다. 현재 Java에 MV 측정 코드와 원본 측정 로그가 없어 재현할 수 없다.
- 결함ID: DEF-QA02-002
- 코드: README.md

## QA02-003 레거시 API 문서
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 현재 endpoint 존재 여부 구분
- 실제: 현재 컨트롤러는 진단·추천·health뿐인데 README/legacy-deployment가 Auth·Story·Admin의 존재 여부를 대조해 적지 않는다.
- 결함ID: DEF-QA02-003
- 코드: README.md

## QA02-004 현재 API 표
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: GET options,POST diagnose,POST recommend로 동기화
- 실제: README에 GET /api/options, POST /api/diagnoses, POST /api/recommendations 표가 없다. 코드 컨트롤러에는 있다.
- 결함ID: DEF-QA02-004
- 코드: README.md

## QA02-005 버전 기록
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 문서 릴리스 정보 일치
- 실제: ai/src/main.py FastAPI version은 2.1.0인데 README에는 그 릴리스 번호가 없다.
- 결함ID: DEF-QA02-005
- 코드: README.md

## QA02-006 RAG 기능 표기
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 문서와 API 동기화
- 실제: main.py는 /api/v1/commercial-rag/* 를 등록하지만 README는 그 API를 적지 않는다.
- 결함ID: DEF-QA02-006
- 코드: README.md

## QA02-007 배포 방법
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 현재 서비스명/DB 방식과 일치
- 실제: README는 docker compose와 DB_PASSWORD만 적는다. 서비스명 db·ai·back·front와 pgvector Postgres는 compose에만 있다.
- 결함ID: DEF-QA02-007
- 코드: README.md

## QA02-008 테스트 방법
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 실제 CI와 동기화
- 실제: README는 main 푸시 때 docker compose build를 돌린다고 하지만 ci.yml에는 그 스텝이 없다. front는 npm run build다.
- 결함ID: DEF-QA02-008
- 코드: README.md

## QA02-009 모델 평가 자료
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 지표 출처 및 버전 추적
- 실제: metrics_ml.json 키는 ['mae', 'r2', 'rows'] , metrics_dl.json 키는 ['mae', 'r2', 'rows'] 뿐이다. 버전·출처가 없고 README도 이 파일을 가리키지 않는다.
- 결함ID: DEF-QA02-009
- 코드: README.md

## QA02-010 상권통계 데이터
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 수집 분기·규칙 설명
- 실제: transform.py는 가장 최근 분기만 dong_stats로 남기지만 README 전처리 절은 dong_stats.json과 그 분기 규칙을 설명하지 않는다.
- 결함ID: DEF-QA02-010
- 코드: README.md

## QA02-011 지원 정책 원천
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 실재 여부 근거 링크 및 운영 고지
- 실제: 지원 정책 source_url 6개는 기관 홈 수준이고 공고 본문 경로는 0개다. README에 샘플·실재 여부 고지가 없다.
- 결함ID: DEF-QA02-011
- 코드: README.md

## QA02-012 오류 사례 추가
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 사용자 안내/개발자 운영 문서
- 실제: 핸들러는 400 VALIDATION_ERROR·INVALID_JSON과 500 INTERNAL_ERROR를 반환하지만 README에 사용자/운영 오류 안내가 없다.
- 결함ID: DEF-QA02-012
- 코드: README.md

## QA02-013 각 소스 경로
- 검증A: Docker = FAIL
- 검증B: SQL = NOT_RUN
- 예상: 코드 현재 버전과 일치
- 실제: 케이스 URL은 blob/main인데 작업 트리와 HEAD가 다른 문서가 있다: ['README.md']. README 현재 내용과 GitHub URL이 같지 않다.
- 결함ID: DEF-QA02-013
- 코드: README.md
