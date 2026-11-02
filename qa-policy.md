# QA·Security 자동화 정책 V4

이 파일이 규칙의 기준이다. `AGENTS.md`와 `.grok/skills/qa-gate/SKILL.md`는 이 절차를 실행하라고 가리킨다. 최초 개발부터 기능 추가, 수정, 유지보수, 버그 수정, 리팩터링, 배포 설정 변경까지 매번 적용한다. 사용자가 QA를 다시 요청하지 않아도 된다.

실행기는 `python qa/runner/qa_gate.py`다. 날짜와 시각은 `Asia/Seoul`이다. 기존 케이스 카드·자동화 이력은 지우거나 덮어쓰지 않는다.

## 1. QA 테스트 영역

QA는 다음 4개 영역으로 고정한다.

1. 단위·통합 테스트 (`01_unit_integration`)
2. 웹·API 테스트 (`02_web_api`)
3. 보안·품질 검사 (`03_security_quality`)
4. 인프라·배포 검사 (`04_infra_deploy`)

## 2. 파일 및 폴더 명명 규칙

- 모든 파일명과 폴더명은 영어로 작성한다. 한글 경로명은 쓰지 않는다.
- 폴더명·파일명은 소문자 `snake_case`를 권장한다.
- 기능별 섹션명도 영어다. 예: `fe01_common_routing`, `de05_missing_outlier`
- 날짜 폴더는 `YYYY-MM-DD`다.
- Excel 시트 이름과 TC ID 식별자는 영어다.
- 테스트 설명, 예상 결과, 오류 분석, 보고서 본문은 한국어로 작성한다.
- 코드 변수명, 명령어, 설정 키 등 기술 식별자는 영어로 유지한다.

## 3. QA 폴더 구조

```
qa/
├── master_test_sheet.tsv
├── input/
│   └── testcases.tsv
└── results/
    ├── 01_unit_integration/
    ├── 02_web_api/
    ├── 03_security_quality/
    └── 04_infra_deploy/
```

각 영역 안에 기능별 섹션 폴더를 두고, 날짜별로 결과를 저장한다.

`qa/results/{area}/{section}/{YYYY-MM-DD}/`

각 날짜 폴더 파일:

- `test_sheet.xlsx`
- `pass.md`
- `fail.md`
- `risk.md`
- `summary.tsv`

`qa/master_test_sheet.tsv`가 전체 TC 현황을 통합 관리한다. 최상단에 전체 현황 Excel을 중복 생성하지 않는다. 위험 등록부와 게이트 스탬프는 `qa/reports/`에 둔다. 실행기·자동화는 `qa/runner/`, `qa/automation/`에 둔다.

## 4. 이중 테스트 규칙

- 모든 TC는 가능한 한 서로 다른 두 검증 방법으로 테스트한다.
- 두 검증은 서로 다른 관점이나 계층에서 동작을 확인한다.
- 각 TC의 1차·2차 실행 명령, 예상 결과, 실제 결과를 각각 기록한다.
- 두 검증 모두 통과한 경우에만 최종 PASS다.
- 하나라도 실패하면 FAIL이다.
- 검증 불가·미실행은 RISK 또는 NOT_RUN으로 구분한다.
- 실행하지 않은 테스트를 PASS로 기록하지 않는다.

현재 게이트 도구 쌍:

| 검사 | area/section | 도구 A | 도구 B |
| --- | --- | --- | --- |
| record | `03_security_quality` / `qa02_doc_trace_regression` | pytest `qa/runner/tests/test_record.py` | `qa/runner/tools/check_record.py` |
| security | `03_security_quality` / `qa01_security_nfr` | bandit | `qa/runner/tools/secret_scan.py` |
| front | `02_web_api` / `fe01_common_routing` | `npm test` | `npx tsc --noEmit` |
| python | `01_unit_integration` / `de05_missing_outlier` | pytest `data/tests` | `qa/runner/tools/regression_oracle.py` |
| java | `01_unit_integration` / `be01_diagnosis_request_dto` | `./gradlew test` | `qa/runner/tools/junit_audit.py` |
| regression | `01_unit_integration` / `de05_missing_outlier` | pytest `qa/automation/de/test_de05.py` | `qa/runner/tools/regression_oracle.py` |

최종 상태 순위: ERROR, FAIL, BLOCKED, NOT_RUN, SKIPPED, PASS. PASS는 두 도구가 모두 PASS일 때만이다.

## 5. 자동화 및 AI 토큰 절약

- QA Agent 1개와 QA Skill 1개를 사용한다.
- 신규 TC 작성, 변경 영향 분석, 복잡한 실패 원인 분석에만 AI를 쓴다.
- 기존 테스트 실행과 결과 판정은 자동화 스크립트로 처리한다.
- 테스트 실행 시 전체 프로젝트와 TSV를 매번 AI에 전달하지 않는다.
- TC를 순차 실행하고 결과 시트를 갱신한다.
- Excel·Markdown 보고서 생성은 AI 호출 없이 수행한다.

## 6. 지속적인 QC

- 신규 기능 개발 시 해당 기능 TC를 추가한다.
- 기능 수정 시 연결된 TC를 재실행한다. (`--scope auto`)
- 실패 TC 수정 후 관련 회귀를 수행한다.
- PR·배포 전 전체 회귀를 실행한다. (`--scope ci`)
- 필수 테스트 실패 시 CI에서 병합·배포를 차단한다.
- 실행 결과와 테스트 이력을 보존한다. 같은 날의 이전 RUN_ID는 지우거나 덮어쓰지 않는다.

```bash
python qa/runner/qa_gate.py --scope auto
python qa/runner/qa_gate.py --scope ci
```

`auto`는 `qa/runner/tree_hash.py`의 `WATCH_PREFIXES`로 검사를 고른다. security는 항상 포함한다. 게이트는 실패해도 `qa/reports/.gate-stamp.json`에 트리 해시를 남긴다.

## 7. PASS, FAIL, RISK와 최종 보고

FAIL 또는 RISK는 코드를 고치기 전에 MD에 기록하고 사용자에게 보고한다. 미해결 HIGH/CRITICAL은 완료·병합을 막는다. 위험을 닫을 때는 `qa/reports/risk-register.tsv` 상태를 `MITIGATED`로 바꾸고 행은 삭제하지 않는다.

모든 테스트 종료 후 기록:

- 전체 TC 수
- PASS / FAIL / RISK / NOT_RUN
- 1차·2차 검증 결과
- 실패 원인과 재현 절차
- 추가 테스트가 필요한 항목
- 실행 일시 및 관련 코드 위치

본문은 한국어, 파일명·폴더명·기술 식별자는 영어다.

## 8. 자동화 위치

- 실행기·기록기: `qa/runner/`
- 상시 안내: `AGENTS.md`, 이 파일. `.grok/rules/qa-policy.md`는 이 파일 링크다.
- 절차: `.grok/skills/qa-gate/SKILL.md`
- Stop 훅: `.grok/hooks/qa-gate.json`
- GitHub Actions: `.github/workflows/qa-gate.yml` (`--scope ci`). `main` 푸시는 운영 배포를 호출하므로 이 정책만으로 `main`에 푸시하지 않는다.
