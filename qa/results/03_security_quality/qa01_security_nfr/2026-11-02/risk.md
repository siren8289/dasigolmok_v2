# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| QA01-001 | 보안·성능·사용자 품질 | SQL 인젝션 방어 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-002 | 보안·성능·사용자 품질 | XSS React 렌더링 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-003 | 보안·성능·사용자 품질 | RAG 프롬프트 주입 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-005 | 보안·성능·사용자 품질 | 공고 종료 오안내 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-009 | 보안·성능·사용자 품질 | 민감정보 노출 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-010 | 보안·성능·사용자 품질 | CORS Origin | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-015 | 보안·성능·사용자 품질 | API 100동시 | Vitest | RISK | Playwright | NOT_RUN | RISK |
| QA01-017 | 보안·성능·사용자 품질 | RAG 벡터 생성 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-020 | 보안·성능·사용자 품질 | 키보드 사용 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-021 | 보안·성능·사용자 품질 | 스크린리더 레이블 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-022 | 보안·성능·사용자 품질 | 색상 대체정보 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-023 | 보안·성능·사용자 품질 | 불확실성 설명 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| QA01-025 | 보안·성능·사용자 품질 | 장애 후 복구 | Vitest | RISK | Playwright | NOT_RUN | RISK |
| QA01-027 | 보안·성능·사용자 품질 | 백업·복구 | Vitest | RISK | Playwright | NOT_RUN | RISK |
| QA01-029 | 보안·성능·사용자 품질 | 사용자 요청 end-to-end | Vitest | RISK | Playwright | NOT_RUN | RISK |

## QA01-001 SQL 인젝션 방어
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: find_stat(' OR 1=1 --')는 None이다. JPA는 메서드 이름 쿼리이고 pgvector는 %s와 cursor.execute(sql, params)를 쓴다.

## QA01-002 XSS React 렌더링
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: vitest FE03-023 통과. explanation의 img/script 문자열이 텍스트로만 보이고 script·img 요소는 생기지 않는다.

## QA01-003 RAG 프롬프트 주입
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: detect_prompt_injection이 ignore previous instructions를 차단했다. 메시지: 비정상적인 요청 패턴이 감지되어 차단되었습니다: 'ignore previous instructions'

## QA01-005 공고 종료 오안내
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 2024-06-30 종료 공고는 2026-11-02 기준 closed/False이다. 종료 3건은 is_open이 아니다.

## QA01-009 민감정보 노출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 500은 '서버 오류가 발생했습니다.' 고정 문구이고 AI 실패도 'AI 서버 호출에 실패했습니다.'만 반환한다. 비밀번호·키는 본문에 없다.

## QA01-010 CORS Origin
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: CORS는 application.yml과 compose의 명시적 Origin 목록만 허용한다. https://evil.example 은 없고 와일드카드 오리진도 없다.

## QA01-015 API 100동시
- 상태: 검증A RISK / 검증B NOT_RUN / 최종 RISK
- 내용: 측정하지 못했거나 잠재 위험으로 남긴 항목이다.
- 실제: RISK: 100동시 analyze의 오류율·p95를 재지 않았다. 실행 중인 API가 없고 docker compose up은 범위 밖이다.

## QA01-017 RAG 벡터 생성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 청크 임베딩은 _EMBEDDINGS_CACHE가 비어 있을 때만 계산하고 이후 검색은 캐시를 재사용한다.

## QA01-020 키보드 사용
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 진단·추천은 label 안 select와 button이라 Tab으로 이동하고 Enter로 버튼을 누를 수 있다.

## QA01-021 스크린리더 레이블
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: DiagnosePage는 자치구·행정동·업종 텍스트가 select를 감싼 label이고 h2 제목이 있다.

## QA01-022 색상 대체정보
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: STATUS_INFO가 안정/주의/위험 문구를 갖고 ResultPage는 status.label 텍스트와 색 클래스를 함께 보여 준다.

## QA01-023 불확실성 설명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: basic_explanation은 공공데이터 추정값·현장 확인을 말하고, RAG 안내문은 실제 결과를 보장하지 않는다고 적는다.

## QA01-025 장애 후 복구
- 상태: 검증A RISK / 검증B NOT_RUN / 최종 RISK
- 내용: 측정하지 못했거나 잠재 위험으로 남긴 항목이다.
- 실제: RISK: db/ai 재시작 뒤 사용자 흐름 재개를 보려면 기동 중인 스택이 필요하다. docker compose up은 범위 밖이라 재시작을 실행하지 않았다.

## QA01-027 백업·복구
- 상태: 검증A RISK / 검증B NOT_RUN / 최종 RISK
- 내용: 측정하지 못했거나 잠재 위험으로 남긴 항목이다.
- 실제: RISK: PostgreSQL 볼륨 백업을 떠서 복원하지 않았다. compose up과 데이터 파괴가 범위 밖이고 저장소에 pg_dump 복원 절차도 없어 무결성을 측정하지 못했다.

## QA01-029 사용자 요청 end-to-end
- 상태: 검증A RISK / 검증B NOT_RUN / 최종 RISK
- 내용: 측정하지 못했거나 잠재 위험으로 남긴 항목이다.
- 실제: RISK: 브라우저→Nginx→Spring→AI→DB 경로는 docker compose up이 금지되어 실행하지 못했다. 결과 UI 성공을 관찰하지 않았다.
