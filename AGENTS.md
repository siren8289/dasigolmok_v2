# dasiGolmok 작업 규칙

기능 추가, 수정, 유지보수, 버그 수정, 리팩터링, 배포 설정 변경은 매번 QA·Security 게이트를 거친다. 사용자가 QA를 다시 말하지 않아도 된다. 기준 문서는 `qa-policy.md`다.

## 매번 할 일

1. 요구사항, 변경 파일, 영향 범위를 먼저 확인한다.
2. 기존 TC를 재사용하고, 빠진 TC만 추가한다. 불명확한 요구는 추측하지 않고 위험으로 남긴다.
3. 그다음 코드를 수정한다.
4. 관련 검사를 실행한다. 기본 명령은 `python qa/runner/qa_gate.py --scope auto`다. 배포·CI·넓은 변경은 `--scope ci`다.
5. 기능 완료 전에 서로 다른 도구 최소 2개로 교차 검증한다. 도구 하나의 실패, 미실행, 도구 오류는 PASS가 아니다.
6. 결과를 PASS / FAIL / RISK로 나눈다.
7. 실행한 섹션만 `qa/results/{area}/{section}/{YYYY-MM-DD}/`에 `test_sheet.xlsx`, `pass.md`, `fail.md`, `risk.md`, `summary.tsv`로 누적한다. 영역은 `01_unit_integration`, `02_web_api`, `03_security_quality`, `04_infra_deploy` 네 개다. 경로명은 영어 `snake_case`만 쓴다. 날짜는 Asia/Seoul이다. 같은 날의 이전 RUN_ID는 지우거나 덮어쓰지 않는다. 전체 현황은 `qa/master_test_sheet.tsv`로 관리하고 최상단 Excel은 만들지 않는다.
8. FAIL 또는 RISK는 코드를 고치기 전에 MD에 기록하고 사용자에게 보고한다. 수정 후 두 도구로 다시 검증하고 회귀 검사를 실행한다.
9. 미해결 HIGH 또는 CRITICAL 위험이 있으면 완료와 병합을 하지 않는다. 위험을 닫을 때는 `qa/reports/risk-register.tsv` 상태를 MITIGATED로 바꾸고 행은 삭제하지 않는다.
10. 최종 보고에 RUN_ID, 도구별 결과, 미실행 종류, 미해결 위험을 적는다. 실행하지 않은 검사는 성공으로 말하지 않는다.

코드 위치는 확인한 값만 적고, 아니면 UNKNOWN이다. TSV 상태는 PASS, FAIL, BLOCKED, ERROR, NOT_RUN, SKIPPED만 쓴다. 보고서 본문은 한국어, 파일·폴더·기술 식별자는 영어다.

기존 `qa/` 케이스 카드와 자동화 이력은 삭제하지 않는다. 개발 중에는 변경 관련 TC만, PR·배포 전에는 전체 회귀를 돌린다. `main` 푸시는 운영 배포를 호출하므로, 배포를 요청받기 전에는 `main`에 푸시하지 않는다.

Stop 훅이 게이트를 요구하면 `qa/runner/qa_gate.py`를 실행한 뒤 종료한다. 훅은 이 폴더를 신뢰한 세션에서 로드된다.
