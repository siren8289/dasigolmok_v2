# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DE01-001 | 소상공인 API·서울시 수집 | 인증키 없음 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-002 | 소상공인 API·서울시 수집 | SEMAS 정상 resultCode | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-003 | 소상공인 API·서울시 수집 | SEMAS 성공 코드 0 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-004 | 소상공인 API·서울시 수집 | SEMAS 성공 코드 000 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-005 | 소상공인 API·서울시 수집 | SEMAS 오류 코드 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-006 | 소상공인 API·서울시 수집 | SEMAS 타임아웃 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-007 | 소상공인 API·서울시 수집 | SEMAS HTTP 500 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-008 | 소상공인 API·서울시 수집 | 대분류와 중분류 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-009 | 소상공인 API·서울시 수집 | 자치구 목록 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-010 | 소상공인 API·서울시 수집 | 업소 샘플 페이지 1 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-011 | 소상공인 API·서울시 수집 | 업소 샘플 페이지 3 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-012 | 소상공인 API·서울시 수집 | 업소 totalCount 미달 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-013 | 소상공인 API·서울시 수집 | 업소 목록 빈 페이지 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-014 | 소상공인 API·서울시 수집 | 업소 전체 건수 충족 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-015 | 소상공인 API·서울시 수집 | 업소 max_pages=0 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-017 | 소상공인 API·서울시 수집 | 비정상 JSON | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-019 | 소상공인 API·서울시 수집 | 서울시 ZIP 다운로드 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-020 | 소상공인 API·서울시 수집 | 서울시 Sheet 다운로드 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-022 | 소상공인 API·서울시 수집 | 다운로드 timeout | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-023 | 소상공인 API·서울시 수집 | 서울시 표 연도 병합 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-024 | 소상공인 API·서울시 수집 | 없는 SEOUL_FILES key | pytest | PASS | fixture | NOT_RUN | NOT_RUN |
| DE01-025 | 소상공인 API·서울시 수집 | 서울 외 데이터 | pytest | PASS | fixture | NOT_RUN | NOT_RUN |

## DE01-001 인증키 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: SERVICE_KEY=''에서 semas_get이 RuntimeError. 메시지에 DATA_GO_KR_KEY 안내가 있음.

## DE01-002 SEMAS 정상 resultCode
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: resultCode '00' 응답을 JSON으로 파싱. items=[{indsLclsCd:'Q'}] 1건.

## DE01-003 SEMAS 성공 코드 0
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: resultCode '0'을 성공으로 허용. items ok=1 반환.

## DE01-004 SEMAS 성공 코드 000
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: resultCode '000'을 성공으로 허용. items ok=1 반환.

## DE01-005 SEMAS 오류 코드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: resultCode '03'은 RuntimeError. 예외 문자열에 03이 포함됨.

## DE01-006 SEMAS 타임아웃
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: requests.get timeout=30. Timeout 예외가 삼켜지지 않고 전파됨.

## DE01-007 SEMAS HTTP 500
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: HTTP 500에서 raise_for_status가 HTTPError '500 Server Error'를 전파.

## DE01-008 대분류와 중분류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: fetch_semas_upjong이 대분류 [음식], 중분류 [한식] 두 목록을 반환. API 호출 2회.

## DE01-009 자치구 목록
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: fetch_semas_dongs 파라미터 ctprvnCd='11'. 반환 1건 ctyNm=마포구.

## DE01-010 업소 샘플 페이지 1
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: max_pages=1, total=999여도 pageNo=[1]만 호출. 수집 행 1.

## DE01-011 업소 샘플 페이지 3
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: max_pages=3, total=999이면 pageNo=[1,2,3]. 수집 행 3.

## DE01-012 업소 totalCount 미달
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 페이지당 1건, total=5. pageNo 1,2,3으로 늘어나 누적 3건.

## DE01-013 업소 목록 빈 페이지
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: items=[]이면 1페이지만 호출하고 [] 반환 후 루프 종료.

## DE01-014 업소 전체 건수 충족
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 1페이지 2건, total=2. pageNo=[1]에서 종료. 행 2.

## DE01-015 업소 max_pages=0
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: max_pages=0이면 [] 반환. requests.get 호출 0회.

## DE01-017 비정상 JSON
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: HTTP 200 HTML 본문은 JSONDecodeError. 디코딩 실패가 전파됨.

## DE01-019 서울시 ZIP 다운로드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: zip 안 cp949 CSV를 DataFrame으로 반환. 연남동 1행.

## DE01-020 서울시 Sheet 다운로드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 시트 CSV를 DataFrame으로 반환. 망원동 1행.

## DE01-022 다운로드 timeout
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: download_seoul_zip의 requests.post timeout=120. Timeout이 전파됨.

## DE01-023 서울시 표 연도 병합
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: zip 연도 seq 5 다음 6. 결합 year_seq=[5,6]으로 순서 유지.

## DE01-024 없는 SEOUL_FILES key
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: fetch_seoul_table('wrong')은 KeyError. 메시지에 wrong이 있음.

## DE01-025 서울 외 데이터
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 11440740은 마포구 1행만 남고 부산 26110510은 0건.
