# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| FE02-001 | 진단 페이지 입력·셀렉트 | 기본 자치구 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-002 | 진단 페이지 입력·셀렉트 | 기본 행정동 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-003 | 진단 페이지 입력·셀렉트 | 기본 업종 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-004 | 진단 페이지 입력·셀렉트 | 옵션 목록 호출 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-005 | 진단 페이지 입력·셀렉트 | 마포구 옵션 존재 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-006 | 진단 페이지 입력·셀렉트 | 마포구 옵션 없음 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-008 | 진단 페이지 입력·셀렉트 | 자치구 변경 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-009 | 진단 페이지 입력·셀렉트 | 기존 동 미포함 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-010 | 진단 페이지 입력·셀렉트 | 기존 동 포함 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-011 | 진단 페이지 입력·셀렉트 | 동 선택 변경 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-012 | 진단 페이지 입력·셀렉트 | 업종 선택 변경 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-013 | 진단 페이지 입력·셀렉트 | 분석 버튼 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-014 | 진단 페이지 입력·셀렉트 | 분석 중 버튼 중복 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-015 | 진단 페이지 입력·셀렉트 | 분석 중 라벨 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-016 | 진단 페이지 입력·셀렉트 | 성공 결과 이동 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-017 | 진단 페이지 입력·셀렉트 | 전송 오류 메시지 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-018 | 진단 페이지 입력·셀렉트 | 비JSON 오류 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-019 | 진단 페이지 입력·셀렉트 | 요청 끝난 뒤 버튼 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-020 | 진단 페이지 입력·셀렉트 | 옵션 요청 실패 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-022 | 진단 페이지 입력·셀렉트 | 서로 다른 구·동 제출 방어 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-023 | 진단 페이지 입력·셀렉트 | 업종 미지원 값 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE02-024 | 진단 페이지 입력·셀렉트 | API 응답 순서 역전 | Vitest | RISK | Playwright | NOT_RUN | RISK |

## FE02-001 기본 자치구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 옵션 로드 후 자치구 값이 마포구다.

## FE02-002 기본 행정동
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 최초 행정동 값이 연남동이다.

## FE02-003 기본 업종
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 최초 업종 값이 한식음식점이다.

## FE02-004 옵션 목록 호출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: StrictMode 없이 마운트하면 GET /api/options 가 1회다.

## FE02-005 마포구 옵션 존재
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: districts에 마포구가 있으면 선택이 마포구로 유지된다.

## FE02-006 마포구 옵션 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마포구가 없으면 첫 자치구 강남구로 바뀐다.

## FE02-008 자치구 변경
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 강남구로 바꾸면 행정동 선택지가 역삼동·삼성동이다.

## FE02-009 기존 동 미포함
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 연남동은 강남구 목록에 없어 첫 동 역삼동으로 바뀐다.

## FE02-010 기존 동 포함
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마포구 목록에 망원동이 있으면 선택 후 첫 동으로 되돌리지 않는다.

## FE02-011 동 선택 변경
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 연남동에서 망원동으로 행정동 값이 바뀐다.

## FE02-012 업종 선택 변경
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 업종 값이 커피-음료로 바뀐다.

## FE02-013 분석 버튼
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST /api/diagnoses body에 district, dong, industry 세 필드가 실렸다.

## FE02-014 분석 중 버튼 중복
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 응답 대기 중 버튼이 disabled이고 POST는 1회만 나갔다.

## FE02-015 분석 중 라벨
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 대기 중 버튼 문구가 'AI가 분석하는 중...'이다.

## FE02-016 성공 결과 이동
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: id=12 응답 후 결과 화면(폐업률)이 같은 라우터의 /diagnoses/12 로 표시된다.

## FE02-017 전송 오류 메시지
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 404 JSON message가 화면에 그대로 표시된다.

## FE02-018 비JSON 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: HTML 500은 JSON 파싱에 실패해 기본 문구 '요청에 실패했습니다.'를 보여 준다.

## FE02-019 요청 끝난 뒤 버튼
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 오류로 Promise가 끝나면 버튼이 다시 '진단하기'이고 활성화된다.

## FE02-020 옵션 요청 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GET /api/options 503의 message '옵션 장애'가 표시된다.

## FE02-022 서로 다른 구·동 제출 방어
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마포구로 돌아오면 역삼동은 유지되지 않고 연남동으로 교정된 뒤 제출된다.

## FE02-023 업종 미지원 값
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: NOT_EXIST 제출 후 서버 message '지원하지 않는 업종입니다.'가 사용자에게 표시된다. 제출 전 별도 클라이언트 차단 문구는 없다.

## FE02-024 API 응답 순서 역전
- 상태: 검증A RISK / 검증B NOT_RUN / 최종 RISK
- 내용: 측정하지 못했거나 잠재 위험으로 남긴 항목이다.
- 실제: 옵션 도착 전 셀렉트 선택지가 현재 구 하나뿐이고, 응답 콜백은 요청 세대 가드 없이 setDistrict를 호출한다. 오래된 응답이 사용자 선택을 덮는 시나리오는 이 UI에서 재현되지 않았다.
