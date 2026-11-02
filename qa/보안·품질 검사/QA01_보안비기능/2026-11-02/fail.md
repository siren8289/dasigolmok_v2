# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| QA01-004 | 보안·성능·사용자 품질 | 지역 데이터 분리 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-006 | 보안·성능·사용자 품질 | 실존 공고 검증 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-007 | 보안·성능·사용자 품질 | RAG 샘플 표시 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-008 | 보안·성능·사용자 품질 | 접근제어 관리자 API | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-011 | 보안·성능·사용자 품질 | CSRF POST | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-012 | 보안·성능·사용자 품질 | HTTP 헤더 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-013 | 보안·성능·사용자 품질 | 보안 취약성 스캔 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-014 | 보안·성능·사용자 품질 | 입력 최대 길이 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-016 | 보안·성능·사용자 품질 | ML 초기 로딩 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-018 | 보안·성능·사용자 품질 | 데이터 최신성 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-019 | 보안·성능·사용자 품질 | 모바일 접근성 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-024 | 보안·성능·사용자 품질 | 사용자 데이터 저장 고지 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-026 | 보안·성능·사용자 품질 | 모니터링 알림 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-028 | 보안·성능·사용자 품질 | 데이터 수정 추적 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |
| QA01-030 | 보안·성능·사용자 품질 | 개선 지표 검증 | Vitest | FAIL | Playwright | NOT_RUN | FAIL |

## QA01-004 지역 데이터 분리
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 지역 다르면 통계 섞이지 않음
- 실제: find_stat(dong, industry)는 구를 보지 않는다. 신사동은 ['강남구', '관악구']에 있고 첫 매칭은 관악구만 반환한다.
- 결함ID: DEF-QA01-004
- 코드: front/src/api/api.ts

## QA01-006 실존 공고 검증
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 공식 모집 페이지와 존재/일자 확인
- 실제: 지원 공고는 POLICY_DATABASE에 고정돼 있고 공식 모집 페이지 존재·일자를 조회하는 코드가 없다. URL은 기관 홈이다.
- 결함ID: DEF-QA01-006
- 코드: front/src/api/api.ts

## QA01-007 RAG 샘플 표시
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 실제 공식 조사로 오인되지 않도록 라벨
- 실제: RAW_KNOWLEDGE_DOCUMENTS 출처가 서울시 상권분석서비스 등으로 적혀 있고 샘플·예시 라벨이 없다.
- 결함ID: DEF-QA01-007
- 코드: front/src/api/api.ts

## QA01-008 접근제어 관리자 API
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 현재 서비스 인증 범위 확인
- 실제: V1 users(ADMIN 역할 가능)는 있으나 Spring Security와 컨트롤러 인가가 없다. 현재 진단 API 인증 범위가 문서·코드에 고정돼 있지 않다.
- 결함ID: DEF-QA01-008
- 코드: front/src/api/api.ts

## QA01-011 CSRF POST
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: CSRF 적정 방어 여부 확인
- 실제: 백엔드에 CSRF 토큰·CookieCsrf 설정이 없다. 쿠키 인증 환경에 대한 방어가 확인되지 않는다.
- 결함ID: DEF-QA01-011
- 코드: front/src/api/api.ts

## QA01-012 HTTP 헤더
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 적정 보안 헤더 설정
- 실제: front/nginx.conf에 Content-Security-Policy와 Referrer-Policy 헤더가 없다.
- 결함ID: DEF-QA01-012
- 코드: front/src/api/api.ts

## QA01-013 보안 취약성 스캔
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: SCA 및 이미지 취약점 탐지
- 실제: 워크플로에 SCA/이미지 스캔이 없고 .github/dependabot.yml도 없다.
- 결함ID: DEF-QA01-013
- 코드: front/src/api/api.ts

## QA01-014 입력 최대 길이
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 메모리/토큰 요청 제한
- 실제: CommercialRagRequest.question에 max_length가 없어 100만 자 질문이 그대로 통과한다.
- 결함ID: DEF-QA01-014
- 코드: front/src/api/api.ts

## QA01-016 ML 초기 로딩
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: Cold-start latency 측정
- 실제: 모델은 최초 1회 적재하지만 Cold-start latency를 재어 둔 로그·벤치마크가 없다.
- 결함ID: DEF-QA01-016
- 코드: front/src/api/api.ts

## QA01-018 데이터 최신성
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 기준 분기 표시
- 실제: Diagnosis.quarter는 API 타입에 있으나 ResultPage·RecommendPage는 기준 분기를 그리지 않는다.
- 결함ID: DEF-QA01-018
- 코드: front/src/api/api.ts

## QA01-019 모바일 접근성
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 탭/테이블 접근성
- 실제: 헤더는 flex-nowrap, 추천 표는 overflow-x 없이 w-full, index.css에 320px 규칙이 없다. 좁은 화면 탭·표 접근이 보장되지 않는다.
- 결함ID: DEF-QA01-019
- 코드: front/src/api/api.ts

## QA01-024 사용자 데이터 저장 고지
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 개인정보·보존정책 설명
- 실제: 진단은 DB에 저장되지만 README와 화면에 개인정보·보존정책 설명이 없다.
- 결함ID: DEF-QA01-024
- 코드: front/src/api/api.ts

## QA01-026 모니터링 알림
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 알림 체계 검증
- 실제: 워크플로와 compose에 API 5xx 버스트 알림(Prometheus, Sentry 등)이 없다.
- 결함ID: DEF-QA01-026
- 코드: front/src/api/api.ts

## QA01-028 데이터 수정 추적
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 데이터 버전 기록
- 실제: dong_stats.json 행과 metrics_ml.json에 데이터 버전·출처 필드가 없다. 갱신 이력을 구분할 키가 없다.
- 결함ID: DEF-QA01-028
- 코드: front/src/api/api.ts

## QA01-030 개선 지표 검증
- 검증A: Vitest = FAIL
- 검증B: Playwright = NOT_RUN
- 예상: 현재 코드에서 측정 환경/재현 가능성 별도 평가
- 실제: README에는 96.2%가 없고, 수치는 docs/portfolio-materialized-view.md에만 있다. 현재 Java에 AnalyticsRefresh 측정 코드·원본 로그가 없어 재현되지 않는다.
- 결함ID: DEF-QA01-030
- 코드: front/src/api/api.ts
