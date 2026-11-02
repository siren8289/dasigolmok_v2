# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| FE04-001 | 업종 추천 화면 | 기본 지역 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-002 | 업종 추천 화면 | 옵션 목록 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-003 | 업종 추천 화면 | 자치구 선택 교체 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-004 | 업종 추천 화면 | 동 일치 검사 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-005 | 업종 추천 화면 | 기존 동 유지 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-006 | 업종 추천 화면 | 추천 버튼 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-007 | 업종 추천 화면 | 추천 버튼 로딩 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-008 | 업종 추천 화면 | 추천 결과 표출 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-010 | 업종 추천 화면 | 추천 결과 상태 안정 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-011 | 업종 추천 화면 | 추천 결과 상태 주의 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-012 | 업종 추천 화면 | 추천 결과 상태 위험 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-013 | 업종 추천 화면 | 추천 결과 미지정 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-014 | 업종 추천 화면 | 추천 수치 단위 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-015 | 업종 추천 화면 | 매출 수치 단위 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-016 | 업종 추천 화면 | 상권변화 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-017 | 업종 추천 화면 | 추천 서버 오류 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-018 | 업종 추천 화면 | 추천 중복 클릭 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-019 | 업종 추천 화면 | 추천 재요청 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE04-022 | 업종 추천 화면 | 모바일 테이블 | Vitest | RISK | Playwright | NOT_RUN | RISK |
| FE04-024 | 업종 추천 화면 | 옵션 실패 후 추천 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |

## FE04-001 기본 지역
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 첫 진입 기본값은 마포구/연남동이다.

## FE04-002 옵션 목록
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마운트 시 GET /api/options 가 호출된다.

## FE04-003 자치구 선택 교체
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 강남구 선택 후 동 목록이 역삼동·삼성동으로 다시 계산된다.

## FE04-004 동 일치 검사
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 기존 연남동이 새 구에 없으면 첫 행정동 역삼동으로 바뀐다.

## FE04-005 기존 동 유지
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 현재 동이 마포구 목록에 있으면 망원동 선택을 유지한다.

## FE04-006 추천 버튼
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST /api/recommendations 에 마포구/연남동이 전송된다.

## FE04-007 추천 버튼 로딩
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 지연 중 버튼이 disabled이고 문구는 '업종을 계산하는 중...'이다.

## FE04-008 추천 결과 표출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: all_industries 3개가 헤더 1행 + 본문 3행으로 표시된다.

## FE04-010 추천 결과 상태 안정
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=stable 행에 안정 뱃지가 있다.

## FE04-011 추천 결과 상태 주의
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=warning 행에 주의 뱃지가 있다.

## FE04-012 추천 결과 상태 위험
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=danger 행에 위험 뱃지가 있다.

## FE04-013 추천 결과 미지정
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=OTHER 는 판단 불가 뱃지로 떨어진다.

## FE04-014 추천 수치 단위
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ml_close_rate 4.2가 '4.2%'로 표시된다.

## FE04-015 매출 수치 단위
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dl_sales_per_store 620.1이 '620.1만원'으로 표시된다.

## FE04-016 상권변화
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 결과 헤더에 행정동과 상권변화명이 함께 있다.

## FE04-017 추천 서버 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 500 message가 화면에 표시된다.

## FE04-018 추천 중복 클릭
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 느린 응답 동안 두 번째 클릭은 막혀 POST가 1회다.

## FE04-019 추천 재요청
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 지역을 바꾼 뒤 다시 누르면 최신 역삼동 결과로 헤더가 바뀐다.

## FE04-022 모바일 테이블
- 상태: 검증A RISK / 검증B NOT_RUN / 최종 RISK
- 내용: 측정하지 못했거나 잠재 위험으로 남긴 항목이다.
- 실제: jsdom은 375px에서 30자 업종명의 테이블 가로 overflow를 계산하지 못한다

## FE04-024 옵션 실패 후 추천
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 옵션 503 안내 뒤에도 기본값 마포구/연남동은 유효해 추천 POST가 나가고 결과가 교체된다.
