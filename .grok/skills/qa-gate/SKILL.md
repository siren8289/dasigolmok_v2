---
name: qa-gate
description: Run the dasiGolmok QA and security gate after code, test, or deploy-config changes and append dated reports. Use when implementing, fixing, refactoring, or changing CI and deployment files, and when the user mentions QA, security checks, or qa/reports.
---

# QA 게이트

기준은 `qa-policy.md`다. 절차를 여기에 다시 쓰지 말고 그 파일의 10단계를 따른다.

코드를 바꾼 뒤, 작업을 완료라고 말하기 전에 저장소 루트에서 실행한다.

```bash
python qa/runner/qa_gate.py --scope auto
```

배포 설정, CI, 여러 영역을 한 번에 바꾼 경우에는 `--scope ci`를 실행한다. 실패한 검사만 다시 볼 때는 `--only`에 `record`, `security`, `front`, `python`, `java`, `regression`만 넣는다.

게이트가 끝난 뒤 `qa/reports`의 이번 RUN_ID를 읽고, FAIL과 OPEN HIGH/CRITICAL을 사용자에게 보고한다. FAIL 또는 RISK 기록보다 먼저 제품 코드를 고치지 않는다. 미실행 종류는 폴더가 없고 성공이 아니다.

`main`에는 푸시하지 않는다. 기존 `qa/` 이력은 삭제하지 않는다.
