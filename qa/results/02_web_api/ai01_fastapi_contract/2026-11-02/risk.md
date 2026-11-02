# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI01-001 | FastAPI 엔드포인트·스키마 | 옵션 API | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-002 | FastAPI 엔드포인트·스키마 | 진단 API | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-003 | FastAPI 엔드포인트·스키마 | 추천 API | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-004 | FastAPI 엔드포인트·스키마 | 헬스 API | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-005 | FastAPI 엔드포인트·스키마 | RAG ask 연결 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-006 | FastAPI 엔드포인트·스키마 | RAG health 연결 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-007 | FastAPI 엔드포인트·스키마 | 진단 존재하지 않는 조합 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-008 | FastAPI 엔드포인트·스키마 | 추천 존재하지 않는 동 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-009 | FastAPI 엔드포인트·스키마 | 진단 JSON 누락 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-010 | FastAPI 엔드포인트·스키마 | 추천 JSON 누락 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-011 | FastAPI 엔드포인트·스키마 | 진단 숫자 타입 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI01-014 | FastAPI 엔드포인트·스키마 | 응답 404 본문 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## AI01-001 옵션 API
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 옵션 조회 GET /api/v1/options status=200 keys=['districts', 'dongs', 'industries', 'semas_dong_count', 'semas_upjong_count'] districts=25 dongs=425 industries=100

## AI01-002 진단 API
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST /api/v1/diagnose status=200 dong=연남동 status_field=warning ml=3.17 dl=4902.2 source=basic

## AI01-003 추천 API
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST /api/v1/recommend status=200 dong=연남동 recommendations=5 all=65

## AI01-004 헬스 API
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 헬스 확인 GET /health status=200 body={'status': 'ok', 'version': '2.1.0'}

## AI01-005 RAG ask 연결
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: POST /api/v1/commercial-rag/ask status=200 intent=support_policy answer_len=589 question=마포구 창업 지원금 알려줘

## AI01-006 RAG health 연결
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: RAG 상태 GET /api/v1/commercial-rag/health status=200 body={'status': 'ok', 'feature': 'commercial_rag_001'}

## AI01-007 진단 존재하지 않는 조합
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 존재하지 않는 동·업종 status=404 body={'detail': '해당 행정동·업종 데이터가 없습니다.'}

## AI01-008 추천 존재하지 않는 동
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 없는 동 추천 status=404 body={'detail': '해당 행정동 데이터가 없습니다.'}

## AI01-009 진단 JSON 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: district 누락 status=422 body={'detail': [{'type': 'missing', 'loc': ['body', 'district'], 'msg': 'Field required', 'input': {'dong': '연남동', 'industry': '한식음식점'}}]}

## AI01-010 추천 JSON 누락
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong 누락 status=422 body={'detail': [{'type': 'missing', 'loc': ['body', 'dong'], 'msg': 'Field required', 'input': {'district': '마포구'}}]}

## AI01-011 진단 숫자 타입
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 정수 district 거부 status=422 body={'detail': [{'type': 'string_type', 'loc': ['body', 'district'], 'msg': 'Input should be a valid string', 'input': 3}]}

## AI01-014 응답 404 본문
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=404 detail='해당 행정동·업종 데이터가 없습니다.' service_error='해당 행정동·업종 데이터가 없습니다.'
