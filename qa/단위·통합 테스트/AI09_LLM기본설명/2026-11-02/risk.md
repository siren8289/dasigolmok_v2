# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI09-001 | Gemini 및 fallback 설명 | 안정 문구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-002 | Gemini 및 fallback 설명 | 주의 문구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-003 | Gemini 및 fallback 설명 | 위험 문구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-004 | Gemini 및 fallback 설명 | 판단 불가 문구 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-005 | Gemini 및 fallback 설명 | 동 이름 보존 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-006 | Gemini 및 fallback 설명 | 업종 보존 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-007 | Gemini 및 fallback 설명 | 최근 폐업률 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-008 | Gemini 및 fallback 설명 | ML 예상 폐업률 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-009 | Gemini 및 fallback 설명 | DL 예상 매출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-010 | Gemini 및 fallback 설명 | 추정값 고지 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-011 | Gemini 및 fallback 설명 | 키 없음 fallback | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-012 | Gemini 및 fallback 설명 | Gemini 정상 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-013 | Gemini 및 fallback 설명 | Gemini API 오류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-014 | Gemini 및 fallback 설명 | Gemini 타임아웃 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-015 | Gemini 및 fallback 설명 | Gemini 빈 텍스트 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-017 | Gemini 및 fallback 설명 | 프롬프트 숫자 정확성 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-018 | Gemini 및 fallback 설명 | 프롬프트 상권변화 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-019 | Gemini 및 fallback 설명 | 프롬프트 3문장 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-021 | Gemini 및 fallback 설명 | API Key 로그 유출 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI09-022 | Gemini 및 fallback 설명 | source 값 계약 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## AI09-001 안정 문구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=stable 설명=연남동 한식음식점 상권은 '안정' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-002 주의 문구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=warning 설명=연남동 한식음식점 상권은 '주의' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-003 위험 문구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=danger 설명=연남동 한식음식점 상권은 '위험' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-004 판단 불가 문구
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=unknown 설명=연남동 한식음식점 상권은 '판단 불가' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-005 동 이름 보존
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dong 설명=연남동 한식음식점 상권은 '안정' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-006 업종 보존
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 업종 설명=연남동 한식음식점 상권은 '안정' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-007 최근 폐업률
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: close_rate=7.3 설명=연남동 한식음식점 상권은 '안정' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-008 ML 예상 폐업률
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ml_close_rate=3.4 설명=연남동 한식음식점 상권은 '안정' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-009 DL 예상 매출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dl_sales=740 설명=연남동 한식음식점 상권은 '안정' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-010 추정값 고지
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: basic=연남동 한식음식점 상권은 '안정' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-011 키 없음 fallback
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: source=basic constructed=None text=연남동 한식음식점 상권은 '안정' 단계입니다. 최근 폐업률은 7.3%이고, AI가 예상한 폐업률은 3.4%입니다. 점포당 예상 매출은 약 740만원입니다. 이 값은 공공데이터 추정값이며, 실제 창업 결정은 현장 확인이 필요합니다.

## AI09-012 Gemini 정상
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: source=gemini text='연남동 한식음식점은 안정입니다.'

## AI09-013 Gemini API 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 서버 오류 API 500 source=basic basic_match=True

## AI09-014 Gemini 타임아웃
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 응답 시간초과 timeout source=basic basic_match=True

## AI09-015 Gemini 빈 텍스트
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 빈 텍스트 source=basic basic_match=True

## AI09-017 프롬프트 숫자 정확성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: prompt에 4%=True 5%=True 전송일치=True

## AI09-018 프롬프트 상권변화
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 상권변화 줄=['상권변화: 상권축소']

## AI09-019 프롬프트 3문장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 프롬프트 첫 줄들=['너는 서울 골목 상권 상담 도우미다.', '아래 진단 결과를 보고 사장님에게 3문장 이내의 쉬운 한국어로 설명하고, 현실적인 조언 1개를 덧붙여라.', '숫자는 그대로 인용하고, 투자 권유나 단정적인 표현은 하지 마라.']

## AI09-021 API Key 로그 유출
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: source=basic stdout='Gemini 호출 실패, 기본 설명을 사용합니다: RuntimeError\n' stderr='' key노출=False

## AI09-022 source 값 계약
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: basic_source=basic gemini_source=gemini basic_len=128 gemini_text='gemini 설명'
