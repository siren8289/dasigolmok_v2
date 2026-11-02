# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| QA02-001 | 문서·구현 일치성·테스트 회귀 | README.md 기능 차이 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| QA02-014 | 문서·구현 일치성·테스트 회귀 | TC ID 유일성 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| QA02-015 | 문서·구현 일치성·테스트 회귀 | 테스트 자동화 기록 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| QA02-016 | 문서·구현 일치성·테스트 회귀 | 정적 리뷰 구분 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| QA02-017 | 문서·구현 일치성·테스트 회귀 | 운영 장애 재현 | Docker | RISK | SQL | NOT_RUN | RISK |
| QA02-018 | 문서·구현 일치성·테스트 회귀 | 상태별 판정 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |

## QA02-001 README.md 기능 차이
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: README는 상권 진단·추천만 적고 MV 글은 docs/portfolio-materialized-view.md로 분리한다. README.md와 Readme.md 동일 파일=True.

## QA02-014 TC ID 유일성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: qa/_meta/sections 44개 파일, TC 973건에서 중복 ID가 없다.

## QA02-015 테스트 자동화 기록
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: normalize_status는 passed만 통과로 두고 skipped·failed를 통과로 바꾸지 않는다. 미실행 항목을 PASS로 적지 않는다.

## QA02-016 정적 리뷰 구분
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: compose.yaml을 읽은 뒤에야 pgvector/pgvector:pg16 여부를 판단했다. 문자열이 있어 결함으로 단정하지 않았다.

## QA02-017 운영 장애 재현
- 상태: 검증A RISK / 검증B NOT_RUN / 최종 RISK
- 내용: 측정하지 못했거나 잠재 위험으로 남긴 항목이다.
- 실제: RISK: AI 다운·DB 다운·Nginx 502를 재현하려면 운영 장애 또는 compose up이 필요하다. 여기서 스택을 내리지 않아 로그로 원인을 재현하지 못했다.

## QA02-018 상태별 판정
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: OPS·QA 119개 ID가 스펙 status를 갖고 테스트 함수와 1:1이다.
