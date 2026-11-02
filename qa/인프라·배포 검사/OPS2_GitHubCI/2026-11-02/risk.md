# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| OPS2-001 | CI 4잡·자동검증 | main 푸시 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-002 | CI 4잡·자동검증 | main PR | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-003 | CI 4잡·자동검증 | data pytest | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-004 | CI 4잡·자동검증 | ai pytest | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-005 | CI 4잡·자동검증 | back gradle | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-006 | CI 4잡·자동검증 | front npm | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-007 | CI 4잡·자동검증 | Python 데이터 3.11 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-008 | CI 4잡·자동검증 | Python AI 3.12 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-009 | CI 4잡·자동검증 | Java 17 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-010 | CI 4잡·자동검증 | Node 22 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-011 | CI 4잡·자동검증 | CI 실패 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-013 | CI 4잡·자동검증 | 테스트 커버리지 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |
| OPS2-016 | CI 4잡·자동검증 | 비밀 환경 분리 | Docker | PASS | SQL | NOT_RUN | NOT_RUN |

## OPS2-001 main 푸시
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ci.yml on.push.branches에 main이 있어 main 푸시가 CI를 트리거한다.

## OPS2-002 main PR
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ci.yml on.pull_request.branches에 main이 있어 main PR이 CI를 트리거한다.

## OPS2-003 data pytest
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: data 잡이 python -m pytest data/tests -q 를 실행한다.

## OPS2-004 ai pytest
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ai 잡은 working-directory ai에서 python -m pytest tests -q 를 실행한다.

## OPS2-005 back gradle
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: back 잡은 working-directory back에서 ./gradlew test(JUnit)를 실행한다.

## OPS2-006 front npm
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: front 잡에 npm ci와 npm run build가 별도 스텝으로 있다.

## OPS2-007 Python 데이터 3.11
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: data 잡 setup-python python-version은 3.11이다.

## OPS2-008 Python AI 3.12
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ai 잡 setup-python python-version은 3.12이다.

## OPS2-009 Java 17
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: back 잡 setup-java distribution=temurin, java-version=17이다.

## OPS2-010 Node 22
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: front 잡 setup-node node-version은 22이다.

## OPS2-011 CI 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ai pytest 스텝에 continue-on-error가 없다. 해당 잡이 실패하면 GitHub Actions 워크플로 결론도 실패다.

## OPS2-013 테스트 커버리지
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ai CI가 ai/tests를 pytest로 돌리고 그 안에 test_commercial_rag.py 회귀 테스트가 있다.

## OPS2-016 비밀 환경 분리
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ci.yml은 secrets 참조와 pull_request_target이 없다. 포크 PR에 넘길 비밀키가 워크플로에 없다.
