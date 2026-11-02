# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE01-016 | 소상공인 API·서울시 수집 | 외부 API 429 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE01-018 | 소상공인 API·서울시 수집 | 인증키 로그 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE01-021 | 소상공인 API·서울시 수집 | 서울시 ZIP 손상 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE01-026 | 소상공인 API·서울시 수집 | 응답 URL 변경 | pytest | FAIL | fixture | NOT_RUN | FAIL |

## DE01-016 외부 API 429
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 재시도/속도제한 정책 검증
- 실제: status=429 응답 1회에서 HTTPError '429 Server Error'. 재시도 없이 종료되어 이후 200 응답은 호출되지 않음.
- 결함ID: DEF-DE01-016
- 코드: data/etl/fetch.py

## DE01-018 인증키 로그
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 로그에서 키 마스킹
- 실제: resultCode 03 헤더에 키가 있으면 로그에 LEAKEDKEY123456789가 평문으로 출력됨. 마스킹 없음. _try_semas는 빈 목록으로 계속 진행.
- 결함ID: DEF-DE01-018
- 코드: data/etl/fetch.py

## DE01-021 서울시 ZIP 손상
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 예외와 재수집 안내
- 실제: 손상 바이너리에 BadZipFile 'File is not a zip file'만 발생. 예외 메시지에 재수집 안내가 없음.
- 결함ID: DEF-DE01-021
- 코드: data/etl/fetch.py

## DE01-026 응답 URL 변경
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 실제 파일 타입 검증
- 실제: HTTP 200 HTML 본문을 파일 타입 검사 없이 Zip 파싱. 메시지는 'File is not a zip file'이고 '파일/타입/형식' 검증 문구가 없음.
- 결함ID: DEF-DE01-026
- 코드: data/etl/fetch.py
