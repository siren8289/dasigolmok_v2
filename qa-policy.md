# QA·Security 자동화 정책 V3

이 파일이 규칙의 기준이다. `AGENTS.md`와 `.grok/skills/qa-gate/SKILL.md`는 이 절차를 실행하라고 가리킨다. 최초 개발부터 기능 추가, 수정, 유지보수, 버그 수정, 리팩터링, 배포 설정 변경까지 매번 적용한다. 사용자가 QA를 다시 요청하지 않아도 된다.

실행기는 `python qa/runner/qa_gate.py`다. 날짜와 시각은 `Asia/Seoul`이다. 기존 973건 케이스 카드와 `qa/automation/` 이력은 지우거나 덮어쓰지 않는다.

## 1. 폴더 구조

QA 결과는 다음 4개 영역으로만 둔다.

1. `단위·통합 테스트`
2. `웹·API 테스트`
3. `보안·품질 검사`
4. `인프라·배포 검사`

각 영역 안에 기능별 섹션 폴더를 두고, 날짜별로 결과를 저장한다.

`qa/{영역}/{섹션}/{YYYY-MM-DD}/`

각 날짜 폴더에는 아래 파일 5개를 둔다.

- `테스트_시트.xlsx`
- `pass.md`
- `fail.md`
- `risk.md`
- `summary.tsv`

`qa/` 최상단에 만드는 엑셀은 `전체_파트_시트.xlsx` 하나뿐이다. 위험 등록부와 게이트 스탬프는 `qa/reports/`에 둔다.

## 2. 테스트 설계

작업을 시작하기 전에 프로젝트 구조, 기술 스택, 요구사항, 변경 파일의 영향 범위를 확인한다. TC는 ISTQB, OWASP ASVS, OWASP WSTG와 해당 기술의 공식 문서를 기준으로 설계한다.

각 변경에서 다음을 검토한다. 정상값, 예외값, NULL, 빈 값, 경계값, 중복, 오류 응답, 권한, 보안, 회귀.

이미 있는 TC를 재사용하고, 빠진 경우만 추가한다. 요구사항이 불명확하면 동작을 추측하지 않고 `risk.md`에 위험으로 남긴다.

## 3. 교차 검증과 실행 범위

모든 TC는 가능한 한 서로 다른 두 검증 방법으로 이중 테스트한다. 두 검증 결과를 각각 기록하며, 실행하지 않은 검증은 PASS로 처리하지 않는다.

코드를 바꾼 뒤에는 관련 검사를 실행한다. 기능을 완료로 보기 전에 서로 다른 도구 최소 2개로 교차 검증한다. 도구 하나라도 필수 검사가 실패하면 완료로 처리하지 않는다. 수정한 뒤에는 같은 두 도구로 다시 검증하고 회귀 검사를 실행한다.

테스트는 가능한 한 기존 스크립트(`qa/runner/qa_gate.py`, `qa/automation/`, 섹션별 pytest·vitest·gradle)로 실행한다. AI는 신규 TC 작성, 변경 영향 분석, 복잡한 실패 원인 분석에만 쓴다.

- 개발 중: 변경된 기능의 관련 TC만 실행한다. (`--scope auto`)
- PR·배포 전: 전체 회귀를 수행한다. (`--scope ci`)

현재 게이트의 도구 쌍은 다음과 같다.

| 검사 | 영역/섹션 | 도구 A | 도구 B |
| --- | --- | --- | --- |
| record | 보안·품질 검사 / QA02_문서추적회귀 | pytest `qa/runner/tests/test_record.py` | `qa/runner/tools/check_record.py` |
| security | 보안·품질 검사 / QA01_보안비기능 | bandit `--severity-level medium` | `qa/runner/tools/secret_scan.py` |
| front | 웹·API 테스트 / FE01_공통라우팅 | `npm test` (vitest) | `npx tsc --noEmit` |
| python | 단위·통합 테스트 / DE05_결측치이상치 | pytest `data/tests` | `qa/runner/tools/regression_oracle.py` |
| java | 단위·통합 테스트 / BE01_진단요청DTO | `back`의 `./gradlew test` | `qa/runner/tools/junit_audit.py` |
| regression | 단위·통합 테스트 / DE05_결측치이상치 | pytest `qa/automation/de/test_de05.py` | `qa/runner/tools/regression_oracle.py` |

최종 상태는 더 나쁜 쪽을 따른다. 순위는 ERROR, FAIL, BLOCKED, NOT_RUN, SKIPPED, PASS다. PASS는 두 도구가 모두 PASS일 때만이다.

## 4. 기록 규칙

실행한 섹션만 날짜 폴더를 만든다. 같은 날짜에 여러 번 실행하면 `RUN_ID`로 MD에 이어 붙인다. `RUN_ID` 형식은 `YYYYMMDD-HHMMSS`이고, 같은 초가 이미 있으면 `-2`부터 붙인다. 이전 행과 이전 문단은 삭제하거나 덮어쓰지 않는다.

`summary.tsv`와 `qa/reports/risk-register.tsv`는 UTF-8이다. 파일을 처음 만들 때만 Excel용 BOM을 넣는다. 이어 쓸 때는 BOM을 다시 넣지 않는다. 상태 값은 `PASS`, `FAIL`, `BLOCKED`, `ERROR`, `NOT_RUN`, `SKIPPED`만 쓴다. 위험 자체는 TSV 상태가 아니라 `risk.md`와 위험 등록부에 둔다.

