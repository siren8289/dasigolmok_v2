# OPS1-024 컨테이너 메모리

| 항목 | 내용 |
| --- | --- |
| TC ID | OPS1-024 |
| 분야 | OPS1_Docker연결 |
| 세부 기능 | Docker Compose 4서비스 |
| 원자 검증 항목 | 컨테이너 메모리 |
| 우선순위 | P1 |
| 테스트 구분 | 검증 |
| 근거 분류 | 개선제안 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `compose.yaml` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/compose.yaml |

## 검증 목적

Docker Compose 4서비스에서 '컨테이너 메모리' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

Docker Compose 4서비스 모듈 준비; 입력 사례 '컨테이너 메모리'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

AI torch+모델

## 실행 절차

1. AI torch+모델 준비
2. Docker Compose 4서비스의 '컨테이너 메모리' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

메모리 상한/압박 측정

## 판정 기준

PASS: 메모리 상한/압박 측정 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | FAIL |
| 실제 결과/증적 (P) | compose.yaml와 config 어디에도 AI/서비스 메모리 상한(mem_limit, deploy.resources)이 없다. |
| 결함 ID (Q) | DEF-OPS1-024 |

## 비고/근거

개선제안/방어 테스트: 아직 구현된 보장이라고 단정하지 않음
