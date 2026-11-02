# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| FE03-001 | 진단 결과 렌더링 | 결과 API 조회 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-002 | 진단 결과 렌더링 | 조회 대기 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-003 | 진단 결과 렌더링 | 조회 실패 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-004 | 진단 결과 렌더링 | 구·동·업종 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-005 | 진단 결과 렌더링 | 최근 폐업률 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-006 | 진단 결과 렌더링 | 상태 안정 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-007 | 진단 결과 렌더링 | 상태 주의 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-008 | 진단 결과 렌더링 | 상태 위험 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-009 | 진단 결과 렌더링 | 상태 미지정 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-010 | 진단 결과 렌더링 | 모르는 상태 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-011 | 진단 결과 렌더링 | 상권변화명 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-012 | 진단 결과 렌더링 | ML 예상 폐업률 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-013 | 진단 결과 렌더링 | DL 예상 매출 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-014 | 진단 결과 렌더링 | 점포 수 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-015 | 진단 결과 렌더링 | 개업률 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-016 | 진단 결과 렌더링 | 유동인구 반올림 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-017 | 진단 결과 렌더링 | 설명 기본 출처 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-018 | 진단 결과 렌더링 | 설명 Gemini 출처 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-019 | 진단 결과 렌더링 | 줄바꿈 유지 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-020 | 진단 결과 렌더링 | 다시 분석 링크 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-023 | 진단 결과 렌더링 | 악의적 설명 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE03-024 | 진단 결과 렌더링 | 빈 설명 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |

## FE03-001 결과 API 조회
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GET /api/diagnoses/12 가 호출된다.

## FE03-002 조회 대기
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 미응답 동안 '불러오는 중...'이 보인다.

## FE03-003 조회 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 404 message가 오류 문장으로 표시된다.

## FE03-004 구·동·업종
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 상단에 마포구, 연남동, 한식음식점이 한 줄에 있다.

## FE03-005 최근 폐업률
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: '폐업률 5.6%' 문자열이 있다.

## FE03-006 상태 안정
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: stable 칩 문구는 안정이고 emerald 클래스가 붙는다.

## FE03-007 상태 주의
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: warning 칩 문구는 주의이고 amber 클래스가 붙는다.

## FE03-008 상태 위험
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: danger 칩 문구는 위험이고 red 클래스가 붙는다.

## FE03-009 상태 미지정
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: unknown 칩 문구는 판단 불가다.

## FE03-010 모르는 상태
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 알 수 없는 status=weird 는 unknown 스타일·판단 불가로 떨어진다.

## FE03-011 상권변화명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 상태 칩 텍스트에 상권축소가 포함된다.

## FE03-012 ML 예상 폐업률
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ML 예상 폐업률 7.34%가 표시된다.

## FE03-013 DL 예상 매출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: DL 예상 매출 650.2만원이 표시된다.

## FE03-014 점포 수
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: '점포 30개'가 표시된다.

## FE03-015 개업률
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: '개업률 2.1%'가 표시된다.

## FE03-016 유동인구 반올림
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: Math.round(1099.9) 후 toLocaleString으로 유동인구 1,100명이다.

## FE03-017 설명 기본 출처
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: explanationSource=basic 이면 '기본 문장'이 보인다.

## FE03-018 설명 Gemini 출처
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: explanationSource=gemini 이면 'Gemini'가 보인다.

## FE03-019 줄바꿈 유지
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 설명 노드에 whitespace-pre-line 이 있고 두 줄 텍스트가 유지된다.

## FE03-020 다시 분석 링크
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: '다시 진단하기' 링크가 / 화면으로 이동한다.

## FE03-023 악의적 설명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 설명의 HTML/script는 텍스트로만 보이고 script·img 요소는 만들어지지 않는다.

## FE03-024 빈 설명
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 빈 설명이어도 폐업률과 출처 라벨이 남고 예외가 없다.
