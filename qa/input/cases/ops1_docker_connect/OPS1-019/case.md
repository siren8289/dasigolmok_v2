# OPS1-019 V1~V9 initdb

| 항목 | 내용 |
| --- | --- |
| TC ID | OPS1-019 |
| 분야 | OPS1_Docker연결 |
| 세부 기능 | Docker Compose 4서비스 |
| 원자 검증 항목 | V1~V9 initdb |
| 우선순위 | P1 |
| 테스트 구분 | 정상/규칙 |
| 근거 분류 | 구현기반 |
| 추천 도구 | Docker/SQL/워크플로 검증 |
| 관련 코드 경로 | `compose.yaml` |
| GitHub 코드 URL | https://github.com/siren8289/dasigolmok_v2/blob/main/compose.yaml |

## 검증 목적

Docker Compose 4서비스에서 'V1~V9 initdb' 단일 조건을 검증하여 입력·처리·출력·예외가 일치하는지 확인

## 사전조건

Docker Compose 4서비스 모듈 준비; 입력 사례 'V1~V9 initdb'에 필요한 fixture/mock 구성; 외부 API는 테스트 더블 사용

## 테스트 입력값

./db/migration mount

## 실행 절차

1. ./db/migration mount 준비
2. Docker Compose 4서비스의 'V1~V9 initdb' 조건 실행
3. 반환값·상태코드·로그·부수효과를 기대결과와 비교

## 기대 결과

신규 데이터 볼륨 초기화가 성공해야 한다

## 판정 기준

PASS: 신규 데이터 볼륨 초기화가 성공해야 한다 관찰 및 예상치 밖 부작용 없음
FAIL: 예상 불일치·예외 누락·데이터 오염
RISK: 검증 불가/정책 미정/잠재 위험

## 실행 기록

| 열 | 값 |
| --- | --- |
| 실행 상태 (O) | PASS |
| 실제 결과/증적 (P) | db/migration 9개 SQL이 /docker-entrypoint-initdb.d 읽기전용 마운트다: V1__init_schema.sql, V2__seed_data.sql, V3__efficiency_optimization.sql, V4__mock_data_extended.sql, V5__area_context_external.sql, V6__analytics_star_schema.sql, V7__ai_adapter_scaffold.sql, V8__story_optimistic_lock.sql, V9__commercial_rag_pgvector.sql. |
| 결함 ID (Q) | — |

## 비고/근거

현재 코드에 있는 함수·라우트·규칙 기준
