# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| BE02-001 | 진단 서비스·저장 | AI 요청 필드 매핑 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-002 | 진단 서비스·저장 | AI 응답 우선 지역 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-003 | 진단 서비스·저장 | AI 지역 누락 fallback | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-004 | 진단 서비스·저장 | AI 동 누락 fallback | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-005 | 진단 서비스·저장 | AI 업종 누락 fallback | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-006 | 진단 서비스·저장 | 분기 필드 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-007 | 진단 서비스·저장 | 점포 수 숫자 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-008 | 진단 서비스·저장 | 개업률 숫자 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-009 | 진단 서비스·저장 | 폐업률 숫자 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-010 | 진단 서비스·저장 | 프랜차이즈 비율 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-011 | 진단 서비스·저장 | 유동인구 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-012 | 진단 서비스·저장 | 변화코드 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-013 | 진단 서비스·저장 | 변화명 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-014 | 진단 서비스·저장 | 영업기간 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-015 | 진단 서비스·저장 | 점포당 매출 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-016 | 진단 서비스·저장 | ML 예측 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-017 | 진단 서비스·저장 | DL 예측 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-018 | 진단 서비스·저장 | 상태 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-019 | 진단 서비스·저장 | 위험불리언 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-020 | 진단 서비스·저장 | 설명 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-021 | 진단 서비스·저장 | 설명 출처 저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-025 | 진단 서비스·저장 | AI 장애 시 비저장 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-026 | 진단 서비스·저장 | ID 정상 조회 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-027 | 진단 서비스·저장 | ID 미등록 조회 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-028 | 진단 서비스·저장 | 최근 조회 정렬 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-029 | 진단 서비스·저장 | 동시 생성 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |
| BE02-030 | 진단 서비스·저장 | 존재하지 않는 지역 | JUnit | PASS | MockMvc | NOT_RUN | NOT_RUN |

## BE02-001 AI 요청 필드 매핑
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: diagnose에 넘긴 Map은 district=마포구, dong=연남동, industry=한식 세 키뿐이었다.

## BE02-002 AI 응답 우선 지역
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 요청 district=종로구, AI district=마포구일 때 저장 district는 마포구였다.

## BE02-003 AI 지역 누락 fallback
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: AI JSON에 district 키가 없으면 저장값은 요청 district 마포구였다.

## BE02-004 AI 동 누락 fallback
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: AI JSON에 dong 키가 없으면 저장값은 요청 dong 연남동이었다.

## BE02-005 AI 업종 누락 fallback
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: AI JSON에 industry 키가 없으면 저장값은 요청 industry 한식이었다.

## BE02-006 분기 필드 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: AI quarter="20244"가 Diagnosis.quarter에 문자열 20244로 저장됐다.

## BE02-007 점포 수 숫자 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: store_count=25가 Double 25.0으로 저장됐다.

## BE02-008 개업률 숫자 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: open_rate=3.4가 Double 3.4로 저장됐다.

## BE02-009 폐업률 숫자 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: close_rate=6.2가 Double 6.2로 저장됐다.

## BE02-010 프랜차이즈 비율 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: franchise_ratio=0.2가 Double 0.2로 저장됐다.

## BE02-011 유동인구 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: foot_traffic=3000이 Double 3000.0으로 저장됐다.

## BE02-012 변화코드 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_code=HL이 문자열 HL로 저장됐다.

## BE02-013 변화명 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: change_name=상권축소가 한글 그대로 저장됐다.

## BE02-014 영업기간 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: operate_months=23.1이 Double 23.1로 저장됐다.

## BE02-015 점포당 매출 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: sales_per_store=800.5가 Double 800.5로 저장됐다.

## BE02-016 ML 예측 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ml_close_rate=5.1이 Double 5.1로 저장됐다.

## BE02-017 DL 예측 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: dl_sales_per_store=730.5가 Double 730.5로 저장됐다.

## BE02-018 상태 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: status=danger가 문자열 danger로 저장됐다.

## BE02-019 위험불리언 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: is_danger=true일 때 엔티티 danger=true로 저장됐다.

## BE02-020 설명 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: explanation=기본 설명이 한글 그대로 저장됐다.

## BE02-021 설명 출처 저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: explanation_source=basic이 basic으로 저장됐다.

## BE02-025 AI 장애 시 비저장
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: AiClient가 ApiException을 던지면 저장 전 예외가 전파되고 diagnosis 건수는 호출 전과 같았다. status=502, code=AI_ERROR.

## BE02-026 ID 정상 조회
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: id를 1로 재시작한 저장 건을 get(1)로 조회하면 같은 Diagnosis(dong=연남동, industry=한식)가 반환됐다.

## BE02-027 ID 미등록 조회
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: get(9999999)는 ApiException status=404, errorCode=NOT_FOUND.

## BE02-028 최근 조회 정렬
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 12건 저장 후 recent()는 10건이고 id가 내림차순이며 가장 오래된 2건은 빠졌다.

## BE02-029 동시 생성
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 병렬 10건 diagnose가 모두 커밋됐다. 서로 다른 id 10개, diagnosis 행 수 10.

## BE02-030 존재하지 않는 지역
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: AI 404를 흉내 낸 예외에서 저장 건수는 그대로이고 ApiException(5xx)이 반환됐다.
