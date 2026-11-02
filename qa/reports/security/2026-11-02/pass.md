# PASS

## 20261102-201533

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty
### TC-SEC-001 정적 보안

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: security
- 검증 목적: ISTQB 예외·OWASP ASVS 비밀관리와 출력 이스케이프를 두 정적 도구로 확인
- 도구 A: bandit / 결과 PASS
- 도구 A 명령: `/private/tmp/qa-venv/bin/python -m bandit -r ai/src data/etl -f json -q --severity-level medium`
- 도구 B: secret_scan / 결과 PASS
- 도구 B 명령: `/private/tmp/qa-venv/bin/python qa/runner/tools/secret_scan.py /Users/jeong-yelim/orca/dasigolmok_v2`
- 최종 상태: PASS
- 기대 결과: HIGH/CRITICAL 비밀·취약점 없음
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] bandit findings=0 high=0 exit=0 || B[PASS] secret findings=0 blocking=0 exit=0
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -

## 20261102-221207

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
### TC-SEC-001 정적 보안

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: security
- 검증 목적: ISTQB 예외·OWASP ASVS 비밀관리와 출력 이스케이프를 두 정적 도구로 확인
- 도구 A: bandit / 결과 PASS
- 도구 A 명령: `/private/tmp/qa-venv/bin/python -m bandit -r ai/src data/etl -f json -q --severity-level medium`
- 도구 B: secret_scan / 결과 PASS
- 도구 B 명령: `/private/tmp/qa-venv/bin/python qa/runner/tools/secret_scan.py /Users/jeong-yelim/orca/dasigolmok_v2`
- 최종 상태: PASS
- 기대 결과: HIGH/CRITICAL 비밀·취약점 없음
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] bandit findings=0 high=0 exit=0 || B[PASS] secret findings=0 blocking=0 exit=0
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
