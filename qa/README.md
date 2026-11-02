# dasiGolmok v2 QA

973건 TC를 영어 섹션으로 관리하고, 실행 결과는 `qa/results/`에 날짜별로 쌓는다.

## 구조

```
qa/
├── master_test_sheet.tsv
├── input/
│   ├── testcases.tsv
│   └── cases/                 # 케이스 카드 (영문 섹션명)
├── results/
│   ├── 01_unit_integration/
│   ├── 02_web_api/
│   ├── 03_security_quality/
│   └── 04_infra_deploy/
├── runner/                    # 게이트 실행기
└── automation/                # 섹션별 자동화
```

날짜 폴더 파일: `test_sheet.xlsx`, `pass.md`, `fail.md`, `risk.md`, `summary.tsv`

경로·식별자는 영어, 보고서 본문은 한국어다. 최상단 전체 Excel은 만들지 않는다.

## 상시 게이트

```bash
python qa/runner/qa_gate.py --scope auto   # 개발 중 관련 TC
python qa/runner/qa_gate.py --scope ci     # PR·배포 전 전체 회귀
```

자세한 규칙은 `qa-policy.md`를 따른다.
