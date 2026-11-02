# DE02-009 ZIP 안 CSV 없음

| 항목 | 내용 |
| --- | --- |
| TC ID | DE02-009 |
| 분야 | DE02_CSV인코딩 |
| 세부 기능 | ZIP·CSV 인코딩·형식 |
| 원자 검증 항목 | ZIP 안 CSV 없음 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | pytest/fixture + CSV검증 |
| 관련 코드 경로 | `data/etl/fetch.py` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/data/etl/fetch.py |

## 검증 목적

ZIP·CSV 인코딩·형식에서 'ZIP 안 CSV 없음' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

ZIP·CSV 인코딩·형식 모듈 준비; 입력 사례 'ZIP 안 CSV 없음'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

archive contains txt

## 실행 절차

1. archive contains txt 준비
2. ZIP·CSV 인코딩·형식의 'ZIP 안 CSV 없음' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

StopIteration 오류 명확화

## 판정 기준

PASS: StopIteration 오류 명확화 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | txt만 있는 zip에서 StopIteration. CSV 없음에 대한 별도 메시지가 없음. |
| 결함 ID (Q) | DEF-DE02-009 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
