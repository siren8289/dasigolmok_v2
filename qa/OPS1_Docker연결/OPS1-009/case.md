# OPS1-009 AI 서비스명

| 항목 | 내용 |
| --- | --- |
| TC ID | OPS1-009 |
| 분야 | OPS1_Docker연결 |
| 세부 기능 | Docker Compose 4서비스 |
| 원자 검증 항목 | AI 서비스명 |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `compose.yaml` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/compose.yaml |

## 검증 목적

Docker Compose 4서비스에서 'AI 서비스명' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

Docker Compose 4서비스 모듈 준비; 입력 사례 'AI 서비스명'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

APP_AI_BASE_URL=http://ai:8000

## 실행 절차

1. APP_AI_BASE_URL=http://ai:8000 준비
2. Docker Compose 4서비스의 'AI 서비스명' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

back→ai DNS 성공

## 판정 기준

PASS: back→ai DNS 성공 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | back 환경변수 APP_AI_BASE_URL=http://ai:8000이고 compose 서비스 이름이 ai라 내부 DNS 대상이 맞다. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
