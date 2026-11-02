# RISK / NOT_RUN

실행일: 2026-11-02. 검증B를 실행하지 않은 항목은 PASS로 올리지 않는다.

| TC ID | 기능 | 항목 | 검증A | 검증A결과 | 검증B | 검증B결과 | 최종 |
|---|---|---|---|---|---|---|---|
| AI04-001 | 행정동 업종 추천 | 동 업종 목록 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-002 | 행정동 업종 추천 | 동 데이터 없음 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-003 | 행정동 업종 추천 | 특성 행합치기 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-004 | 행정동 업종 추천 | ML 예측 매핑 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-005 | 행정동 업종 추천 | DL 예측 매핑 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-006 | 행정동 업종 추천 | 추천 점수 공식 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-007 | 행정동 업종 추천 | 추천 점수 공식 2 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-008 | 행정동 업종 추천 | 추천 점수 공식 경계 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-009 | 행정동 업종 추천 | 소수 점수 반올림 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-010 | 행정동 업종 추천 | 점수 내림차순 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-011 | 행정동 업종 추천 | 상위 5 제한 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-012 | 행정동 업종 추천 | 전체 업종 유지 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-013 | 행정동 업종 추천 | 업종 1개 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-014 | 행정동 업종 추천 | 업종 5개 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-015 | 행정동 업종 추천 | 업종 6개 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-016 | 행정동 업종 추천 | 예상 폐업률 기준 상태 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-017 | 행정동 업종 추천 | 실제 폐업률 보존 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-018 | 행정동 업종 추천 | 상권 축소 우선 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-019 | 행정동 업종 추천 | 변화명 대표값 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-020 | 행정동 업종 추천 | 원본 행 순서 변화 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-024 | 행정동 업종 추천 | limit=0 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-026 | 행정동 업종 추천 | limit=10000 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |
| AI04-027 | 행정동 업종 추천 | 동시 추천 | pytest | PASS | 모킹 | NOT_RUN | NOT_RUN |

## AI04-001 동 업종 목록
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 입력=7 ml_rows=7 dl_rows=7 all=7 rec=5

## AI04-002 동 데이터 없음
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 빈 동 결과={'error': '해당 행정동 데이터가 없습니다.', 'recommendations': []}

## AI04-003 특성 행합치기
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ML/DL 입력 shape=(3, 8) columns=['district', 'industry', 'change_code', 'store_count', 'open_rate', 'franchise_ratio', 'foot_traffic', 'operate_months']

## AI04-004 ML 예측 매핑
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: ML 매핑={'업종0': 3, '업종1': 5, '업종2': 8}

## AI04-005 DL 예측 매핑
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: DL 매핑={'업종0': 1000, '업종1': 800, '업종2': 600}

## AI04-006 추천 점수 공식
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: sales=1000 close=3 score=-14.0 기대=-14.0

## AI04-007 추천 점수 공식 2
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: sales=1500 close=1 score=7.0 기대=7.0

## AI04-008 추천 점수 공식 경계
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 영 입력 점수 sales=0 close=0 score=0.0

## AI04-009 소수 점수 반올림
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 소수 반올림 sales=999.5 close=3.33 score=-16.6 round1=-16.6

## AI04-010 점수 내림차순
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 입력 score 대응 sales 900/100/500 → 정렬 [9.0, 5.0, 1.0]

## AI04-011 상위 5 제한
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 추천 건수 recommendations=5 all=7

## AI04-012 전체 업종 유지
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 전체 업종 수 all_industries=7

## AI04-013 업종 1개
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 추천과 전체 rec=1 all=1

## AI04-014 업종 5개
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 기본 상한 rec=5

## AI04-015 업종 6개
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 추천과 전체 rec=5 all=6

## AI04-016 예상 폐업률 기준 상태
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 실제 close_rate=1 ml=9 status=danger

## AI04-017 실제 폐업률 보존
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 반환 폐업률 close_rate=2.3

## AI04-018 상권 축소 우선
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 축소 상권 판정 change=HL ml=1 status=danger

## AI04-019 변화명 대표값
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 반환 change_name='첫변화' 추천1=높음

## AI04-020 원본 행 순서 변화
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 정렬=[('A', 9.0), ('B', 5.0), ('C', 1.0)]

## AI04-024 limit=0
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 상한 0건 rec=[] all=3

## AI04-026 limit=10000
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 추천과 전체 rec=4 all=4

## AI04-027 동시 추천
- 상태: 검증A PASS / 검증B NOT_RUN / 최종 NOT_RUN
- 내용: 검증A는 통과했다. 검증B는 실행하지 않아 최종 PASS가 아니다.
- 실제: 병렬 dong=['연남동', '역삼1동'] district=['마포구', '강남구'] 순차와동일=True
