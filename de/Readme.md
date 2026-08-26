# dasiGolmok — Materialized View 비동기화 및 데이터 파이프라인 최적화

> **쓰기 트랜잭션 내부에서 실행되던 PostgreSQL Materialized View 갱신을 `AFTER_COMMIT + @Async` 구조로 분리해, 로컬 PostgreSQL 약 6만 건 기준 관리자 상태변경 API 평균 응답시간을 1.079초에서 0.041초로 줄인 DB/DE 최적화 프로젝트**

* **프로젝트 구분:** 개인 프로젝트
* **핵심 역할:** PostgreSQL Materialized View 운영 구조 개선, Transaction Boundary 설계, 비동기 Refresh 구조 설계, DE 파이프라인 구성
* **기술 스택:** PostgreSQL, Spring Boot, Spring Data JPA, Flyway, Java, Python, Docker
* **주요 영역:** DBA / Database Performance Engineering / Data Engineering / Analytics Serving

---

# 1. 문제 상황 및 요구사항

## 1-1. 프로젝트 배경

dasiGolmok은 상권·스토리 데이터를 기반으로 지도, 큐레이션, 관리자 기능과 분석 기능을 제공하는 프로젝트입니다.

Repository는 다음처럼 역할별로 분리되어 있습니다.

```text
back/   → Spring Boot API
db/     → PostgreSQL + Flyway
de/     → 공공데이터 ingestion / DQ / mart
da/     → Star Schema / KPI
ai/     → FastAPI AI Assist
qa/     → QA 자동화
```

DE 영역은 별도로 `raw → quarantine → staging → mart` 구조를 두고 있으며, 데이터 파이프라인 실행 스크립트와 dataset catalog도 분리되어 있습니다.

---

## 1-2. 발생한 핵심 문제

관리자 상태 변경, 스토리 등록, 좋아요처럼 일반적인 Write API가 실행될 때 통계용 Materialized View도 같은 요청 안에서 즉시 갱신되고 있었습니다.

### 기존 구조

```text
Story / Like / Admin Write
        ↓
DB Write
        ↓
Materialized View 1 REFRESH
        ↓
Materialized View 2 REFRESH
        ↓
Response
```

즉 사용자는 하나의 데이터를 저장하거나 상태만 변경했는데, 요청이 끝나기 전에 **전체 통계 집계까지 기다려야 하는 구조**였습니다.

Materialized View는 미리 계산된 결과를 빠르게 읽는 데 유리하지만, `REFRESH MATERIALIZED VIEW`는 View의 내용을 다시 계산해야 하므로 원본 데이터가 커질수록 Refresh 비용도 커질 수 있습니다.

---

## 1-3. 해결 요구사항

DBA 관점에서 다음 요구사항을 잡았습니다.

* 일반 Write Transaction과 통계 Refresh의 책임을 분리한다.
* DB Write가 실패했는데 통계 Refresh가 실행되는 상황을 방지한다.
* 같은 Materialized View에 Refresh 요청이 동시에 몰리지 않도록 제어한다.
* Client Response가 통계 전체 재계산 시간에 종속되지 않게 한다.
* 변경 전/후 API 응답시간을 같은 조건에서 비교한다.
* 장애 발생 시 Exception을 서버 로그로 추적할 수 있어야 한다.

DE 관점에서는 다음 요구사항을 추가했습니다.

* 운영 데이터 변경과 분석용 집계를 분리한다.
* `raw → staging → DQ → mart` 데이터 처리 구조를 유지한다.
* 통계/분석 Serving은 Materialized View나 Mart를 통해 제공한다.
* 데이터 품질 실패 데이터를 별도 quarantine할 수 있어야 한다.
* 파이프라인 실행 경로를 독립된 `de/` 영역에서 관리한다.

---

# 2. 원인 분석

## 2-1. 병목은 Write Query 자체가 아니라 후속 집계 작업

처음 문제만 보면 관리자 상태변경 API가 느린 것처럼 보이지만, 실제 구조를 보면 API의 본래 업무보다 Materialized View Refresh가 훨씬 무거운 작업이었습니다.

```text
실제 요청 목적
→ Story 상태값 변경

함께 수행되던 작업
→ 전체 Analytics View 재계산
```

