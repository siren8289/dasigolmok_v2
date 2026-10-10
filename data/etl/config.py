"""데이터 수집 설정값을 한 곳에 모아 둔다.

사용하는 공공데이터 5개
  1. 소상공인시장진흥공단 상가(상권)정보 API  → 업종 코드, 서울 행정동, 샘플 업소
  2. 서울시 상권분석서비스(점포-행정동)       → 점포 수, 개업/폐업
  3. 서울시 상권분석서비스(추정매출-행정동)   → 추정 매출
  4. 서울시 상권분석서비스(길단위인구-행정동) → 유동인구
  5. 서울시 상권분석서비스(상권변화지표-행정동) → 상권 축소/확장
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# data/ 폴더 위치. 어디서 실행해도 같은 폴더를 가리키도록 파일 기준으로 계산한다.
DATA_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = DATA_DIR / "raw"              # API/파일 원본
PROCESSED_DIR = DATA_DIR / "processed"  # 전처리가 끝난 CSV

# data/.env 또는 저장소 루트 .env 에서 인증키를 읽는다. (.env 는 git에 올리지 않는다)
load_dotenv(DATA_DIR / ".env")
load_dotenv(DATA_DIR.parent / ".env")
SERVICE_KEY = os.getenv("DATA_GO_KR_KEY", "")

# 1) 소상공인시장진흥공단 상가(상권)정보 API
SEMAS_BASE = "https://apis.data.go.kr/B553077/api/open/sdsc2"
SEMAS_ENDPOINTS = {
    "large_upjong": "/largeUpjongList",   # 업종 대분류
    "middle_upjong": "/middleUpjongList",  # 업종 중분류
    "dong": "/baroApi",                    # 행정동
    "stores": "/storeListInDong",          # 행정동 단위 업소
}

# 서울 열린데이터광장 파일 다운로드
# zip: 연도별 압축 파일 / sheet: 시트 전체를 CSV로 받기
SEOUL_DOWNLOAD = "https://datafile.seoul.go.kr/bigfile/iot"
SEOUL_FILES = {
    "store": {
        "name": "점포-행정동",
        "inf_id": "OA-22172",
        "kind": "zip",
        # seq 번호는 서울 열린데이터광장 파일 목록과 같다. (2023=5, 2024=6, 2025=7)
        "years": {2023: 5, 2024: 6, 2025: 7},
    },
    "sales": {
        "name": "추정매출-행정동",
        "inf_id": "OA-22175",
        "kind": "zip",
        "years": {2023: 5, 2024: 6, 2025: 7},
    },
    "pop": {
        "name": "길단위인구-행정동",
        "inf_id": "OA-22178",
        "kind": "sheet",
    },
    "change": {
        "name": "상권변화지표-행정동",
        "inf_id": "OA-15575",
        "kind": "sheet",
    },
}

# 서울 25개 자치구. 행정동 코드 앞 5자리가 이 값이다.
SEOUL_DISTRICTS = {
    "11110": "종로구", "11140": "중구", "11170": "용산구", "11200": "성동구",
    "11215": "광진구", "11230": "동대문구", "11260": "중랑구", "11290": "성북구",
    "11305": "강북구", "11320": "도봉구", "11350": "노원구", "11380": "은평구",
    "11410": "서대문구", "11440": "마포구", "11470": "양천구", "11500": "강서구",
    "11530": "구로구", "11545": "금천구", "11560": "영등포구", "11590": "동작구",
    "11620": "관악구", "11650": "서초구", "11680": "강남구", "11710": "송파구",
    "11740": "강동구",
}

# 상권변화지표 코드 → 쉬운 이름
CHANGE_NAMES = {
    "HH": "정체",
    "HL": "상권축소",
    "LH": "상권확장",
    "LL": "다이나믹",
}

# SEMAS 샘플 업소를 받아 올 행정동 (역삼1동). 전체 426동을 다 받으면 API 한도가 부담된다.
SAMPLE_DONG_CODE = "11680640"
