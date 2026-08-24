# dasiGolmok 

## 1. 핵심 한 줄

> **Golmok은 쓰기 API 안에서 무거운 통계 Materialized View 갱신을 바로 실행하던 구조를, 커밋 이후 비동기 작업으로 분리해 관리자 상태변경 API 응답시간을 약 96.2% 개선한 프로젝트입니다.**

---

## 프로젝트 구조

```text
dasigolmog/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── ai/
│   ├── catalog/
│   │   └── policy.yaml
│   ├── scripts/
│   │   └── run_ai.sh
│   └── service/                   # FastAPI AI assist (tags/summary/classify/curation)
│       ├── app/
│       ├── Dockerfile
│       └── requirements.txt
├── back/                          # Spring Boot API
│   ├── db/
│   │   └── README.md
│   ├── gradle/
│   │   └── wrapper/
│   ├── scripts/
│   │   ├── db-up.sh
│   │   └── db-down.sh
│   ├── src/
│   │   └── main/                  # java + resources + migration
│   ├── build.gradle.kts
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── gradlew*
├── da/                            # Data Analytics
│   ├── catalog/
│   │   └── kpi.yaml
│   ├── pipeline/                  # star build · KPI
│   ├── scripts/
│   │   └── run_analytics.sh
│   ├── sql/
│   │   └── kpi_queries.sql
│   └── reports/
├── de/                            # Data Engineering
│   ├── catalog/
│   │   └── datasets.yaml
│   ├── fixtures/                  # 상권 CSV
│   ├── data/                      # raw · quarantine · staging
│   ├── pipeline/                  # ingest → DQ → mart
│   ├── scripts/
│   │   └── run_pipeline.sh
│   └── reports/
├── front/                         # Next.js
│   ├── src/
│   │   ├── app/                   # page routes (admin/auth/curation/map/stories)
│   │   ├── components/            # Header, StoryCard, StoryMap...
│   │   ├── lib/                   # api-client, auth-context
│   │   └── types/
│   ├── package.json
│   ├── next.config.ts
│   └── Dockerfile
├── qa/
│   ├── catalog/
│   │   └── traceability.yaml
│   ├── evidence/
│   ├── reports/
│   │   └── latest_run.json
│   └── scripts/
│       └── run_gm_tc.{py,sh}
├── scripts/                       # deploy, health-check, rollback
├── docker-compose.yml
├── docker-compose.dev.yml
├── package.json                   # monorepo scripts
├── DEPLOYMENT.md
└── README.md
```

| 경로 | 역할 |
|------|------|
| `back/` | BE API (Auth·Story·Admin·Analytics·AI gateway) |
| `ai/` | FastAPI AI assist + policy catalog (제안만, 검수 대체 없음) |
| `front/` | FE (지도·큐레이션·등록·관리자) |
| `de/` | 상권 공공데이터 파이프라인 |
| `da/` | 이벤트·스타 스키마·KPI |
| `ai/` | AI 정책 카탈로그 (기능은 `back/.../ai`) |
| `qa/` | GM-TC 자동화·증거 팩 |

---

## 2. 문제: 사용자가 통계 재계산까지 기다리는 구조

기존에는 `AnalyticsViewRefresher.refreshAll()`이 스토리 등록, 좋아요, 관리자 승인 같은 쓰기 트랜잭션 안에서 두 개의 Materialized View를 바로 갱신하고 있었습니다.

```text
Before

스토리 등록 / 좋아요 / 관리자 승인 요청
→ DB 쓰기 작업 수행
→ Materialized View 2개 즉시 refresh
→ refresh가 끝난 뒤 사용자에게 응답
```

비전공자 관점에서 보면, 사용자는 “스토리 하나 저장해줘”라고 요청했는데 서버는 그 자리에서 **전체 통계 장부까지 다시 정리한 뒤 응답**하고 있던 것입니다.

PostgreSQL 공식문서에 따르면 `REFRESH MATERIALIZED VIEW`는 Materialized View의 내용을 완전히 교체하며, `WITH DATA`가 지정되거나 기본값이면 View를 정의한 쿼리를 다시 실행해 새 데이터를 만듭니다. 즉, 원본 데이터가 많아질수록 갱신 비용이 커질 수 있습니다.

