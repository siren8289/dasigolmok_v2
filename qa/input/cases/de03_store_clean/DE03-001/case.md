# DE03-001 공통 key 추출

| 항목 | 내용 |
| --- | --- |
| TC ID | DE03-001 |
| 분야 | DE03_점포정제 |
| 세부 기능 | 점포 통계 clean_store |
| 원자 검증 항목 | 공통 key 추출 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/fixture + CSV검증 |
| 관련 코드 경로 | `data/etl/transform.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/data/etl/transform.py |

## 검증 목적

점포 통계 clean_store에서 '공통 key 추출' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

점포 통계 clean_store 모듈 준비; 입력 사례 '공통 key 추출'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

quarter/dong_code/industry_code

## 실행 절차

1. quarter/dong_code/industry_code 준비
2. 점포 통계 clean_store의 '공통 key 추출' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

영문 key 통일

## 판정 기준

PASS: 영문 key 통일 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 공통 키가 quarter=20242, dong_code=11440740, industry_code=CS100001. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