따라서 병목의 원인은 단일 UPDATE SQL이 아니라 **동일 요청 스레드에서 수행되는 후속 집계 작업**이라고 판단했습니다.

---

## 2-2. Transaction 내부 Refresh의 구조적 문제

기존 구조는 다음처럼 해석할 수 있습니다.

```text
BEGIN

Write
Refresh MV
Refresh MV

COMMIT
```

이 경우 문제가 두 가지 있습니다.

첫째, 사용자가 기다리는 시간이 DB Write 시간보다 통계 Refresh 시간에 크게 영향을 받습니다.

둘째, 원본 데이터가 확정되기 전에 통계 갱신 흐름이 결합되어 있어 Transaction Boundary가 불필요하게 넓습니다.

따라서 원본 Write는 먼저 확정하고 통계 갱신은 이후 작업으로 보내는 편이 더 적절하다고 판단했습니다.

---

## 2-3. 단순 `@Async`만으로는 충분하지 않음

비동기로만 바꾸면 다음 위험이 남습니다.

```text
Write 시작
→ Async Refresh 요청
→ Write Rollback
→ Refresh는 이미 실행
```

이 경우 실제 운영 데이터는 저장되지 않았는데 Analytics View만 불필요하게 Refresh될 수 있습니다.

그래서 비동기 실행 시점도 반드시 **Commit 이후**여야 했습니다.

---

## 2-4. 여러 Refresh의 동시 실행 위험

쓰기 요청이 연속해서 들어오면 다음처럼 될 수 있습니다.

```text
Request A → Refresh
Request B → Refresh
Request C → Refresh
```

이 Refresh들을 무조건 병렬 실행하면 같은 Materialized View를 동시에 갱신하려는 요청이 겹칠 수 있습니다.

Repository README에서도 PostgreSQL의 `REFRESH MATERIALIZED VIEW CONCURRENTLY`가 조회를 덜 막도록 도와주지만, 하나의 Materialized View에는 동시에 하나의 Refresh만 실행될 수 있다는 점을 근거로 단일 Thread Executor를 선택하고 있습니다.

---

# 3. 문제 해결 및 적용 과정

## Step 1. Materialized View Refresh를 Write Path에서 제거

기존 `AnalyticsViewRefresher.refreshAll()`이 직접 View Refresh를 실행하던 구조를 변경했습니다.

### Before

```text
Write API
 ↓
DB Write
 ↓
REFRESH MV
 ↓
REFRESH MV
 ↓
Response
```

### After

```text
Write API
 ↓
DB Write
 ↓
COMMIT
 ↓
Response

        ↓

Analytics Refresh Event
 ↓
Async Executor
 ↓
REFRESH MV
```

즉 Client Response와 Analytics 집계 작업의 실행 경로를 분리했습니다.

---

## Step 2. Event 기반으로 Refresh 요청 분리

직접 Refresh를 호출하지 않고:

```text
AnalyticsRefreshRequestedEvent
```

를 발행하도록 변경했습니다.

이를 통해 서비스 로직은:

```text
"데이터가 변경되었다"
```

는 사실만 전달하고,

실제 Analytics 갱신 방식은 별도의 Listener가 책임지도록 분리했습니다.

구조적으로:

```text
Write Domain
      ↓
Domain/Event Signal
      ↓
Analytics Refresh
```

경계를 만든 것입니다.

---

## Step 3. `AFTER_COMMIT` 적용

Event Listener에는:

```java
@TransactionalEventListener(
    phase = TransactionPhase.AFTER_COMMIT
)
```

방식을 적용했습니다.

목적은 명확합니다.

```text
Write 성공
→ Commit
→ Analytics Refresh

Write 실패
→ Rollback
→ Analytics Refresh 실행 안 함
```

원본 DB 데이터가 정상적으로 확정된 경우에만 후속 Analytics 작업을 실행하도록 Transaction Boundary를 재설계했습니다.

---

## Step 4. `@Async`로 요청 Thread와 분리

실제 Refresh 실행은 별도의 Thread에서 수행하도록 했습니다.

```text
Request Thread
→ DB Write
→ Response

Async Thread
→ REFRESH MATERIALIZED VIEW
```

이 방식으로 사용자가 통계 재계산이 끝날 때까지 기다리던 문제를 제거했습니다.

---

## Step 5. Refresh 전용 단일 Thread Executor 구성