---

## 3. Materialized View란?

Materialized View는 매번 계산하는 일반 View와 달리, **미리 계산해 저장해둔 통계표**에 가깝습니다.

```text
일반 View:
조회할 때마다 원본 데이터를 계산한다.

Materialized View:
계산 결과를 저장해두고 빠르게 읽는다.
```

PostgreSQL 공식문서는 Materialized View가 일반 View처럼 rule system을 사용하지만, 결과를 테이블과 비슷한 형태로 저장한다고 설명합니다.

그래서 관리자 대시보드나 통계 화면에는 유리하지만, 원본 데이터가 바뀌면 저장된 통계표도 다시 갱신해야 합니다.

비전공자식으로 말하면,
매번 전체 장부를 계산하지 않으려고 **미리 만들어둔 통계 요약표**입니다. 다만 원본 장부가 바뀌면 이 요약표도 다시 업데이트해야 합니다.

---

## 4. 수정: 커밋 후 비동기 refresh로 분리

수정 후에는 `AnalyticsViewRefresher.refreshAll()`이 직접 `REFRESH`를 실행하지 않고, `AnalyticsRefreshRequestedEvent`만 발행하도록 바꿨습니다.

```text
After

스토리 등록 / 좋아요 / 관리자 승인 요청
→ DB 쓰기 작업 수행
→ 트랜잭션 커밋
→ 사용자에게 먼저 응답
→ 이후 별도 스레드에서 Materialized View refresh
```

변경 구조는 다음과 같습니다.

| 변경 항목                                               | 내용                                        |
| --------------------------------------------------- | ----------------------------------------- |
| `AnalyticsRefreshRequestedEvent`                    | 통계 갱신이 필요하다는 이벤트 발행                       |
| `@TransactionalEventListener(phase = AFTER_COMMIT)` | 쓰기 트랜잭션이 성공적으로 커밋된 뒤 refresh 이벤트 처리       |
| `@Async`                                            | 실제 refresh 작업을 사용자 요청 스레드가 아닌 별도 스레드에서 실행 |
| `AnalyticsAsyncConfig`                              | refresh 전용 단일 스레드 executor 구성             |

Spring 공식문서에 따르면 `@TransactionalEventListener`의 기본 phase는 `AFTER_COMMIT`입니다. 따라서 DB 쓰기가 성공적으로 끝난 뒤 후속 작업을 실행하는 구조에 적합합니다.

---

## 5. 왜 `AFTER_COMMIT`인가?

통계 View는 원본 데이터가 DB에 확정된 뒤 갱신되어야 합니다.

```text
스토리 저장 성공
→ 커밋 완료
→ 통계 View 갱신
```

커밋 전에 통계 갱신을 실행하면, 아직 확정되지 않은 데이터를 기준으로 계산하거나, 저장이 실패했는데도 불필요한 갱신이 발생할 수 있습니다.

그래서 이번 구조는 **저장 성공이 확정된 뒤 통계 갱신을 요청하는 방식**으로 바꾼 것입니다.

비전공자식으로 말하면,
서류가 최종 승인되기도 전에 통계표에 반영하지 않고, **승인이 끝난 뒤 통계 담당자에게 업데이트 요청을 보내는 방식**입니다.

---

## 6. 왜 `@Async`인가?

`@Async`는 현재 요청 흐름과 별도로 작업을 실행하기 위한 Spring의 비동기 처리 방식입니다.

Spring 공식문서에서 `@EnableAsync`는 Spring의 비동기 메서드 실행 기능을 활성화한다고 설명합니다. 또한 Spring의 `TaskExecutor` 추상화는 executor가 단일 스레드일 수도, 동기식일 수도 있으며 구현 세부사항을 숨겨준다고 설명합니다.

이번 작업에서는 사용자가 기다려야 하는 흐름과 통계 갱신 흐름을 분리했습니다.

