# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI02-001 | 행정동 통계·옵션 캐시 | 통계 JSON 로드 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-002 | 행정동 통계·옵션 캐시 | 옵션 JSON 로드 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-003 | 행정동 통계·옵션 캐시 | 통계 경로 오류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-004 | 행정동 통계·옵션 캐시 | 옵션 경로 오류 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-005 | 행정동 통계·옵션 캐시 | 첫 조회 캐시 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-006 | 행정동 통계·옵션 캐시 | 첫 옵션 캐시 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-007 | 행정동 통계·옵션 캐시 | 동업종 완전 일치 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-008 | 행정동 통계·옵션 캐시 | 업종 다름 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-009 | 행정동 통계·옵션 캐시 | 동 다름 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-010 | 행정동 통계·옵션 캐시 | 존재하지 않는 동 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-011 | 행정동 통계·옵션 캐시 | 동 기준 전체 업종 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI02-016 | 행정동 통계·옵션 캐시 | 없는 필수 key | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## AI02-001 통계 JSON 로드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 통계 적재 type=list len=25936 sample_keys=['change_code', 'change_name', 'close_count', 'close_rate', 'district', 'dong']

## AI02-002 옵션 JSON 로드
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 선택지 적재 type=dict keys=['districts', 'dongs', 'industries', 'semas_dong_count', 'semas_upjong_count']

## AI02-003 통계 경로 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: STATS_PATH 없음 → FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/qp/wtpnyvgn0kx_759hkfcdztw80000gn/T/pytest-of-jeong-yelim/pytest-3/test_AI02_0030/missing_dong_stats.json'

## AI02-004 옵션 경로 오류
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: OPTIONS_PATH 없음 → FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/qp/wtpnyvgn0kx_759hkfcdztw80000gn/T/pytest-of-jeong-yelim/pytest-3/test_AI02_0040/missing_options.json'

## AI02-005 첫 조회 캐시
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: load_stats 2회 read_text 호출=1 same_object=True len=25936

## AI02-006 첫 옵션 캐시
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: load_options 2회 read_text 호출=1 same_object=True

## AI02-007 동업종 완전 일치
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: find_stat(연남동,한식음식점) district=마포구 industry=한식음식점 matches=1

## AI02-008 업종 다름
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 한식=한식음식점 PC방=PC방

## AI02-009 동 다름
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 연남동 district=마포구 역삼1동 district=강남구

## AI02-010 존재하지 않는 동
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 없는 동 조회 find_stat=None industries_in_dong=[]

## AI02-011 동 기준 전체 업종
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industries_in_dong('연남동')=65 전체필터=65 districts=['마포구']

## AI02-016 없는 필수 key
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: industry 누락 행 → KeyError: 'industry'
