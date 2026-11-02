# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE06-001 | Spring 에러 표준화·로그 | ApiException 404 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE06-002 | Spring 에러 표준화·로그 | ApiException 502 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE06-003 | Spring 에러 표준화·로그 | Bean Validation | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE06-004 | Spring 에러 표준화·로그 | JSON 문법 오류 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE06-005 | Spring 에러 표준화·로그 | 알 수 없는 예외 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE06-006 | Spring 에러 표준화·로그 | 서버 오류 로깅 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE06-007 | Spring 에러 표준화·로그 | 사용자 오류 로그 수준 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE06-008 | Spring 에러 표준화·로그 | 예외 스택 마스킹 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE06-009 | Spring 에러 표준화·로그 | 동시 실패 10건 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE06-010 | Spring 에러 표준화·로그 | 다중 필드 검증 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE06-012 | Spring 에러 표준화·로그 | CORS 실패 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |

## BE06-001 ApiException 404
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 없는 진단 GET은 404. JSON에 errorCode=NOT_FOUND와 message가 있다.

## BE06-002 ApiException 502
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 진단 POST 중 AI ApiException은 502. body errorCode=AI_ERROR, message가 있다.

## BE06-003 Bean Validation
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 빈 district POST는 400, errorCode=VALIDATION_ERROR.

## BE06-004 JSON 문법 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 깨진 JSON POST는 400, errorCode=INVALID_JSON.

## BE06-005 알 수 없는 예외
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: RuntimeException(boom-internal-detail)은 500 INTERNAL_ERROR. message는 서버 오류가 발생했습니다.이고 상세 문자열은 없다.

## BE06-006 서버 오류 로깅
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 5xx ApiException 처리 로그에 ai-down-marker와 cause root-cause-marker가 있고 ERROR throwable이 붙었다.

## BE06-007 사용자 오류 로그 수준
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 4xx NOT_FOUND 처리 시 GlobalExceptionHandler ERROR 로그와 throwable이 없었다.

## BE06-008 예외 스택 마스킹
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: SQLException의 DROP TABLE, secret-stack, SQLException 문구는 응답에 없고 status=500, errorCode=INTERNAL_ERROR.

## BE06-009 동시 실패 10건
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 병렬 GET id 910000~910009가 각각 404 NOT_FOUND이고 본문에 자기 id만 들어 응답이 섞이지 않았다.

## BE06-010 다중 필드 검증
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district/dong/industry 세 @NotBlank 실패가 400 VALIDATION_ERROR 한 메시지에 세 필드명을 모두 이었다.

## BE06-012 CORS 실패
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: Origin https://evil.example OPTIONS /api/diagnoses는 403, Allow-Origin 헤더 없음. 로그: Reject: 'https://evil.example' origin is not allowed.