```text
기존:
사용자 요청 스레드가 DB 저장 + 통계 갱신까지 모두 처리

개선:
사용자 요청 스레드는 DB 저장 후 응답
통계 갱신은 별도 스레드에서 처리
```

쉽게 말하면, 계산이 오래 걸리는 일을 **계산대 앞에서 바로 처리하지 않고, 접수 후 뒤쪽 작업대로 넘긴 것**입니다.

---

## 7. 왜 단일 스레드 executor인가?

`REFRESH MATERIALIZED VIEW CONCURRENTLY`는 이름에 `CONCURRENTLY`가 붙어 있지만, 같은 Materialized View에 대해 여러 refresh가 동시에 실행될 수 있는 것은 아닙니다.

PostgreSQL 공식문서는 `CONCURRENTLY` 옵션을 사용하면 concurrent select를 잠그지 않고 refresh할 수 있다고 설명하면서도, 해당 옵션을 사용하더라도 하나의 Materialized View에는 한 번에 하나의 `REFRESH`만 실행될 수 있다고 설명합니다.

그래서 여러 쓰기 요청이 동시에 들어올 때 refresh 작업을 병렬로 많이 실행하면, 오히려 서로 대기하거나 DB 부담이 커질 수 있습니다.

이번에는 전용 단일 스레드 executor를 사용해 refresh를 순서대로 처리하게 했습니다.

```text
요청 A: refresh 필요
요청 B: refresh 필요
요청 C: refresh 필요

→ refresh 작업은 한 줄로 대기
→ 하나씩 순서대로 실행
→ 같은 View에 대한 동시 refresh 충돌 방지
```

Spring `ThreadPoolTaskExecutor` 공식문서는 corePoolSize, maxPoolSize, queueCapacity 같은 속성으로 `ThreadPoolExecutor`를 bean style로 설정하고 Spring `TaskExecutor`로 노출할 수 있다고 설명합니다.

비전공자식으로 말하면,
통계표를 여러 명이 동시에 고치다가 꼬이지 않도록 **한 명의 통계 담당자가 순서대로 처리하게 만든 것**입니다.

---

## 8. 측정 결과

로컬 테스트 DB인 `golmok-test-pg`에 스토리 약 6만 건을 넣고, 관리자 상태변경 API 기준으로 8회 평균 응답시간을 비교했습니다.

| 구분                | 평균 응답시간 |
| ----------------- | ------- |
| 수정 전: 동기 refresh  | 1.079초  |
| 수정 후: 비동기 refresh | 0.041초  |

결과는 다음과 같습니다.

```text
1.079초 → 0.041초
약 96.2% 응답시간 감소
약 26배 빨라짐
```

즉, 데이터가 쌓일수록 사용자 요청에 붙던 통계 갱신 비용을 분리해, 클라이언트는 DB 쓰기 반영이 끝나는 즉시 응답을 받을 수 있게 되었습니다.

README에는 이렇게 쓰는 게 안전합니다.

> 로컬 테스트 DB에 스토리 약 6만 건을 넣고 관리자 상태변경 API를 8회 측정한 결과, 평균 응답시간이 1.079초에서 0.041초로 감소했습니다. 이는 테스트 환경 기준 약 96.2% 응답시간 개선입니다.

---

## 9. 예외 로깅 개선

추가로 `GlobalExceptionHandler`에서 처리되지 않은 예외가 로그 없이 응답으로만 처리되던 부분도 수정했습니다.

Spring MVC 공식문서는 `@Controller`와 `@ControllerAdvice` 클래스가 `@ExceptionHandler` 메서드를 통해 controller method에서 발생한 예외를 처리할 수 있다고 설명합니다. 또한 `@ControllerAdvice`에 선언된 전역 `@ExceptionHandler`는 모든 Controller나 handler에서 발생한 예외 처리에 사용할 수 있습니다.

이번 변경은 예외 처리 정책을 크게 바꾼 것이 아니라, 장애가 났을 때 원인을 추적할 수 있도록 **서버 로그를 남기는 운영성 개선**입니다.

```text
Before

예외 발생
→ 에러 응답은 내려감
→ 서버 로그에 원인 추적 정보 부족

After

예외 발생
→ 에러 응답 처리
→ 서버 로그에 예외 원인 기록
```

