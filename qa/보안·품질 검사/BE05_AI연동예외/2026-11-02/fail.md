# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE05-011 | RestTemplate 연동·오류 | AI 404 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE05-012 | RestTemplate 연동·오류 | AI 422 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE05-014 | RestTemplate 연동·오류 | AI 빈 JSON | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE05-015 | RestTemplate 연동·오류 | AI HTML 응답 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE05-016 | RestTemplate 연동·오류 | 재시도 여부 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE05-018 | RestTemplate 연동·오류 | AI 잘못된 주소 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE05-019 | RestTemplate 연동·오류 | 비밀 값 마스킹 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |

## BE05-011 AI 404
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 의도된 Spring 에러코드로 변환·구분
- 실제: AI HTTP 404와 HTTP 500이 모두 ApiException errorCode=AI_ERROR, status 502. 404 전용 코드로 구분되지 않음.
- 결함ID: DEF-BE05-011
- 코드: back/src/main/java/com/dasigolmok/ai/AiClient.java

## BE05-012 AI 422
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 요청 validation 원인 재해석 가능
- 실제: AI HTTP 422 body의 field required/industry가 사용자 메시지에 없음. 관측 message=AI 서버 호출에 실패했습니다. code=AI_ERROR.
- 결함ID: DEF-BE05-012
- 코드: back/src/main/java/com/dasigolmok/ai/AiClient.java

## BE05-014 AI 빈 JSON
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 핵심 필드 누락을 감지해야 한다
- 실제: diagnose에 {}를 주면 예외 없이 그 JsonNode를 반환. status/close_rate 등 핵심 필드 누락을 감지하지 않음.
- 결함ID: DEF-BE05-014
- 코드: back/src/main/java/com/dasigolmok/ai/AiClient.java

## BE05-015 AI HTML 응답
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: JSON 역직렬화 실패 안내
- 실제: content-type text/html(UnknownContentTypeException)의 안내가 JSON 역직렬화 실패가 아니라 message=AI 서버 호출에 실패했습니다.
- 결함ID: DEF-BE05-015
- 코드: back/src/main/java/com/dasigolmok/ai/AiClient.java

## BE05-016 재시도 여부
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 서비스 정책에 맞는 재시도/타임아웃 확인
- 실제: HTTP 503에서 RestTemplate.postForObject가 1회만 호출되고 ApiException으로 종료. 재시도 0.
- 결함ID: DEF-BE05-016
- 코드: back/src/main/java/com/dasigolmok/ai/AiClient.java

## BE05-018 AI 잘못된 주소
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 설정 오류 로그·안내
- 실제: baseUrl=https://wrong 실패 시 message=AI 서버 호출에 실패했습니다. 로그는 API error와 UnknownHost 스택뿐이고 설정/base-url 안내는 없음.
- 결함ID: DEF-BE05-018
- 코드: back/src/main/java/com/dasigolmok/ai/AiClient.java

## BE05-019 비밀 값 마스킹
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 환경변수·DB_PASSWORD 노출 없음
- 실제: 응답 JSON에는 DB_PASSWORD가 없으나 GlobalExceptionHandler ERROR 로그 cause에 RestClientException: upstream failed DB_PASSWORD=supersecret이 남음.
- 결함ID: DEF-BE05-019
- 코드: back/src/main/java/com/dasigolmok/ai/AiClient.java
