# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI01-012 | FastAPI 엔드포인트·스키마 | 빈 문자열 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI01-013 | FastAPI 엔드포인트·스키마 | 최대 길이 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI01-015 | FastAPI 엔드포인트·스키마 | OPTIONS 요청 CORS | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI01-016 | FastAPI 엔드포인트·스키마 | 프론트 경로 비공개 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## AI01-012 빈 문자열
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 잘못된 값에 대한 422 사전 검증
- 실제: dong='' status=404 body={"detail":"해당 행정동·업종 데이터가 없습니다."}
- 결함ID: DEF-AI01-012
- 코드: ai/src/main.py

## AI01-013 최대 길이
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 리소스 보호 위해 길이 제한
- 실제: industry 20000자 status=404 body={"detail":"해당 행정동·업종 데이터가 없습니다."}
- 결함ID: DEF-AI01-013
- 코드: ai/src/main.py

## AI01-015 OPTIONS 요청 CORS
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 환경에 따른 CORS 설정 검증
- 실제: 교차출처 사전요청 OPTIONS Origin=http://localhost:5173 status=405 ACAO=None allow='POST'
- 결함ID: DEF-AI01-015
- 코드: ai/src/main.py

## AI01-016 프론트 경로 비공개
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 네트워크 접근 범위 정책 검증
- 실제: 외부 직접 POST /api/v1/diagnose status=200 auth=None
- 결함ID: DEF-AI01-016
- 코드: ai/src/main.py