병렬성을 높이기 위해 Thread를 무작정 늘리지 않았습니다.

같은 Materialized View에 Refresh 요청이 연속해서 발생할 수 있기 때문에 전용 Single Thread Executor를 사용했습니다.

```text
Refresh A ─┐
Refresh B ─┼→ Queue → 1 Thread → 순차 실행
Refresh C ─┘
```

이를 통해:

* 동일 View에 대한 Refresh 충돌 방지
* 불필요한 DB 동시 부하 방지
* 실행 순서 예측 가능성 확보

를 목표로 했습니다.

---

# 4. 성능 검증

## Step 6. 동일 데이터 조건에서 Before / After 비교

로컬 테스트 PostgreSQL인 `golmok-test-pg`에 **스토리 약 6만 건**을 넣고 관리자 상태변경 API를 기준으로 테스트했습니다.

측정은 각각 8회 수행해 평균 응답시간을 비교했습니다.

| 측정 지표                |   개선 전 |   개선 후 |          개선 효과 |
| -------------------- | -----: | -----: | -------------: |
| 관리자 상태변경 API 평균 응답시간 | 1.079초 | 0.041초 | **약 96.2% 감소** |
| 상대 처리 속도             |     1x |  약 26x |   **약 26배 개선** |

### Before

```text
1.079 sec
```

### After

```text
0.041 sec
```

따라서:

```text
1.079 → 0.041 sec
```

로 줄어 테스트 환경 기준 약 **96.2% 응답시간 개선**을 확인했습니다.

이 프로젝트에서 가장 강한 정량 성과입니다.

---

# 5. 왜 이 개선이 단순 비동기 처리 이상인가

이 작업은 단순히 코드에 `@Async` 하나를 추가한 것이 아닙니다.

기존의:

```text
OLTP Write
+
Analytics Recalculation
```

결합 구조를:

```text
OLTP Write
      ↓
   Commit
      ↓
Analytics Refresh
```

로 분리했습니다.

즉 **Operational Transaction과 Analytics Processing의 경계를 재설계한 작업**입니다.

DBA 관점에서는:

```text
Transaction Boundary Optimization
```

DE 관점에서는:

```text
Operational Data
→ Asynchronous Analytics Serving
```

으로 설명할 수 있습니다.

---

# 6. Data Engineering 구조

Repository에는 별도의 `de/` 영역이 존재합니다.

```text
de/
├── catalog/
│   └── datasets.yaml
├── fixtures/
├── data/
│   ├── raw
│   ├── quarantine
│   └── staging
├── pipeline/
├── scripts/
│   └── run_pipeline.sh
└── reports/
```

DE 흐름은 다음과 같습니다.

```text
상권 Public Data
      ↓
Raw
      ↓
Validation / DQ
   ↙        ↘
PASS       FAIL
 ↓           ↓
Staging   Quarantine
 ↓
Mart
 ↓
DA / Analytics
```

즉 서비스 DB의 Read/Write 흐름과 별도로 상권 공공데이터를 분석에 사용할 수 있는 데이터 파이프라인 영역을 분리했습니다.

---

# 7. Raw / Quarantine / Staging 분리

DE 영역에서 중요한 점은 데이터 폴더를 하나로 두지 않은 것입니다.

```text
raw
→ 원천 데이터 보존

quarantine
→ 검증 실패 데이터 격리

staging
→ 분석에 사용할 수 있도록 정제된 데이터
```

이 구조는 잘못된 데이터를 바로 Mart로 전달하지 않고, 품질 검증을 데이터 처리 과정에 포함시키기 위한 구조입니다.

---

# 8. Pipeline Boundary

Repository의 DE Pipeline 역할은:

```text
ingest
→ DQ
→ mart
```

로 구성되어 있습니다.

이를 포트폴리오에서는 다음처럼 설명할 수 있습니다.

```text
Source
 ↓
Ingestion
 ↓
Raw Preservation
 ↓
Data Quality
 ↓
Staging
 ↓
Mart Build
 ↓
Analytics Serving
```

즉 상권 데이터를 단순 CSV 파일로 읽고 끝내는 것이 아니라 **수집·품질검사·분석 데이터 생성**이라는 처리 단계로 분리했습니다.

---

# 9. Analytics Serving과 Materialized View 연결

