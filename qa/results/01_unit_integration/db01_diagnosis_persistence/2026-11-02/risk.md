# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| DB01-001 | JPA 엔터티·Repository | 기본키 자동생성 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-002 | JPA 엔터티·Repository | 한글 지역 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-003 | JPA 엔터티·Repository | 한글 동 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-004 | JPA 엔터티·Repository | 한글 업종 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-005 | JPA 엔터티·Repository | 분기 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-006 | JPA 엔터티·Repository | 저장/조회 일치 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-007 | JPA 엔터티·Repository | Double null | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-008 | JPA 엔터티·Repository | 위험 boolean false | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-009 | JPA 엔터티·Repository | 위험 boolean true | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-010 | JPA 엔터티·Repository | 설명 길이 2000 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-011 | JPA 엔터티·Repository | 설명 길이 2001 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-012 | JPA 엔터티·Repository | 설명 특수문자 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-013 | JPA 엔터티·Repository | 생성 시각 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-014 | JPA 엔터티·Repository | 최근 10건 조회 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-015 | JPA 엔터티·Repository | 단건 삭제 후 조회 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-016 | JPA 엔터티·Repository | 동시 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-017 | JPA 엔터티·Repository | 재시작 후 데이터 유지 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| DB01-019 | JPA 엔터티·Repository | 트랜잭션 AI 실패 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |

## DB01-001 기본키 자동생성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: diagnosis.id IDENTITY 로 값을 넣지 않았는데 id=1, 2 로 증가했다. 엔터티 전략은 GenerationType.IDENTITY.

## DB01-002 한글 지역 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: server_encoding=UTF8. district '마포구' 저장 후 조회 값이 같다.

## DB01-003 한글 동 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong '연남동' 이 UTF-8 그대로 저장·조회됐다.

## DB01-004 한글 업종 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industry '한식음식점' 이 UTF-8 그대로 저장·조회됐다.

## DB01-005 분기 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: quarter '20244' 문자열이 숫자로 바뀌지 않고 그대로 보존됐다.

## DB01-006 저장/조회 일치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 진단 20개 컬럼(문자·실수·boolean·시각)을 넣고 RETURNING 값이 원본과 같다.

## DB01-007 Double null
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: foot_traffic NULL 저장·조회가 성공했다. 엔터티 필드는 primitive가 아닌 Double.

## DB01-008 위험 boolean false
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: danger=false 가 true나 NULL로 바뀌지 않고 false로 조회됐다.

## DB01-009 위험 boolean true
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: danger=true 가 false로 바뀌지 않고 true로 조회됐다.

## DB01-010 설명 길이 2000
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한글 2000자를 explanation varchar(2000)에 저장했다. @Column(length=2000).

## DB01-011 설명 길이 2001
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한글 2001자는 varchar(2000) 제약으로 거절됐다. 22001 value too long for type character varying(2000)

## DB01-012 설명 특수문자
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한글, 큰따옴표, 이모지(😀)가 explanation에 그대로 남았다.

## DB01-013 생성 시각
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: Diagnosis 필드 초기화가 createdAt=LocalDateTime.now()이다. DB 컬럼 default는 None이고, 앱이 넣은 2026-11-02T19:41:38가 그대로 저장됐다.

## DB01-014 최근 10건 조회
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 12건 추가 후 ORDER BY id DESC LIMIT 10 결과 10건, 내림차순, 최대 id=25가 맨 앞. 리포지토리 메서드는 findTop10ByOrderByIdDesc.

## DB01-015 단건 삭제 후 조회
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: id=26 삭제 후 SELECT count=0. DiagnosisService.get은 없으면 ApiException.notFound(HttpStatus.NOT_FOUND)를 던지고 GlobalExceptionHandler가 e.getStatus()로 응답하므로 HTTP 404다.

## DB01-016 동시 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 스레드 20개가 동시에 INSERT 했고 id 20개가 모두 다르다. 범위 27–46.

## DB01-017 재시작 후 데이터 유지
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: docker restart qa-pg-dasigolmok 후 id=47 재접속 조회가 삽입값과 같다. ('재시작구', '재시작동', '재시작업', '20244', '유지')

## DB01-019 트랜잭션 AI 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: DiagnosisService.diagnose는 aiClient.diagnose 다음에만 save한다. AI 예외면 save에 도달하지 않는다. 같은 DB에서 INSERT 후 예외를 롤백하면 id=19 행이 0건이다.
