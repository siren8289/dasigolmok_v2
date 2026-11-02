# dasiGolmok 작업 규칙

기능 추가·수정·유지보수·버그 수정·리팩터링·API·DB·UI·인프라·배포 설정 변경은 매번 QA·Security 게이트를 거친다. 사용자가 QA를 다시 말할 필요 없다. 기준은 `qa-policy.md`(V3.0)다.

## 매번 할 일

1. 요구사항·변경 파일·영향 범위를 확인한다.
2. 기존 TC를 재사용하고, 신규는 실행 전에 `qa/input/testcases.tsv`에 등록한다. 불명확하면 추측하지 않고 RISK로 남긴다.
3. 코드와 함께 테스트·독립 검증 명령을 작성한다. 명령은 `qa/config/test_map.json`을 따른다.
4. `python qa/runner/qa_gate.py --scope auto`를 실행한다. PR·배포 전은 `--scope ci`다.
5. 서로 다른 두 검증 경로를 실제로 실행한다. 미실행·도구 오류는 PASS가 아니다.
6. FAIL/RISK는 코드를 고치기 전에 `pass.md`/`fail.md`/`risk.md`/`results.tsv`와 `history/execution_log.tsv`에 기록하고 사용자에게 알린다.
7. 결과는 `qa/results/{area}/{section}/{YYYY-MM-DD}/`에만 쌓는다. 영역: `01_unit_integration`, `02_web_api`, `03_security_quality`, `04_infra_deploy`. 경로명은 영어. 전체 Excel은 `qa/master_test_sheet.xlsx`만 둔다.
8. 수정 후 두 경로로 재검증하고 관련 회귀를 돌린다.
9. 미해결 HIGH/CRITICAL이 있으면 완료·병합하지 않는다. 닫을 때 `qa/reports/risk-register.tsv`를 MITIGATED로 바꾸고 행은 삭제하지 않는다.
10. 보고에 RUN_ID, 도구별 결과, 미실행, 미해결 위험을 적는다. Hook/CI가 검증되지 않았으면 자동화 완료라고 말하지 않는다.

상태 값: PASS, FAIL, BLOCKED, ERROR, NOT_RUN, SKIPPED. 본문은 한국어, 파일·폴더·식별자는 영어.

Stop 훅(`.grok/hooks/qa-gate.json`)이 감시 변경을 감지하면 게이트 실행 전 종료를 막는다. `main` 푸시는 배포 요청 전에는 하지 않는다.
