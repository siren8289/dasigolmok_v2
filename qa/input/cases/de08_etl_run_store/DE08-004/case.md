# DE08-004 SEMAS API 실패

| 항목 | 내용 |
| --- | --- |
| TC ID | DE08-004 |
| 분야 | DE08_ETL실행저장 |
| 세부 기능 | 데이터 수집→전처리→아티팩트 |
| 원자 검증 항목 | SEMAS API 실패 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | pytest/fixture + CSV검증 |
| 관련 코드 경로 | `data/etl/run.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/data/etl/run.py |

## 검증 목적

데이터 수집→전처리→아티팩트에서 'SEMAS API 실패' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

데이터 수집→전처리→아티팩트 모듈 준비; 입력 사례 'SEMAS API 실패'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

_try_semas raises

## 실행 절차

1. _try_semas raises 준비
2. 데이터 수집→전처리→아티팩트의 'SEMAS API 실패' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

빈 옵션 보조자료로 진행

## 판정 기준

PASS: 빈 옵션 보조자료로 진행 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | 업종 API RuntimeError 후 '건너뜁니다'. semas_dong_count=0, semas_upjong_count=0, [3/3] 저장까지 진행. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