비전공자식으로 말하면,
손님에게는 “문제가 발생했습니다”라고 안내하고, 내부 기록에는 **어디서 왜 문제가 생겼는지 남기는 구조**입니다.

---

## 10. 최종적으로 줄어든 비용

```text
1. 쓰기 API 응답 대기 시간 감소
2. 사용자 요청 스레드의 무거운 통계 작업 부담 제거
3. 트랜잭션 실패 시 불필요한 통계 갱신 방지
4. Materialized View refresh 충돌 가능성 감소
5. 통계 갱신 작업을 별도 executor에서 관리
6. 장애 발생 시 서버 로그로 원인 추적 가능
```

---

## 11. 문서용 요약 문장

Golmok의 통계 View 갱신 구조를 동기 처리에서 커밋 후 비동기 처리로 변경했습니다.

기존에는 스토리 등록, 좋아요, 관리자 승인 같은 쓰기 트랜잭션 안에서 `AnalyticsViewRefresher.refreshAll()`이 두 개의 Materialized View를 즉시 `REFRESH MATERIALIZED VIEW CONCURRENTLY`로 갱신했습니다. PostgreSQL에서 Materialized View는 계산 결과를 테이블처럼 저장해두는 구조이고, `REFRESH MATERIALIZED VIEW`는 해당 View의 데이터를 다시 채우는 작업이므로 데이터가 많아질수록 갱신 비용이 커질 수 있습니다.

이를 해결하기 위해 `AnalyticsRefreshRequestedEvent`를 발행하고, 실제 refresh는 `@TransactionalEventListener(phase = AFTER_COMMIT)`와 `@Async`를 사용해 커밋 이후 별도 스레드에서 실행되도록 변경했습니다. 또한 같은 View에 대한 refresh가 동시에 여러 번 실행되지 않도록 전용 단일 스레드 executor를 구성해 작업을 직렬화했습니다.

로컬 테스트 DB에 스토리 약 6만 건을 넣고 관리자 상태변경 API를 8회 측정한 결과, 평균 응답시간이 1.079초에서 0.041초로 감소했습니다. 이는 테스트 환경 기준 약 96.2% 응답시간 개선이며, 약 26배 빨라진 결과입니다.

추가로 `GlobalExceptionHandler`에 처리되지 않은 예외 로그를 남기도록 보완해, 장애 발생 시 원인 추적이 가능하도록 운영성을 개선했습니다.

---

## 12. 한 줄 설명

> **Golmok의 쓰기 API 안에서 실행되던 Materialized View 갱신을 커밋 후 비동기 작업으로 분리해, 로컬 테스트 환경 기준 관리자 상태변경 API 평균 응답시간을 1.079초에서 0.041초로 줄인 응답속도 최적화 작업입니다.**

---

## 13. README 카드용 문장

> **Materialized View 동기 갱신 병목을 이벤트 기반 비동기 처리로 분리하여, 스토리 약 6만 건 기준 관리자 상태변경 API 응답시간을 1.079초에서 0.041초로 개선했습니다. `AFTER_COMMIT` 이벤트와 단일 스레드 executor로 통계 갱신의 안정성도 함께 확보했습니다.**

---

## 14. 공식문서 참고

| 적용 내용                       | 공식문서                                   |
| --------------------------- | -------------------------------------- |
| Materialized View 구조        | PostgreSQL Materialized Views          |
| `REFRESH MATERIALIZED VIEW` | PostgreSQL `REFRESH MATERIALIZED VIEW` |
| 트랜잭션 커밋 후 이벤트 처리            | Spring `@TransactionalEventListener`   |
| 비동기 실행 활성화                  | Spring `@EnableAsync`                  |
| TaskExecutor 구조             | Spring Task Execution and Scheduling   |
| 전용 executor 설정              | Spring `ThreadPoolTaskExecutor`        |
| 전역 예외 처리                    | Spring MVC `@ExceptionHandler`         |
| ControllerAdvice            | Spring MVC `@ControllerAdvice`         |