dasiGolmok의 DB/DE 구조에서 중요한 특징은 운영 데이터와 Analytics 결과를 분리한 것입니다.

```text
Operational DB
      ↓
Data Change
      ↓
Analytics Processing
      ↓
Materialized View / Mart
      ↓
Dashboard / Analytics
```

Materialized View는 조회 시 반복 집계 비용을 줄이는 대신 Refresh가 필요한 구조입니다.

따라서 이번 성능 개선은:

> Materialized View를 없앤 것

이 아니라,

> **Materialized View의 장점은 유지하면서 Refresh 비용을 사용자 요청에서 분리한 것**

이라고 설명하는 것이 정확합니다.

---

# 10. 장애 추적성 개선

추가로 `GlobalExceptionHandler`의 예외 로깅도 개선했습니다.

### Before

```text
Exception
→ Error Response
→ Server Log에 원인 정보 부족
```

### After

```text
Exception
→ Error Response
+
Server Error Log
```

이를 통해 DB 또는 Analytics Refresh 과정에서 문제가 발생했을 때 원인을 추적할 수 있도록 운영성을 높였습니다.

---

# 11. DBA 관점 핵심 성과

## ① Transaction Boundary 재설계

```text
Before

Write
+
Analytics Refresh
=
One Request
```

```text
After

Write
→ Commit

Analytics Refresh
→ Separate Async Process
```

---

## ② Materialized View 운영 최적화

```text
Fast Read
→ Materialized View 유지

Heavy Refresh
→ Async로 분리
```

Materialized View 자체를 제거하지 않고 Read 성능상 이점을 유지하면서 Refresh의 영향만 줄였습니다.

---

## ③ 동시성 제어

```text
Multiple Refresh Requests
→ Single Thread Queue
→ Sequential Refresh
```

동일한 Materialized View의 Refresh가 충돌하거나 DB 부담을 키우는 것을 방지하기 위한 구조를 선택했습니다.

---

## ④ 정량적 성능 검증

```text
약 60,000 Story
8회 평균

1.079 sec
→ 0.041 sec

96.2% 감소
```

이 프로젝트는 DBA 포트폴리오에서 이 숫자를 가장 앞에 가져가도 됩니다.

---

# 12. DE 관점 핵심 성과

DE에서는 다음 구조를 중심으로 설명하면 됩니다.

```text
Public Data
 ↓
Raw
 ↓
DQ
 ├─ FAIL → Quarantine
 └─ PASS
       ↓
    Staging
       ↓
      Mart
       ↓
Analytics
```

그리고 운영 서비스 데이터는:

```text
OLTP Write
 ↓
Commit
 ↓
Async Analytics Refresh
 ↓
Materialized View
```

구조로 연결했습니다.

즉 dasiGolmok은 DE 관점에서 **“운영 트랜잭션과 분석 데이터 처리를 분리한 프로젝트”**라고 포지셔닝하는 것이 좋습니다.

---

# 13. 문제 해결 흐름 요약

```text
[Problem]

Write API에서
Materialized View 2개 즉시 Refresh

        ↓

[Impact]

Client가 통계 전체 재계산을 기다림
DB Write와 Analytics 작업 결합
동시 Refresh 요청 가능

        ↓

[Root Cause]

OLTP Transaction Boundary 안에
Analytics Refresh 포함

        ↓

[Action]

AnalyticsRefreshRequestedEvent
        ↓
AFTER_COMMIT
        ↓
@Async
        ↓
Single Thread Executor
        ↓
Materialized View Refresh

        ↓

[Result]

6만 Story 로컬 테스트
1.079s → 0.041s
약 96.2% 개선
```

---

# 14. 해결 결과 및 성과

| 영역                | 개선 전                  | 개선 후                          |
| ----------------- | --------------------- | ----------------------------- |
| Write API         | DB Write + 통계 Refresh | DB Write 후 바로 응답              |
| Analytics Refresh | 요청 Thread에서 동기 실행     | Commit 이후 Async               |
| Transaction       | Analytics까지 포함        | Operational Write 중심          |
| 동시 Refresh        | 병렬 요청 가능              | Single Thread Queue           |
| 관리자 API 평균 응답     | 1.079초                | **0.041초**                    |
| 응답 개선율            | -                     | **약 96.2%**                   |
| 데이터 처리            | 운영/분석 흐름 결합           | OLTP와 Analytics 분리            |
| DE 품질 처리          | 단일 처리 경로              | Raw / Quarantine / Staging 분리 |

