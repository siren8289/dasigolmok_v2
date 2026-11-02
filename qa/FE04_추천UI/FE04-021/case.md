# FE04-021 추천 상위 5와 전체 목록 차이

| 항목 | 내용 |
| --- | --- |
| TC ID | FE04-021 |
| 분야 | FE04_추천UI |
| 세부 기능 | 업종 추천 화면 |
| 원자 검증 항목 | 추천 상위 5와 전체 목록 차이 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Vitest/Playwright + 네트워크 검증 |
| 관련 코드 경로 | `front/src/pages/RecommendPage.tsx` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/front/src/pages/RecommendPage.tsx |

## 검증 목적

업종 추천 화면에서 '추천 상위 5와 전체 목록 차이' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

업종 추천 화면 모듈 준비; 입력 사례 '추천 상위 5와 전체 목록 차이'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

recommendations 5개, all_industries 10개

## 실행 절차

1. recommendations 5개, all_industries 10개 준비
2. 업종 추천 화면의 '추천 상위 5와 전체 목록 차이' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

전체 표가 10개 렌더링되고 상위 추천 표시 여부 점검

## 판정 기준

PASS: 전체 표가 10개 렌더링되고 상위 추천 표시 여부 점검 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | 10행은 렌더되지만 recommendations 5개를 구분하는 상위 추천 표시가 없다: expected null not to be null |
| 결함 ID (Q) | DEF-FE04-021 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
