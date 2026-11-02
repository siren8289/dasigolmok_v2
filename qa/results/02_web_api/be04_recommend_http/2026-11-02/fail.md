# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE04-016 | 옵션·추천 HTTP | API 메서드 방어 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |
| BE04-018 | 옵션·추천 HTTP | 지역·동 일치 | JUnit | FAIL | MockMvc | NOT_RUN | FAIL |

## BE04-016 API 메서드 방어
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 405
- 실제: GET /api/recommendations는 405가 아니라 500 INTERNAL_ERROR. body errorCode=INTERNAL_ERROR.
- 결함ID: DEF-BE04-016
- 코드: back/src/main/java/com/dasigolmok/recommend/controller/RecommendController.java

## BE04-018 지역·동 일치
- 검증A: JUnit = FAIL
- 검증B: MockMvc = NOT_RUN
- 예상: 교차 지역 추천을 방지하는 검증 필요
- 실제: 마포구+역삼동 POST /api/recommendations가 400이 아니라 200. body dong=역삼동, recommendations=[]. 교차 지역 검증 없음.
- 결함ID: DEF-BE04-018
- 코드: back/src/main/java/com/dasigolmok/recommend/controller/RecommendController.java
