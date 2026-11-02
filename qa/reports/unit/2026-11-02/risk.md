# RISK

## 20261102-201533

- 실행 시각: 2026-11-02T20:15:33+0900
- Git Commit: 4c28384-dirty

### RISK-20261102-201533-1 MEDIUM OPEN

- 기능: 프론트 타입
- 관련 TC_ID: TC-UNIT-FRONT-001
- 발생 가능성: 높음
- 영향: 타입 오류가 있으면 빌드 스크립트 tsc --noEmit이 배포를 막거나, 검사를 빼면 타입 회귀가 남는다.
- 내용: src/test/FE01_routing.test.tsx(1,30): error TS2307: Cannot find module 'node:fs' or its corresponding type declarations.
- 권장 조치: node 타입 선언을 테스트 범위에 포함하고 tsc를 다시 실행한다.
- 처리 상태: OPEN
- 파일: front/src/test/FE01_routing.test.tsx
- 함수: UNKNOWN
- 줄 번호: 1

## 20261102-201658

- 실행 시각: 2026-11-02T20:16:58+0900
- Git Commit: 4c28384-dirty
이 RUN에서 새 위험은 없다.

## 20261102-201740

- 실행 시각: 2026-11-02T20:17:40+0900
- Git Commit: 4c28384-dirty
이 RUN에서 새 위험은 없다.

## 상태 변경

- RISK-20261102-201533-1: OPEN에서 MITIGATED로 변경. 행은 유지한다.
- 근거: RUN 20261102-201740 도구 B `npx tsc --noEmit` PASS. `front` 개발 의존성에 `@types/node`를 두고 `front/tsconfig.json`의 `types`에 `node`를 넣었다.
- RUN 20261102-201658의 도구 B PASS는 채택하지 않는다. 그때 타입 해석이 저장소 루트에 잠시 생긴 `node_modules`를 사용했다. 그 파일은 삭제했다.

## 20261102-221207

- 실행 시각: 2026-11-02T22:12:07+0900
- Git Commit: 4c28384-dirty
이 RUN에서 새 위험은 없다.
