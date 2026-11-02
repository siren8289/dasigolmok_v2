# FAIL

## 20261102-201533

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty
### TC-UNIT-FRONT-001 프론트 단위·타입

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: unit
- 검증 목적: 라우팅·입력·결과·추천·API 클라이언트 테스트와 TypeScript 검사를 교차
- 도구 A: vitest / 결과 FAIL
- 도구 A 명령: `npm test`
- 도구 B: tsc / 결과 FAIL
- 도구 B 명령: `npx tsc --noEmit --pretty false`
- 최종 상태: FAIL
- 기대 결과: vitest 통과이고 tsc --noEmit 오류 없음
- 실제 결과: A=FAIL, B=FAIL, final=FAIL
- 근거: A[FAIL] /1/../../: expected 'http://localhost:8080/api/diagnoses/1…' not to contain '/../'

Expected: "/../"
Received: "http://localhost:8080/api/diagnoses/1/../../"

 ❯ src/test/FE05_api.test.ts:170:38
    168|     await api.getDiagnosis("1/../../").catch(() => undefined);
    169|     const url = String(fetchMock.mock.calls[0][0]);
    170|     expect(url, `실제 URL ${url}`).not.toContain("/../");
       |                                      ^
    171|   });
    172| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[18/18]⎯ || B[FAIL] le 'node:path' or its corresponding type declarations.
