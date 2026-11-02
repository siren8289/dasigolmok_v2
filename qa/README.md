# dasiGolmok v2 QA (V3.0)

## Layout

```
qa/
├── master_test_sheet.xlsx
├── input/testcases.tsv
├── config/test_map.json
├── history/execution_log.tsv
├── results/{01_unit_integration|02_web_api|03_security_quality|04_infra_deploy}/
├── runner/
└── automation/
```

Date folder files: `test_sheet.xlsx`, `pass.md`, `fail.md`, `risk.md`, `results.tsv`

Paths/IDs are English. Report bodies are Korean. Policy: `../qa-policy.md`.

## Gate

```bash
python qa/runner/qa_gate.py --scope auto
python qa/runner/qa_gate.py --scope ci
```

Local Stop hook: `.grok/hooks/qa-gate.json`  
CI: `.github/workflows/qa-gate.yml` (gate + CodeQL)