공통 연결 항목: `RUN_ID`, `TC_ID`, 실행 날짜와 시각, 영역, 섹션, 기능명, 도구 A, 도구 B, 각 도구 결과, 최종 상태, Git Commit, 검사 대상 파일, 함수명, 줄 번호, `ISSUE_ID`, `RISK_ID`.

코드 위치는 그 실행에서 확인한 값만 적는다. 확인하지 못했으면 `UNKNOWN`이다. Git 커밋은 짧은 해시이고, 워킹 트리가 더러우면 `-dirty`를 붙인다.

## 5. PASS, FAIL, RISK

PASS에는 검증 목적, 사용한 도구, 기대 결과, 실제 결과, 근거를 짧게 적는다.

FAIL에는 입력값, 오류 메시지, 재현 방법, 기대 결과, 실제 결과, 오류 파일, 함수, 줄 번호, 원인 분석, 수정 코드 위치, 재검증 내역을 적는다.

RISK는 테스트 통과와 별도로 적는다. 심각도, 발생 가능성, 영향, 권장 조치, 처리 상태를 포함한다. 심각도는 `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`다. 새 위험은 `OPEN`이다.

FAIL 또는 RISK를 발견하면 코드를 고치기 전에 MD에 먼저 기록하고 사용자에게 보고한다. 미해결 `HIGH` 또는 `CRITICAL` 위험은 완료와 병합을 막는다. 위험을 닫을 때는 `qa/reports/risk-register.tsv`의 상태를 `MITIGATED`로 바꾸고 행은 삭제하지 않는다. 같은 내용, 파일, 줄, 심각도는 다시 추가하지 않는다.

bandit의 MEDIUM은 도구 결과를 실패로 만들지 않고 위험으로 남긴다. HIGH와 CRITICAL, 그리고 비밀 스캔의 HIGH와 CRITICAL은 해당 도구를 FAIL로 만든다.

## 6. 매 작업 절차

1. 요구사항, 변경 파일, 영향 범위를 분석한다.
2. 기존 TC를 확인하고 필요할 때만 추가한다.
3. 코드를 작성하거나 수정한다.
4. 관련 QA와 Security 검사를 실행한다.
5. 최소 2개 도구로 교차 검증한다.
6. PASS, FAIL, RISK로 분류한다.
7. 해당 영역·섹션의 날짜별 파일 5개에 누적 기록한다.
8. 실패하면 원인을 분석하고, 기록 이후에 수정하고, 두 도구로 다시 검증한다.
9. 회귀 검사를 실행한다.
10. 최종 결과와 미해결 위험을 보고한다.

변경 후 명령은 영향 범위에 맞춘다.

```bash
python qa/runner/qa_gate.py --scope auto
```

배포 설정, CI, 넓은 회귀가 포함되면 다음을 실행한다.

```bash
python qa/runner/qa_gate.py --scope ci
```

특정 검사만 다시 돌릴 때는 `--only record,security,front,python,java,regression` 중에서 고른다. `--only`를 써도 실행하지 않은 검증을 PASS로 적지 않는다.

`auto`는 감시 중인 미커밋 경로로 검사를 고른다. 감시 경로는 `qa/runner/tree_hash.py`의 `WATCH_PREFIXES`다. 해당 변경이 없으면 security만 실행한다. 프론트 변경은 front, 백엔드 변경은 java, 데이터 또는 러너 변경은 python과 regression, 러너 변경은 record를 포함한다. security는 항상 포함한다.

게이트는 실패해도 `qa/reports/.gate-stamp.json`에 이번 트리 해시를 남긴다. 그래야 실패를 보고하고 작업을 끝낼 수 있다. 스탬프가 있어도 실패와 미해결 HIGH, CRITICAL은 완료가 아니다.

## 7. 자동화와 기존 이력

- 실행기와 기록기는 `qa/runner/`에 있다.
- 상시 안내는 `AGENTS.md`와 이 파일이다. `.grok/rules/qa-policy.md`는 이 파일과 동일 내용을 유지한다.
- 절차 안내는 `.grok/skills/qa-gate/SKILL.md`다.
- Stop 훅은 `.grok/hooks/qa-gate.json`이다. 감시 파일이 마지막 스탬프와 다르면 종료를 막는다. 프로젝트 훅은 폴더 신뢰 뒤에 동작한다.
- GitHub Actions 워크플로 `.github/workflows/qa-gate.yml`은 `--scope ci`를 실행하고, 게이트가 0이 아니면 CI를 실패시킨다. 기존 `ci.yml`과 `deploy.yml`은 바꾸지 않는다. `main` 푸시는 운영 배포를 호출하므로 이 정책만으로 `main`에 푸시하지 않는다.
- `qa/` 아래의 기존 케이스 카드, `QA_MASTER.tsv`, `qa/automation/` 결과는 이 게이트가 삭제하지 않는다.

완료로 보고하려면 실제 실행 근거, 두 도구의 결과, 날짜별 기록, 미해결 위험 확인이 있어야 한다.
