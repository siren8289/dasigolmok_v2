# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE02-001 | ZIP·CSV 인코딩·형식 | cp949 CSV | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE02-002 | ZIP·CSV 인코딩·형식 | UTF8 BOM CSV | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE02-003 | ZIP·CSV 인코딩·형식 | UTF8 일반 CSV | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE02-004 | ZIP·CSV 인코딩·형식 | 깨진 한글 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE02-005 | ZIP·CSV 인코딩·형식 | 빈 CSV | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE02-006 | ZIP·CSV 인코딩·형식 | CSV 헤더만 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE02-007 | ZIP·CSV 인코딩·형식 | ZIP 안 CSV 하나 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE02-008 | ZIP·CSV 인코딩·형식 | ZIP 안 CSV 여러개 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE02-010 | ZIP·CSV 인코딩·형식 | ZIP 폴더 포함 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE02-012 | ZIP·CSV 인코딩·형식 | CSV 쉼표 인용 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE02-013 | ZIP·CSV 인코딩·형식 | CSV 줄바꿈 인용 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |

## DE02-001 cp949 CSV
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: cp949 CSV의 동이 '연남동', 값은 1로 읽힘.

## DE02-002 UTF8 BOM CSV
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: utf-8-sig는 cp949에서 UnicodeDecodeError 후 utf-8-sig로 재시도. 결과 '연남동'.

## DE02-003 UTF8 일반 CSV
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: utf-8 CSV의 동이 '망원동' 1행.

## DE02-004 깨진 한글
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 잘못된 바이트는 RuntimeError 'CSV 글자 코드를 알 수 없습니다.'

## DE02-005 빈 CSV
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: raw=b''는 EmptyDataError로 파싱 실패가 전달됨. DataFrame을 만들지 않음.

## DE02-006 CSV 헤더만
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 헤더만 있는 CSV는 컬럼 [a,b], 행 0의 빈 DataFrame.

## DE02-007 ZIP 안 CSV 하나
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: zip 안 CSV 1개의 첫 파일을 읽어 연남동 1행.

## DE02-008 ZIP 안 CSV 여러개
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: first.csv, second.csv 중 namelist 첫 CSV '첫번째' 1행만 선택.

## DE02-010 ZIP 폴더 포함
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: reports/data.csv 경로의 CSV를 읽어 합정동 1행.

## DE02-012 CSV 쉼표 인용
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 인용 필드 '카페,음료'가 한 칸으로 보존. 컬럼 수 2.

## DE02-013 CSV 줄바꿈 인용
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 인용 필드 '두\n줄'이 1행 1셀로 보존.
