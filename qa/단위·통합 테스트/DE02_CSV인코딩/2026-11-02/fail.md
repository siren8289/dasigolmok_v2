# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE02-009 | ZIP·CSV 인코딩·형식 | ZIP 안 CSV 없음 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE02-011 | ZIP·CSV 인코딩·형식 | CSV 악성 수식 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE02-014 | ZIP·CSV 인코딩·형식 | 숫자 열 선행 0 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE02-015 | ZIP·CSV 인코딩·형식 | 빈 원본 ZIP | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE02-016 | ZIP·CSV 인코딩·형식 | zip 폭탄 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE02-017 | ZIP·CSV 인코딩·형식 | CSV 컬럼명 변동 | pytest | FAIL | fixture | NOT_RUN | FAIL |
| DE02-018 | ZIP·CSV 인코딩·형식 | 잘못된 파일 mime | pytest | FAIL | fixture | NOT_RUN | FAIL |

## DE02-009 ZIP 안 CSV 없음
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: StopIteration 오류 명확화
- 실제: txt만 있는 zip에서 StopIteration. CSV 없음에 대한 별도 메시지가 없음.
- 결함ID: DEF-DE02-009
- 코드: data/etl/fetch.py

## DE02-011 CSV 악성 수식
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 엑셀 수식 실행 우려, raw 값 데이터 처리
- 실제: 메모 셀이 '=HYPERLINK("http://evil")'로 남아 수식 원문이 그대로 저장됨.
- 결함ID: DEF-DE02-011
- 코드: data/etl/fetch.py

## DE02-014 숫자 열 선행 0
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 행정동 코드 선행 0 보존
- 실제: code '01100000'이 int 1100000으로 읽힘. 선행 0이 사라지고 dtype은 int64.
- 결함ID: DEF-DE02-014
- 코드: data/etl/fetch.py

## DE02-015 빈 원본 ZIP
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 명확한 오류
- 실제: 빈 zip은 StopIteration이고 예외 메시지가 빈 문자열이라 원인 안내가 없음.
- 결함ID: DEF-DE02-015
- 코드: data/etl/fetch.py

## DE02-016 zip 폭탄
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 최대 파일 크기 검증 필요
- 실제: 압축 해제 400006바이트 CSV를 상한 없이 100000행 DataFrame으로 읽음.
- 결함ID: DEF-DE02-016
- 코드: data/etl/fetch.py

## DE02-017 CSV 컬럼명 변동
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: 스키마 변화 감지·경고
- 실제: 헤더 폐업율 CSV를 경고 없이 읽음. columns=['기준_년분기_코드','행정동_코드','폐업율']. 폐업_률 스키마 경고 없음.
- 결함ID: DEF-DE02-017
- 코드: data/etl/fetch.py

## DE02-018 잘못된 파일 mime
- 검증A: pytest = FAIL
- 검증B: fixture = NOT_RUN
- 예상: CSV 대신 HTML 감지
- 실제: HTTP 200 text/html을 예외 없이 CSV로 읽음. HTML 감지 실패.
- 결함ID: DEF-DE02-018
- 코드: data/etl/fetch.py
