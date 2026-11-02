---
name: qa-gate
description: Run dasiGolmok QA/Security gate after code, test, or deploy-config changes. Use for feature work, refactors, CI/deploy changes, and when the user mentions QA, security, hooks, or qa/results.
---

# QA 게이트 (V3.0)

기준은 `qa-policy.md`다. 절차를 여기에 다시 쓰지 말고 그 파일을 따른다.

완료 보고 전 저장소 루트에서:

```bash
python qa/runner/qa_gate.py --scope auto
```

넓은 변경·PR·배포 전:

```bash
python qa/runner/qa_gate.py --scope ci
```

`--only` 허용: `record,security,front,python,java,regression,web_api,infra`

명령 원본은 `qa/config/test_map.json`. 결과는 `qa/results/{area}/{section}/{date}/`의 `test_sheet.xlsx`, `pass.md`, `fail.md`, `risk.md`, `results.tsv`와 `qa/history/execution_log.tsv`. 전체 현황 Excel은 `qa/master_test_sheet.xlsx`만.

FAIL/RISK를 코드 수정보다 먼저 기록·보고한다. 미실행 검증은 PASS가 아니다. Hook/CI 미검증 상태에서 자동화 완료를 주장하지 않는다. `main`에 푸시하지 않는다.
