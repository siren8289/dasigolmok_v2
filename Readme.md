# dasiGolmok v2

서울 골목 상권의 **폐업 위험**을 진단하고, **같은 동의 업종**을 추천하는 서비스입니다.
공공데이터 5개를 모아 전처리하고, 머신러닝·딥러닝·LLM을 모두 사용합니다.

## 메인 기능 2개

| 기능 | 하는 일 | 사용 기술 |
| --- | --- | --- |
| 1. 골목 상권 진단 | 행정동+업종을 고르면 최근 폐업률로 위험 단계를 나누고, AI 예상 폐업률·매출과 쉬운 설명을 보여 줌 | 규칙 + **ML** + **DL** + **LLM** |
| 2. 업종 추천 | 같은 동의 업종을 전부 예측해서, 폐업률이 낮고 매출이 나은 순으로 추천 | **ML** + **DL** |

- 폐업률 4% 이하 + 축소 아님 `안정` / 4% 이상 또는 다이나믹 `주의` / 8% 이상 또는 상권축소 `위험`

## 폴더 구조

```text
dasigolmok_v2/
├── data/                  공공데이터 수집·전처리
│   ├── etl/
│   │   ├── config.py      API 주소, 자치구 코드
│   │   ├── fetch.py       1단계: API/파일에서 받아 오기
│   │   ├── transform.py   2단계: 전처리
│   │   ├── load.py        3단계: CSV/JSON 저장
│   │   └── run.py         전체 실행
│   ├── raw/               원본 (git 제외)
│   ├── processed/         전처리 결과
│   └── tests/
├── ai/                    AI 서버 (FastAPI, Python)
│   ├── train/             ML·DL 학습
│   ├── models/            학습된 모델
│   └── src/               예측, 규칙, LLM 설명
├── back/                  백엔드 (Spring Boot, Java)
│   └── src/main/java/com/dasigolmok/
│       ├── diagnosis/     기능 1: 진단
│       ├── recommend/     기능 2: 추천
│       ├── ai/            AI 서버 호출
│       └── global/
├── front/                 프론트 (React + Vite, TypeScript)
│   └── src/pages/         진단 입력, 결과, 추천
├── compose.yaml
└── .env.example
```

데이터 흐름: `공공데이터 → data(전처리) → ai(학습) → ai 서버 ← back(Spring) ← front(Vite)`

## 사용한 공공데이터 5개

| # | 데이터 | 용도 |
| --- | --- | --- |
| 1 | 소상공인시장진흥공단 상가(상권)정보 API | 업종 코드, 서울 행정동, 샘플 업소 |
| 2 | 서울시 상권분석서비스(점포-행정동) | 점포 수, 개업/폐업 |
| 3 | 서울시 상권분석서비스(추정매출-행정동) | 점포당 매출 학습 |
| 4 | 서울시 상권분석서비스(길단위인구-행정동) | 유동인구 |
| 5 | 서울시 상권분석서비스(상권변화지표-행정동) | 상권 축소/확장 |

### 전처리 순서 (`data/etl/transform.py`)

1. 숫자 문자열 정리 (`"1,000"` → `1000`)
2. 컬럼 이름 통일, 서울만 남기기
3. 결측치 채우기 (같은 업종 중앙값)
4. 파생 변수 (점포당 매출, 자치구, 프랜차이즈 비율)
5. 이상치 제거 (업종별 상하위 1%)
6. 점포 + 매출 + 유동인구 + 변화지표 결합

## AI 모델

| 구분 | 모델 | 예측값 |
| --- | --- | --- |
| ML | 랜덤포레스트 | 폐업률(%) |
| DL | PyTorch MLP | 점포당 매출(만원) |
| LLM | Google Gemini (키 없으면 기본 문장) | 쉬운 설명 |

## 로컬 실행

```bash
cp .env.example .env
# .env 에 DATA_GO_KR_KEY, DB_PASSWORD 를 넣는다.

# 1) 데이터
python -m data.etl.run

# 2) 학습
python -m ai.train.train_ml
python -m ai.train.train_dl

# 3) AI
cd ai && python -m uvicorn src.main:app --reload --port 8000

# 4) Spring
cd back && ./gradlew bootRun

# 5) Vite
cd front && npm install && npm run dev
```

브라우저: http://localhost:5173

또는 한 번에: `cp .env.example .env` 후 `docker compose up --build` → http://localhost

GitHub Actions: `data` / `ai` / `back` / `front` 테스트를 돌리고, `main` 푸시 때 `docker compose build` 까지 확인합니다.

예전 포트폴리오 글(Materialized View)은 `docs/portfolio-materialized-view.md` 에 두었습니다.