src/test/FE01_routing.test.tsx(3,31): error TS2307: Cannot find module 'node:url' or its corresponding type declarations.
src/test/note.ts(1,43): error TS2307: Cannot find module 'node:fs' or its corresponding type declarations.
src/test/note.ts(2,34): error TS2307: Cannot find module 'node:path' or its corresponding type declarations.
src/test/note.ts(3,31): error TS2307: Cannot find module 'node:url' or its corresponding type declarations.
- 파일: front/src/test/FE01_routing.test.tsx
- 함수: UNKNOWN
- 줄 번호: 1
- ISSUE_ID: -
- RISK_ID: RISK-20261102-201533-1
- 입력값: -
- 오류 메시지: t/development/chunk-OB3PAWPO.mjs:7134:13
 ❯ src/test/FE04_recommend.test.tsx:283:33

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[14/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-015
AssertionError: 빈 200 body는 의미 있는 오류 문구로 바뀌어야 한다: expected [Function] to throw error including '요청에 실패했습니다.' but got 'Unexpected end of JSON input'

Expected: "요청에 실패했습니다."
Received: "Unexpected end of JSON input"

 ❯ src/test/FE05_api.test.ts:141:5
    139|     installFetch(async () => new Response("", { status: 200, headers: …
    140|     const api = await loadApi();
    141|     await expect(api.getOptions(), "빈 200 body는 의미 있는 오류 문구로 바뀌어야 한다")…
       |     ^
    142|   });
    143| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[15/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-016
AssertionError: 실제 URL https://host//api/options: expected 'https://host//api/options' not to contain '//api'

Expected: "//api"
Received: "https://host//api/options"

 ❯ src/test/FE05_api.test.ts:150:38
    148|     await api.getOptions();
    149|     const url = String(fetchMock.mock.calls[0][0]);
    150|     expect(url, `실제 URL ${url}`).not.toContain("//api");
       |                                      ^
    151|   });
    152| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[16/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-017
AssertionError: 실제 메시지에 토큰이 남아 있다: token=SECRET-TOKEN-123 failed: expected 'token=SECRET-TOKEN-123 failed' not to contain 'SECRET-TOKEN-123'

Expected: "SECRET-TOKEN-123"
Received: "token=SECRET-TOKEN-123 failed"

 ❯ src/test/FE05_api.test.ts:161:60
    159|     } catch (error) {
    160|       const message = error instanceof Error ? error.message : String(…
    161|       expect(message, `실제 메시지에 토큰이 남아 있다: ${message}`).not.toContain("…
       |                                                            ^
    162|     }
    163|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[17/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-018
AssertionError: 실제 URL http://localhost:8080/api/diagnoses/1/../../: expected 'http://localhost:8080/api/diagnoses/1…' not to contain '/../'

Expected: "/../"
Received: "http://localhost:8080/api/diagnoses/1/../../"

 ❯ src/test/FE05_api.test.ts:170:38
    168|     await api.getDiagnosis("1/../../").catch(() => undefined);
    169|     const url = String(fetchMock.mock.calls[0][0]);
    170|     expect(url, `실제 URL ${url}`).not.toContain("/../");
       |                                      ^
    171|   });
    172| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[18/18]⎯
- 재현 방법: npm test
- 원인 분석: 도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다.
- 수정 코드 위치: 아직 수정하지 않음
- 재검증: 아직 재검증하지 않음

### TC-UNIT-JAVA-001 Spring 진단·추천

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: unit
- 검증 목적: JUnit 실행과 XML 재집계로 실패가 숨지 않는지 확인
- 도구 A: gradle / 결과 FAIL
- 도구 A 명령: `./gradlew test --console=plain`
- 도구 B: junit_audit / 결과 FAIL
- 도구 B 명령: `/private/tmp/qa-venv/bin/python qa/runner/tools/junit_audit.py /Users/jeong-yelim/orca/dasigolmok_v2`
- 최종 상태: FAIL
- 기대 결과: Gradle test 종료 0이고 JUnit XML 실패 0
- 실제 결과: A=FAIL, B=FAIL, final=FAIL
- 근거: A[FAIL] ionable tasks: 1 executed, 3 up-to-date

OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended

122 tests completed, 24 failed

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':test'.
> There were failing tests. See the report at: file:///Users/jeong-yelim/orca/dasigolmok_v2/back/build/reports/tests/test/index.html

* Try:
> Run with --scan to get full insights.

BUILD FAILED in 7s || B[FAIL] golmok.qa.Be03DiagnosisHttpTest.BE03-008,com.dasigolmok.qa.Be03DiagnosisHttpTest.BE03-010,com.dasigolmok.qa.Be03DiagnosisHttpTest.BE03-014,com.dasigolmok.qa.Be04RecommendHttpTest.BE04-016,com.dasigolmok.qa.Be04RecommendHttpTest.BE04-018,com.dasigolmok.qa.Be05AiClientTest.BE05-011,com.dasigolmok.qa.Be05AiClientTest.BE05-012,com.dasigolmok.qa.Be05AiClientTest.BE05-014,com.dasigolmok.qa.Be05AiClientTest.BE05-015,com.dasigolmok.qa.Be05AiClientTest.BE05-016,com.dasigolmok.qa.Be05AiClientTest.BE05-018
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
- 입력값: -
- 오류 메시지: =SA: (connection evicted)
2026-11-02T20:15:51.066+09:00 DEBUG 54240 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn34: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T20:15:51.066+09:00 DEBUG 54240 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn35: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T20:15:51.066+09:00 DEBUG 54240 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn36: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T20:15:51.066+09:00 DEBUG 54240 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn37: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T20:15:51.066+09:00 DEBUG 54240 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn38: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T20:15:51.066+09:00 DEBUG 54240 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn39: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T20:15:51.067+09:00 DEBUG 54240 --- [ionShutdownHook] com.zaxxer.hikari.pool.HikariPool        : HikariPool-4 - After shutdown stats (total=0, active=0, idle=0, waiting=0)
2026-11-02T20:15:51.067+09:00  INFO 54240 --- [ionShutdownHook] com.zaxxer.hikari.HikariDataSource       : HikariPool-4 - Shutdown completed.

> Task :test FAILED

Deprecated Gradle features were used in this build, making it incompatible with Gradle 9.0.

You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.

For more on this, please refer to https://docs.gradle.org/8.9/userguide/command_line_interface.html#sec:command_line_warnings in the Gradle documentation.
4 actionable tasks: 1 executed, 3 up-to-date

OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended

122 tests completed, 24 failed

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':test'.
> There were failing tests. See the report at: file:///Users/jeong-yelim/orca/dasigolmok_v2/back/build/reports/tests/test/index.html

* Try:
> Run with --scan to get full insights.

BUILD FAILED in 7s
- 재현 방법: ./gradlew test --console=plain
- 원인 분석: 도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다.
- 수정 코드 위치: 아직 수정하지 않음
- 재검증: 아직 재검증하지 않음

## 20261102-201658

- 실행 시각: 2026-11-02T20:16:58+0900
- Git Commit: 4c28384-dirty
### TC-UNIT-FRONT-001 프론트 단위·타입

- 실행 시각: 2026-11-02T20:16:58+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: unit
- 검증 목적: 라우팅·입력·결과·추천·API 클라이언트 테스트와 TypeScript 검사를 교차
- 도구 A: vitest / 결과 FAIL
- 도구 A 명령: `npm test`
- 도구 B: tsc / 결과 PASS
- 도구 B 명령: `npx tsc --noEmit --pretty false`
- 최종 상태: FAIL
- 기대 결과: vitest 통과이고 tsc --noEmit 오류 없음
- 실제 결과: A=FAIL, B=PASS, final=FAIL
- 근거: A[FAIL] /1/../../: expected 'http://localhost:8080/api/diagnoses/1…' not to contain '/../'

Expected: "/../"
Received: "http://localhost:8080/api/diagnoses/1/../../"

 ❯ src/test/FE05_api.test.ts:170:38
    168|     await api.getDiagnosis("1/../../").catch(() => undefined);
    169|     const url = String(fetchMock.mock.calls[0][0]);
    170|     expect(url, `실제 URL ${url}`).not.toContain("/../");
       |                                      ^
    171|   });
    172| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[18/18]⎯ || B[PASS] 
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
- 입력값: -
- 오류 메시지: t/development/chunk-OB3PAWPO.mjs:7134:13
 ❯ src/test/FE04_recommend.test.tsx:283:33

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[14/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-015
AssertionError: 빈 200 body는 의미 있는 오류 문구로 바뀌어야 한다: expected [Function] to throw error including '요청에 실패했습니다.' but got 'Unexpected end of JSON input'

Expected: "요청에 실패했습니다."
Received: "Unexpected end of JSON input"

 ❯ src/test/FE05_api.test.ts:141:5
    139|     installFetch(async () => new Response("", { status: 200, headers: …
    140|     const api = await loadApi();
    141|     await expect(api.getOptions(), "빈 200 body는 의미 있는 오류 문구로 바뀌어야 한다")…
       |     ^
    142|   });
    143| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[15/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-016
AssertionError: 실제 URL https://host//api/options: expected 'https://host//api/options' not to contain '//api'

Expected: "//api"
Received: "https://host//api/options"

 ❯ src/test/FE05_api.test.ts:150:38
    148|     await api.getOptions();
    149|     const url = String(fetchMock.mock.calls[0][0]);
    150|     expect(url, `실제 URL ${url}`).not.toContain("//api");
       |                                      ^
    151|   });
    152| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[16/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-017
AssertionError: 실제 메시지에 토큰이 남아 있다: token=SECRET-TOKEN-123 failed: expected 'token=SECRET-TOKEN-123 failed' not to contain 'SECRET-TOKEN-123'

Expected: "SECRET-TOKEN-123"
Received: "token=SECRET-TOKEN-123 failed"

 ❯ src/test/FE05_api.test.ts:161:60
    159|     } catch (error) {
    160|       const message = error instanceof Error ? error.message : String(…
    161|       expect(message, `실제 메시지에 토큰이 남아 있다: ${message}`).not.toContain("…
       |                                                            ^
    162|     }
    163|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[17/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-018
AssertionError: 실제 URL http://localhost:8080/api/diagnoses/1/../../: expected 'http://localhost:8080/api/diagnoses/1…' not to contain '/../'

Expected: "/../"
Received: "http://localhost:8080/api/diagnoses/1/../../"

 ❯ src/test/FE05_api.test.ts:170:38
    168|     await api.getDiagnosis("1/../../").catch(() => undefined);
    169|     const url = String(fetchMock.mock.calls[0][0]);
    170|     expect(url, `실제 URL ${url}`).not.toContain("/../");
       |                                      ^
    171|   });
    172| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[18/18]⎯
- 재현 방법: npm test
- 원인 분석: 도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다.
- 수정 코드 위치: 아직 수정하지 않음
- 재검증: 아직 재검증하지 않음

## 20261102-201740

- 실행 시각: 2026-11-02T20:17:40+0900
- Git Commit: 4c28384-dirty
### TC-UNIT-FRONT-001 프론트 단위·타입

- 실행 시각: 2026-11-02T20:17:40+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: unit
- 검증 목적: 라우팅·입력·결과·추천·API 클라이언트 테스트와 TypeScript 검사를 교차
- 도구 A: vitest / 결과 FAIL
- 도구 A 명령: `npm test`
- 도구 B: tsc / 결과 PASS
- 도구 B 명령: `npx tsc --noEmit --pretty false`
- 최종 상태: FAIL
- 기대 결과: vitest 통과이고 tsc --noEmit 오류 없음
- 실제 결과: A=FAIL, B=PASS, final=FAIL
- 근거: A[FAIL] /1/../../: expected 'http://localhost:8080/api/diagnoses/1…' not to contain '/../'

Expected: "/../"
Received: "http://localhost:8080/api/diagnoses/1/../../"

 ❯ src/test/FE05_api.test.ts:170:38
    168|     await api.getDiagnosis("1/../../").catch(() => undefined);
    169|     const url = String(fetchMock.mock.calls[0][0]);
    170|     expect(url, `실제 URL ${url}`).not.toContain("/../");
       |                                      ^
    171|   });
    172| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[18/18]⎯ || B[PASS] 
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
- 입력값: -
- 오류 메시지: t/development/chunk-OB3PAWPO.mjs:7134:13
 ❯ src/test/FE04_recommend.test.tsx:283:33

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[14/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-015
AssertionError: 빈 200 body는 의미 있는 오류 문구로 바뀌어야 한다: expected [Function] to throw error including '요청에 실패했습니다.' but got 'Unexpected end of JSON input'

Expected: "요청에 실패했습니다."
Received: "Unexpected end of JSON input"

 ❯ src/test/FE05_api.test.ts:141:5
    139|     installFetch(async () => new Response("", { status: 200, headers: …
    140|     const api = await loadApi();
    141|     await expect(api.getOptions(), "빈 200 body는 의미 있는 오류 문구로 바뀌어야 한다")…
       |     ^
    142|   });
    143| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[15/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-016
AssertionError: 실제 URL https://host//api/options: expected 'https://host//api/options' not to contain '//api'

Expected: "//api"
Received: "https://host//api/options"

 ❯ src/test/FE05_api.test.ts:150:38
    148|     await api.getOptions();
    149|     const url = String(fetchMock.mock.calls[0][0]);
    150|     expect(url, `실제 URL ${url}`).not.toContain("//api");
       |                                      ^
    151|   });
    152| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[16/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-017
AssertionError: 실제 메시지에 토큰이 남아 있다: token=SECRET-TOKEN-123 failed: expected 'token=SECRET-TOKEN-123 failed' not to contain 'SECRET-TOKEN-123'

Expected: "SECRET-TOKEN-123"
Received: "token=SECRET-TOKEN-123 failed"

 ❯ src/test/FE05_api.test.ts:161:60
    159|     } catch (error) {
    160|       const message = error instanceof Error ? error.message : String(…
    161|       expect(message, `실제 메시지에 토큰이 남아 있다: ${message}`).not.toContain("…
       |                                                            ^
    162|     }
    163|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[17/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-018
AssertionError: 실제 URL http://localhost:8080/api/diagnoses/1/../../: expected 'http://localhost:8080/api/diagnoses/1…' not to contain '/../'

Expected: "/../"
Received: "http://localhost:8080/api/diagnoses/1/../../"

 ❯ src/test/FE05_api.test.ts:170:38
    168|     await api.getDiagnosis("1/../../").catch(() => undefined);
    169|     const url = String(fetchMock.mock.calls[0][0]);
    170|     expect(url, `실제 URL ${url}`).not.toContain("/../");
       |                                      ^
    171|   });
    172| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[18/18]⎯
- 재현 방법: npm test
- 원인 분석: 도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다.
- 수정 코드 위치: 아직 수정하지 않음
- 재검증: 아직 재검증하지 않음

## 재검증 메모

- RUN 20261102-201740: 도구 A vitest FAIL(출력 인덱스 18/18), 도구 B tsc PASS. 최종 FAIL. 타입 선언 추가로 tsc만 다시 확인했다. vitest 실패 18건은 제품 동작을 바꾸지 않아 그대로다.
- RUN 20261102-201658의 tsc PASS는 루트 `node_modules` 해석이라 재검증 근거로 쓰지 않는다.

## 20261102-221207

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
### TC-UNIT-FRONT-001 프론트 단위·타입

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: unit
- 검증 목적: 라우팅·입력·결과·추천·API 클라이언트 테스트와 TypeScript 검사를 교차
- 도구 A: vitest / 결과 FAIL
- 도구 A 명령: `npm test`
- 도구 B: tsc / 결과 PASS
- 도구 B 명령: `npx tsc --noEmit --pretty false`
- 최종 상태: FAIL
- 기대 결과: vitest 통과이고 tsc --noEmit 오류 없음
- 실제 결과: A=FAIL, B=PASS, final=FAIL
- 근거: A[FAIL] /1/../../: expected 'http://localhost:8080/api/diagnoses/1…' not to contain '/../'

Expected: "/../"
Received: "http://localhost:8080/api/diagnoses/1/../../"

 ❯ src/test/FE05_api.test.ts:170:38
    168|     await api.getDiagnosis("1/../../").catch(() => undefined);
    169|     const url = String(fetchMock.mock.calls[0][0]);
    170|     expect(url, `실제 URL ${url}`).not.toContain("/../");
       |                                      ^
    171|   });
    172| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[18/18]⎯ || B[PASS] 
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
- 입력값: -
- 오류 메시지: t/development/chunk-OB3PAWPO.mjs:7134:13
 ❯ src/test/FE04_recommend.test.tsx:283:33

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[14/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-015
AssertionError: 빈 200 body는 의미 있는 오류 문구로 바뀌어야 한다: expected [Function] to throw error including '요청에 실패했습니다.' but got 'Unexpected end of JSON input'

Expected: "요청에 실패했습니다."
Received: "Unexpected end of JSON input"

 ❯ src/test/FE05_api.test.ts:141:5
    139|     installFetch(async () => new Response("", { status: 200, headers: …
    140|     const api = await loadApi();
    141|     await expect(api.getOptions(), "빈 200 body는 의미 있는 오류 문구로 바뀌어야 한다")…
       |     ^
    142|   });
    143| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[15/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-016
AssertionError: 실제 URL https://host//api/options: expected 'https://host//api/options' not to contain '//api'

Expected: "//api"
Received: "https://host//api/options"

 ❯ src/test/FE05_api.test.ts:150:38
    148|     await api.getOptions();
    149|     const url = String(fetchMock.mock.calls[0][0]);
    150|     expect(url, `실제 URL ${url}`).not.toContain("//api");
       |                                      ^
    151|   });
    152| 

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[16/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-017
AssertionError: 실제 메시지에 토큰이 남아 있다: token=SECRET-TOKEN-123 failed: expected 'token=SECRET-TOKEN-123 failed' not to contain 'SECRET-TOKEN-123'

Expected: "SECRET-TOKEN-123"
Received: "token=SECRET-TOKEN-123 failed"

 ❯ src/test/FE05_api.test.ts:161:60
    159|     } catch (error) {
    160|       const message = error instanceof Error ? error.message : String(…
    161|       expect(message, `실제 메시지에 토큰이 남아 있다: ${message}`).not.toContain("…
       |                                                            ^
    162|     }
    163|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[17/18]⎯

 FAIL  src/test/FE05_api.test.ts > FE05 HTTP 클라이언트 > FE05-018
AssertionError: 실제 URL http://localhost:8080/api/diagnoses/1/../../: expected 'http://localhost:8080/api/diagnoses/1…' not to contain '/../'

Expected: "/../"
Received: "http://localhost:8080/api/diagnoses/1/../../"

 ❯ src/test/FE05_api.test.ts:170:38
    168|     await api.getDiagnosis("1/../../").catch(() => undefined);
    169|     const url = String(fetchMock.mock.calls[0][0]);
    170|     expect(url, `실제 URL ${url}`).not.toContain("/../");
       |                                      ^
    171|   });
    172| });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[18/18]⎯
