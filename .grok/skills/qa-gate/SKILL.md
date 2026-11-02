---
name: qa-gate
description: Run the dasiGolmok QA and security gate after code, test, or deploy-config changes and append dated reports under the four QA areas. Use when implementing, fixing, refactoring, or changing CI and deployment files, and when the user mentions QA, security checks, or qa/ reports.
---

# QA 게이트

기준은 `qa-policy.md`다. 절차를 여기에 다시 쓰지 말고 그 파일의 단계를 따른다.

코드를 바꾼 뒤, 작업을 완료라고 말하기 전에 저장소 루트에서 실행한다.

```bash
python qa/runner/qa_gate.py --scope auto
```

배포 설정, CI, 여러 영역을 한 번에 바꾼 경우에는 `--scope ci`를 실행한다. 실패한 검사만 다시 볼 때는 `--only`에 `record`, `security`, `front`, `python`, `java`, `regression`만 넣는다.

게이트가 끝난 뒤 이번 RUN_ID와 `qa/{영역}/{섹션}/{날짜}/` 기록을 읽고, FAIL과 OPEN HIGH/CRITICAL을 사용자에게 보고한다. FAIL 또는 RISK 기록보다 먼저 제품 코드를 고치지 않는다. 실행하지 않은 검증은 PASS가 아니다.

결과는 네 영역(`단위·통합 테스트`, `웹·API 테스트`, `보안·품질 검사`, `인프라·배포 검사`) 아래 섹션·날짜 폴더에 `테스트_시트.xlsx`, `pass.md`, `fail.md`, `risk.md`, `summary.tsv`로 남긴다. `qa/` 최상단 엑셀은 `전체_파트_시트.xlsx`만 둔다.

`main`에는 푸시하지 않는다. 기존 `qa/` 케이스 카드와 자동화 이력은 삭제하지 않는다.
