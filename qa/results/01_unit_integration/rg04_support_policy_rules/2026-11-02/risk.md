# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| RG04-001 | 지원정책 기간·적합성 | 모집 시작 전 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-002 | 지원정책 기간·적합성 | 모집 시작 당일 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-003 | 지원정책 기간·적합성 | 모집 중간 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-004 | 지원정책 기간·적합성 | 마감 당일 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-005 | 지원정책 기간·적합성 | 마감 다음날 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-006 | 지원정책 기간·적합성 | 과거 종료 지원 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-007 | 지원정책 기간·적합성 | 마감일 형식 오류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-008 | 지원정책 기간·적합성 | 시작일 형식 오류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-010 | 지원정책 기간·적합성 | 기준 날짜 없는 경우 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-011 | 지원정책 기간·적합성 | 종료 정책 only_open | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-012 | 지원정책 기간·적합성 | 종료 정책 포함 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-013 | 지원정책 기간·적합성 | 예정 정책 only_open | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-014 | 지원정책 기간·적합성 | 지역 전역 정책 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-015 | 지원정책 기간·적합성 | 지역 지정 정책 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-016 | 지원정책 기간·적합성 | 타구 정책 배제 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-017 | 지원정책 기간·적합성 | 업종 전역 정책 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-018 | 지원정책 기간·적합성 | 음식점 대상 정책 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-019 | 지원정책 기간·적합성 | 비대상 업종 정책 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-020 | 지원정책 기간·적합성 | 맞춤 구 점수 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-021 | 지원정책 기간·적합성 | 맞춤 업종 점수 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-022 | 지원정책 기간·적합성 | 키워드 일치 점수 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-023 | 지원정책 기간·적합성 | 정렬 기준 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-024 | 지원정책 기간·적합성 | top_k=1 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-025 | 지원정책 기간·적합성 | top_k=5 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| RG04-027 | 지원정책 기간·적합성 | top_k=0 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## RG04-001 모집 시작 전
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 기준일 2026-11-02, 시작 2026-12-01 은 upcoming, false 이다.

## RG04-002 모집 시작 당일
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 시작 당일 2026-11-02 는 open, true 이다.

## RG04-003 모집 중간
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 기간 중간 2026-11-02 는 open, true 이다.

## RG04-004 마감 당일
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마감 당일 2026-11-02 는 open, true 이다.

## RG04-005 마감 다음날
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마감 다음날 기준 2026-11-02, 종료 2026-11-01 은 closed, false 이다.

## RG04-006 과거 종료 지원
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 2024-06-30 종료 사업은 기준일 2026-11-02 에 closed, false 이다.

## RG04-007 마감일 형식 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마감일 형식 오류는 closed, false 이다.

## RG04-008 시작일 형식 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 시작일 형식 오류는 closed, false 이다.

## RG04-010 기준 날짜 없는 경우
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: target_date 가 없으면 시스템 오늘(2026-11-02)로 판정한다.

## RG04-011 종료 정책 only_open
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: only_open=True, 기준 2026-11-02 는 마감 공고를 제외한다.

## RG04-012 종료 정책 포함
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: only_open=False 는 마감 상태를 표기한 채 종료 공고를 포함한다.

## RG04-013 예정 정책 only_open
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: only_open=True 는 시작 전 예정 공고를 제외한다.

## RG04-014 지역 전역 정책
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 대상 지역이 없는 서울 전역 공고는 마포구 조회에 포함된다.

## RG04-015 지역 지정 정책
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마포구 지정 공고는 마포구 조회에 포함된다.

## RG04-016 타구 정책 배제
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 마포구 조회에서 강남구 공고는 제외된다.

## RG04-017 업종 전역 정책
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 업종 제한이 없는 공고는 한식음식점 조회에 포함된다.

## RG04-018 음식점 대상 정책
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 커피-음료는 마포 청년창업 대상 업종에 포함된다.

## RG04-019 비대상 업종 정책
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 학원은 마포 청년창업 대상 업종이 아니므로 제외된다.

## RG04-020 맞춤 구 점수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 자치구가 맞는 정책 점수는 전역 정책보다 0.5 높다.

## RG04-021 맞춤 업종 점수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 업종이 맞는 정책 점수는 전업종 정책보다 0.5 높다.

## RG04-022 키워드 일치 점수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 쿼리 토큰 1개 일치는 점수 0.3 을 더한다.

## RG04-023 정렬 기준
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 점수가 높은 자치구 맞춤 정책이 앞에 온다.

## RG04-024 top_k=1
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: top_k=1 은 정책 1건만 반환한다.

## RG04-025 top_k=5
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: top_k=5 는 5건 이하다.

## RG04-027 top_k=0
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: top_k=0 은 빈 배열이다.
