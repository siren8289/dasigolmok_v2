# BE01-023 지역·동 불일치

| 항목 | 내용 |
| --- | --- |
| TC ID | BE01-023 |
| 분야 | BE01_진단요청DTO |
| 세부 기능 | 진단 DTO 유효성 |
| 원자 검증 항목 | 지역·동 불일치 |
| 우선순위 | P0 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | JUnit/MockMvc + DB검증 |
| 관련 코드 경로 | `back/src/main/java/com/dasigolmok/diagnosis/dto/DiagnosisRequest.java` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/back/src/main/java/com/dasigolmok/diagnosis/dto/DiagnosisRequest.java |

## 검증 목적

진단 DTO 유효성에서 '지역·동 불일치' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

진단 DTO 유효성 모듈 준비; 입력 사례 '지역·동 불일치'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

마포구/역삼동

## 실행 절차

1. 마포구/역삼동 준비
2. 진단 DTO 유효성의 '지역·동 불일치' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

상위 계층에서 조합 검증 필요

## 판정 기준

PASS: 상위 계층에서 조합 검증 필요 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | 마포구/역삼동 POST가 400이 아니라 201. 응답 district=마포구, dong=역삼동으로 저장됨. 지역·동 조합 검증 없음. |
| 결함 ID (Q) | DEF-BE01-023 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
