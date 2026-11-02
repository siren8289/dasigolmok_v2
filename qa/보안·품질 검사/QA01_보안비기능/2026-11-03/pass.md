# PASS

## 20261103-010421

- 실행 시각: 2026-11-03T01:04:21+0900
- Git Commit: 16c28b4-dirty
### TC-SEC-001 정적 보안

- 실행 시각: 2026-11-03T01:04:21+0900
- Git Commit: 16c28b4-dirty
- 영역: 보안·품질 검사
- 섹션: QA01_보안비기능
- 테스트 종류: security
- 검증 목적: ISTQB 예외·OWASP ASVS 비밀관리와 출력 이스케이프를 두 정적 도구로 확인
- 도구 A: bandit / 결과 PASS
- 도구 A 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m bandit -r ai/src data/etl -f json -q --severity-level medium`
- 도구 B: secret_scan / 결과 PASS
- 도구 B 명령: `/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 qa/runner/tools/secret_scan.py /Users/jeong-yelim/orca/dasigolmok_v2`
- 최종 상태: PASS
- 기대 결과: HIGH/CRITICAL 비밀·취약점 없음
- 실제 결과: A=PASS, B=PASS, final=PASS
- 근거: A[PASS] bandit findings=0 high=0 exit=0 || B[PASS] secret findings=0 blocking=0 exit=0
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
