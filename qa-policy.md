# QA·Security 자동화 정책 V3.0

이 파일이 규칙의 기준이다. `AGENTS.md`와 `.grok/skills/qa-gate/SKILL.md`는 이 절차를 실행하라고 가리킨다. 신규 기능 개발, 수정, 유지보수, 버그 수정, 리팩터링, API·DB·UI·인프라·배포 설정 변경마다 TC 추가/갱신과 자동 검증을 수행한다. 사용자가 매번 QA를 요청할 필요가 없다.

실행기는 `python qa/runner/qa_gate.py`다. 날짜·시각은 `Asia/Seoul`이다. 지침만 작성했다고 자동 실행되었다고 보고하지 않는다. 로컬 Hook과 GitHub Actions를 연결하고 작동을 검증한다.

## 1. 4개 QA 영역과 이중 검증

| 영역 폴더 | 1차 검증 | 2차 검증 | 핵심 검증 |
| --- | --- | --- | --- |
| `01_unit_integration` | JUnit / pytest / Vitest (해당 스택) | 독립 오라클·JUnit XML 재집계·tsc 등 별도 경로. DB 의존 시 Testcontainers 또는 API/DB 블랙박스 | 함수 결과, 분기, 연동 |
| `02_web_api` | httpx/TestClient 계약 (Playwright 도입 후 UI 흐름으로 확장) | curl 실서버 스모크 (Schemathesis/Postman CLI 도입 후 교체·추가) | HTTP 상태·본문·오류 |
| `03_security_quality` | Semgrep | secret_scan + **CI CodeQL** | 취약 패턴·비밀·인가 |
| `04_infra_deploy` | `docker compose config`·healthcheck | curl HTTP 스모크 (부하 목표는 k6, 격리 환경만) | 컨테이너 준비·실제 요청 |

- 같은 명령을 두 번 실행한 것은 교차 검증이 아니다.
- 필수 경로가 하나뿐이면 `risk.md`에 이유·대체 계획을 남기고 최종 PASS로 처리하지 않는다.
- CodeQL·Semgrep은 정적 분석이며 UI/API/배포 동작 검사를 대체하지 않는다.

도구 매핑의 실행 명령 원본은 `qa/config/test_map.json`이다. AI가 매번 명령을 추측하지 않는다.

## 2. 원자적 TC 분해

변경된 파일과 연결된 기능부터 `요구사항 → 기능 → 화면/API → 서비스/함수 → DB/외부 → 예외/상태`를 갱신한다. 각 기능은 입력·경계·분기·출력·상태·인증·외부 장애·보안·회귀를 **구분된 TC**로 분해한다. 제외 시 이유를 남긴다. 추측 금지, 근거 없으면 `RISK`.

필수 필드: `TC_ID`, `FEATURE_ID`, `REQUIREMENT_ID`, `AREA`, `SECTION`, `SCENARIO`, `PRECONDITION`, `INPUT`, `STEPS`, `EXPECTED_RESULT`, `TOOL_A`, `COMMAND_A`, `TOOL_B`, `COMMAND_B`, `CODE_FILE`, `FUNCTION`, `RISK_LEVEL`(필요 시). 정의 원본은 `qa/input/testcases.tsv`.

## 3. 작업 순서 (완료 조건)

1. 변경 전: 영향 범위와 기존 TC 매핑
2. 신규 TC는 실행 전에 `qa/input/testcases.tsv`에 등록
3. 코드와 함께 테스트·픽스처·독립 검증 명령 작성
4. 수정 범위 1차·2차 검증을 실제 실행하고 로그·증거 수집
5. FAIL/RISK는 **수정 전에** 보고서·이력 저장 후 사용자 보고
6. 수정 후 해당 TC·회귀를 두 경로로 재검증
7. 필수 TC·두 검증 증거 없으면 완료로 보고하지 않음
8. PR/배포 전 전체 회귀·보안·배포 검증. CI 실패·미해결 HIGH/CRITICAL이면 병합/배포 차단

```bash
python qa/runner/qa_gate.py --scope auto
python qa/runner/qa_gate.py --scope ci
```

## 4. 폴더·파일 규칙 (이름은 영어)

설명·원인 분석·보고서 본문은 한국어. 날짜 `YYYY-MM-DD`(KST).

```
qa/
├── master_test_sheet.xlsx
├── input/
│   └── testcases.tsv
├── config/
│   └── test_map.json
├── history/
│   └── execution_log.tsv
└── results/
    ├── 01_unit_integration/
    ├── 02_web_api/
    ├── 03_security_quality/
    └── 04_infra_deploy/
```

결과 위치: `qa/results/{area}/{section}/{YYYY-MM-DD}/`

- `test_sheet.xlsx`, `pass.md`, `fail.md`, `risk.md`, `results.tsv`
- `master_test_sheet.xlsx`: qa 루트 유일한 전체 현황 Excel
- `execution_log.tsv`: append-only 실행 이력
- 기존 이력 삭제·덮어쓰기 금지. 실행 TSV는 append-only

## 5. 상태·증거·차단

상태: `PASS / FAIL / BLOCKED / ERROR / NOT_RUN / SKIPPED`. RISK는 별도 등록부(`qa/reports/risk-register.tsv`).

- PASS: 두 필수 경로 실행·단언 통과·증거 존재
- FAIL: 필수 단언 실패
- BLOCKED: 환경/의존성으로 검증 불가
- ERROR: 도구·설정·수집 오류
- NOT_RUN / SKIPPED: 미실행·명시 제외(사유 기록). SKIPPED를 PASS로 계산하지 않음

연결 항목: `RUN_ID`, `TC_ID`, `FEATURE_ID`, 시각(KST), 도구·명령·각 결과·최종 상태, 기대/실제, 증거 경로, Git SHA, 파일·함수·줄(`UNKNOWN` 가능), ISSUE/RISK ID. 비밀·개인정보 로그 금지.

미해결 HIGH/CRITICAL이면 완료·병합 금지. 닫을 때 상태를 `MITIGATED`로 바꾸고 행은 삭제하지 않는다.

## 6. 자동화·토큰 최소화

- QA Agent 1개, QA Skill 1개
- 실행·판정·리포트·Excel은 스크립트
- 로컬: `.grok/hooks` Stop 훅이 감시 파일 변경 시 게이트 미실행을 차단
- CI: `.github/workflows/qa-gate.yml`이 push/PR에서 게이트·CodeQL 실행
- AI는 신규 TC 설계·복잡한 영향/원인 분석에만 사용. 전체 코드·TSV를 매번 넣지 않음
- Hook/CI가 검증되지 않으면 “매 작업 자동화 완료”라고 주장하지 않음

## 7. 보고

변경 기능, 신규·수정 TC 수, 영역별 실행, 도구별 상태, PASS/FAIL/BLOCKED/ERROR/NOT_RUN/SKIPPED, 미해결 RISK, 경로, RUN_ID를 한국어로 보고한다.

기능 완료 필수: (1) TC 등록 (2) 테스트 코드·명령 연결 (3) 두 검증 증거 (4) 필수 검증 통과 (5) 결과 5파일·master Excel 반영 (6) 미해결 HIGH/CRITICAL 없음.

## 8. 근거 문서

ISTQB CTFL, OWASP ASVS/WSTG, pytest, Playwright, Docker Compose readiness, GitHub Actions/protected branches, k6 thresholds. 본 문서는 프로젝트 맞춤 운영정책이다.