---

# 15. 회고 및 배운 점

첫째, 성능 문제의 원인이 항상 느린 SQL 자체에 있는 것은 아니라는 점을 배웠습니다.

이번 경우 핵심 UPDATE Query보다 **같은 요청 안에서 수행되던 후속 Analytics Refresh가 실제 병목**이었습니다. 따라서 Query만 튜닝하기보다 전체 Transaction Flow를 분석하는 것이 중요했습니다.

둘째, 비동기 처리도 실행 시점이 중요하다는 점을 확인했습니다. 단순 `@Async`만 적용하면 DB Write가 실패했는데 후속 작업이 실행될 수 있기 때문에 `AFTER_COMMIT`을 통해 원본 데이터가 확정된 뒤에만 Analytics 작업이 시작되도록 해야 했습니다.

셋째, 병렬 처리가 항상 성능 개선을 의미하지 않는다는 점을 배웠습니다. 같은 Materialized View에 여러 Refresh를 병렬로 실행하는 것보다, 하나의 전용 Queue에서 순차 처리해 충돌과 DB 부하를 줄이는 편이 더 적절했습니다.

넷째, OLTP와 Analytics는 같은 DB를 사용하더라도 다른 책임을 가질 수 있다는 점을 이해했습니다. 서비스 요청은 사용자 데이터 변경을 빠르고 안정적으로 확정하는 것이 우선이고, 집계·통계는 별도 Processing Boundary로 분리하는 것이 더 적절했습니다.

다섯째, Data Engineering에서도 잘못된 데이터를 단순히 버리는 것보다 Raw를 보존하고 Quarantine으로 격리해야 이후 원인 분석과 재처리가 가능하다는 점을 프로젝트 구조에 반영했습니다.

---

# 16. 현재 프로젝트에서 주장하지 않는 것

현재 Repository 근거를 넘어서는 아래 내용은 성과로 적지 않습니다.

* PostgreSQL CPU 사용률 감소 수치
* TPS 개선 수치
* P95 / P99 latency 측정
* `EXPLAIN ANALYZE` 기반 Query Plan 튜닝
* Partial Index / BRIN
* Table Partitioning
* PgBouncer
* AWS RDS / Aurora
* Primary / Replica
* HA / Failover
* RTO / RPO
* Backup / Restore 자동화
* Kafka / Debezium CDC
* Airflow 운영 배포
* Spark 대용량 처리
* 1천만 건 이상 DB Benchmark

실제 Repository에서 확인되는 가장 강한 성능 Evidence는 **로컬 PostgreSQL 약 6만 Story, 관리자 상태변경 API 8회 평균 기준 `1.079초 → 0.041초`**입니다.

---

# 17. 포트폴리오용 최종 설명

> **dasiGolmok에서 PostgreSQL Materialized View 갱신이 사용자 Write API의 Transaction Path에 포함되어 응답시간을 증가시키는 병목을 분석했습니다. 기존에는 스토리 등록·좋아요·관리자 상태변경 후 두 개의 Materialized View를 동기 Refresh한 뒤 응답했지만, `AnalyticsRefreshRequestedEvent → @TransactionalEventListener(AFTER_COMMIT) → @Async → Single Thread Executor` 구조로 변경해 원본 DB Write와 Analytics 집계를 분리했습니다. 로컬 PostgreSQL에 스토리 약 6만 건을 구성하고 관리자 상태변경 API를 8회 측정한 결과 평균 응답시간이 1.079초에서 0.041초로 감소해 테스트 환경 기준 약 96.2% 개선되었습니다. 또한 Data Engineering 영역은 공공데이터를 `Raw → DQ → Staging → Mart`로 처리하고 검증 실패 데이터는 Quarantine으로 분리해 운영 데이터와 분석 데이터의 처리 경계를 명확히 구성했습니다.**

## 한 줄 성과

> **Materialized View Refresh를 Write Transaction에서 `AFTER_COMMIT + Async`로 분리해 약 6만 건 테스트 기준 관리자 API 평균 응답시간을 1.079초에서 0.041초로 줄여 약 96.2% 개선했습니다.**