- 재현 방법: npm test
- 원인 분석: 도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다.
- 수정 코드 위치: 아직 수정하지 않음
- 재검증: 아직 재검증하지 않음

### TC-UNIT-JAVA-001 Spring 진단·추천

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
- 테스트 종류: unit
- 검증 목적: JUnit 실행과 XML 재집계로 실패가 숨지 않는지 확인
- 도구 A: gradle / 결과 FAIL
- 도구 A 명령: `./gradlew test --console=plain`
- 도구 B: junit_audit / 결과 FAIL
- 도구 B 명령: `/private/tmp/qa-venv/bin/python qa/runner/tools/junit_audit.py /Users/jeong-yelim/orca/dasigolmok_v2`
- 최종 상태: FAIL
- 기대 결과: Gradle test 종료 0이고 JUnit XML 실패 0
- 실제 결과: A=FAIL, B=FAIL, final=FAIL
- 근거: A[FAIL] ionable tasks: 1 executed, 3 up-to-date

OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended

122 tests completed, 24 failed

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':test'.
> There were failing tests. See the report at: file:///Users/jeong-yelim/orca/dasigolmok_v2/back/build/reports/tests/test/index.html

* Try:
> Run with --scan to get full insights.

BUILD FAILED in 8s || B[FAIL] golmok.qa.Be03DiagnosisHttpTest.BE03-008,com.dasigolmok.qa.Be03DiagnosisHttpTest.BE03-010,com.dasigolmok.qa.Be03DiagnosisHttpTest.BE03-014,com.dasigolmok.qa.Be04RecommendHttpTest.BE04-016,com.dasigolmok.qa.Be04RecommendHttpTest.BE04-018,com.dasigolmok.qa.Be05AiClientTest.BE05-011,com.dasigolmok.qa.Be05AiClientTest.BE05-012,com.dasigolmok.qa.Be05AiClientTest.BE05-014,com.dasigolmok.qa.Be05AiClientTest.BE05-015,com.dasigolmok.qa.Be05AiClientTest.BE05-016,com.dasigolmok.qa.Be05AiClientTest.BE05-018
- 파일: UNKNOWN
- 함수: UNKNOWN
- 줄 번호: UNKNOWN
- ISSUE_ID: -
- RISK_ID: -
- 입력값: -
- 오류 메시지: =SA: (connection evicted)
2026-11-02T22:12:26.793+09:00 DEBUG 62703 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn34: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T22:12:26.793+09:00 DEBUG 62703 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn35: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T22:12:26.793+09:00 DEBUG 62703 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn36: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T22:12:26.793+09:00 DEBUG 62703 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn37: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T22:12:26.793+09:00 DEBUG 62703 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn38: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T22:12:26.793+09:00 DEBUG 62703 --- [nnection closer] com.zaxxer.hikari.pool.PoolBase          : HikariPool-4 - Closing connection conn39: url=jdbc:h2:mem:dasigolmok user=SA: (connection evicted)
2026-11-02T22:12:26.798+09:00 DEBUG 62703 --- [ionShutdownHook] com.zaxxer.hikari.pool.HikariPool        : HikariPool-4 - After shutdown stats (total=0, active=0, idle=0, waiting=0)
2026-11-02T22:12:26.799+09:00  INFO 62703 --- [ionShutdownHook] com.zaxxer.hikari.HikariDataSource       : HikariPool-4 - Shutdown completed.

> Task :test FAILED

Deprecated Gradle features were used in this build, making it incompatible with Gradle 9.0.

You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.

For more on this, please refer to https://docs.gradle.org/8.9/userguide/command_line_interface.html#sec:command_line_warnings in the Gradle documentation.
4 actionable tasks: 1 executed, 3 up-to-date

OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended

122 tests completed, 24 failed

FAILURE: Build failed with an exception.

* What went wrong:
Execution failed for task ':test'.
> There were failing tests. See the report at: file:///Users/jeong-yelim/orca/dasigolmok_v2/back/build/reports/tests/test/index.html

* Try:
> Run with --scan to get full insights.

BUILD FAILED in 8s
- 재현 방법: ./gradlew test --console=plain
- 원인 분석: 도구 출력을 확인한다. 코드는 기록 전에 수정하지 않는다.
- 수정 코드 위치: 아직 수정하지 않음
- 재검증: 아직 재검증하지 않음
