# FE01-011 타이틀/랜드마크

| 항목 | 내용 |
| --- | --- |
| TC ID | FE01-011 |
| 분야 | FE01_공통라우팅 |
| 세부 기능 | React 라우팅·공통 UX |
| 원자 검증 항목 | 타이틀/랜드마크 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Vitest/Playwright + 네트워크 검증 |
| 관련 코드 경로 | `front/src/App.tsx` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/front/src/App.tsx |

## 검증 목적

React 라우팅·공통 UX에서 '타이틀/랜드마크' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

React 라우팅·공통 UX 모듈 준비; 입력 사례 '타이틀/랜드마크'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

헤더/main DOM

## 실행 절차

1. 헤더/main DOM 준비
2. React 라우팅·공통 UX의 '타이틀/랜드마크' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

header/main 의미 구조와 제목 노출이 유지된다

## 판정 기준

PASS: header/main 의미 구조와 제목 노출이 유지된다 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | header/main 랜드마크와 브랜드 텍스트, 진단 heading이 있다. document title은 index.html의 'dasiGolmok - 서울 골목 상권 진단'이다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
