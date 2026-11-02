# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| FE01-001 | React 라우팅·공통 UX | 루트 진입 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-002 | React 라우팅·공통 UX | 추천 경로 진입 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-003 | React 라우팅·공통 UX | 진단 결과 경로 진입 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-004 | React 라우팅·공통 UX | 네비게이션 진단 링크 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-005 | React 라우팅·공통 UX | 네비게이션 추천 링크 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-006 | React 라우팅·공통 UX | 뒤로가기 라우팅 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-007 | React 라우팅·공통 UX | 새로고침 딥링크 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-009 | React 라우팅·공통 UX | 반응형 좁은 화면 | Vitest | RISK | Playwright | NOT_RUN | RISK |
| FE01-010 | React 라우팅·공통 UX | 키보드 탭 이동 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-011 | React 라우팅·공통 UX | 타이틀/랜드마크 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-012 | React 라우팅·공통 UX | 초기 로딩 상태 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-013 | React 라우팅·공통 UX | 링크 직접 키보드 활성화 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-014 | React 라우팅·공통 UX | 브라우저 새 탭 링크 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-015 | React 라우팅·공통 UX | 모바일 320px | Vitest | RISK | Playwright | NOT_RUN | RISK |
| FE01-016 | React 라우팅·공통 UX | URL query 보존 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |
| FE01-017 | React 라우팅·공통 UX | 기존 새 화면 영향 | Vitest | PASS | Playwright | NOT_RUN | NOT_RUN |

## FE01-001 루트 진입
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GET / 렌더에서 heading '골목 상권 진단'과 자치구·행정동·업종 셀렉트가 보인다.

## FE01-002 추천 경로 진입
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: GET /recommend 에서 heading '업종 추천'이 렌더된다.

## FE01-003 진단 결과 경로 진입
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 경로 /diagnoses/1 이 GET /api/diagnoses/1 을 호출한다.

## FE01-004 네비게이션 진단 링크
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 상단 '골목 상권 진단' 링크 클릭 후 진단 화면 heading이 돌아온다.

## FE01-005 네비게이션 추천 링크
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 상단 '업종 추천' 클릭 후 /recommend 화면이 표시된다.

## FE01-006 뒤로가기 라우팅
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 진단 화면에서 추천으로 이동한 뒤 window.history.back() 으로 진단 화면과 이전 주소가 복원된다.

## FE01-007 새로고침 딥링크
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: front/nginx.conf location / 에 try_files $uri $uri/ /index.html history fallback이 있다. 라이브 Nginx 재시작은 이 단위 실행에 포함하지 않았다.

## FE01-009 반응형 좁은 화면
- 상태: 검증A RISK / 검증B NOT_RUN / 최종 RISK
- 내용: 측정하지 못했거나 잠재 위험으로 남긴 항목이다.
- 실제: jsdom은 375px 뷰포트의 가로 잘림(scrollWidth)을 계산하지 않아 탭·셀렉트 overflow를 실행 측정할 수 없음

## FE01-010 키보드 탭 이동
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: Tab 이동으로 포커스가 바뀐 요소: A:골목 상권 진단 | A:업종 추천 | SELECT:강남구마포구 | SELECT:연남동망원동 | SELECT:한식음식점커피-음료 | BUTTON:진단하기 | BODY:dasiGolmok골목 상권 진단업종

## FE01-011 타이틀/랜드마크
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: header/main 랜드마크와 브랜드 텍스트, 진단 heading이 있다. document title은 index.html의 'dasiGolmok - 서울 골목 상권 진단'이다.

## FE01-012 초기 로딩 상태
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 옵션 목 응답으로 첫 렌더 후 header/main/heading이 있고 console.error가 비어 있다.

## FE01-013 링크 직접 키보드 활성화
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 업종 추천 링크에 포커스한 뒤 Enter로 추천 화면에 진입했다.

## FE01-014 브라우저 새 탭 링크
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 상단 메뉴는 href가 있는 <a>라 중클릭·새 탭으로 주소가 독립적으로 열린다.

## FE01-015 모바일 320px
- 상태: 검증A RISK / 검증B NOT_RUN / 최종 RISK
- 내용: 측정하지 못했거나 잠재 위험으로 남긴 항목이다.
- 실제: jsdom은 320px에서 실제 글자 폭과 가로 스크롤을 계산하지 않아 가독성·잘림을 실행 측정할 수 없음

## FE01-016 URL query 보존
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: /recommend?utm=qa 진입 시 추천 화면이 렌더되고 console.error가 없다. 쿼리는 라우트가 제거하지 않는다.

## FE01-017 기존 새 화면 영향
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: App 라우트는 / 와 /recommend 두 화면을 그대로 렌더한다. RAG API는 이 두 라우트를 바꾸지 않는다.
