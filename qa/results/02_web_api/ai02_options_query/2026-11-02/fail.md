# FAIL

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI02-012 | 행정동 통계·옵션 캐시 | 동 문자열 공백 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI02-013 | 행정동 통계·옵션 캐시 | 동 이름 중복 자치구 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI02-014 | 행정동 통계·옵션 캐시 | 중복 분기 통계 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI02-015 | 행정동 통계·옵션 캐시 | 대용량 조회 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI02-017 | 행정동 통계·옵션 캐시 | JSON 타입 변조 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |
| AI02-018 | 행정동 통계·옵션 캐시 | 옵션 JSON 새 버전 | pytest | FAIL | 모킹 | NOT_RUN | FAIL |

## AI02-012 동 문자열 공백
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 일치 정책·trim 여부 명시
- 실제: exact=있음 dong=' 연남동 ' → None industry=' 한식음식점 ' → None
- 결함ID: DEF-AI02-012
- 코드: ai/src/dong_stats.py

## AI02-013 동 이름 중복 자치구
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: district 포함 식별키 사용
- 실제: industries_in_dong('신사동') rows=149 districts=['강남구', '관악구']
- 결함ID: DEF-AI02-013
- 코드: ai/src/dong_stats.py

## AI02-014 중복 분기 통계
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 최신 데이터만 선택됨을 검증
- 실제: 복수 quarter 조회 결과 quarter=20231 close_rate=1.0
- 결함ID: DEF-AI02-014
- 코드: ai/src/dong_stats.py

## AI02-015 대용량 조회
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 선형 탐색 병목 계측·인덱스 검토
- 실제: 50만 행 미존재 키 20회 elapsed=0.168s 회당=8.4ms 결과=None 인덱스없음
- 결함ID: DEF-AI02-015
- 코드: ai/src/dong_stats.py

## AI02-017 JSON 타입 변조
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 구조 검증 필요
- 실제: 통계 최상위 dict 조회 결과 TypeError: string indices must be integers, not 'str'
- 결함ID: DEF-AI02-017
- 코드: ai/src/dong_stats.py

## AI02-018 옵션 JSON 새 버전
- 검증A: pytest = FAIL
- 검증B: 모킹 = NOT_RUN
- 예상: 캐시 무효화/재시작 정책 검증
- 실제: 캐시 후 파일 변경 first=['A'] second=['A']
- 결함ID: DEF-AI02-018
- 코드: ai/src/dong_stats.py
