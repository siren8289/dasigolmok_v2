"""1단계: 공공데이터 API/파일에서 데이터를 받아 온다.

- 소상공인 API: JSON
- 서울시 파일: zip(CSV) 또는 시트 CSV (글자 깨짐 방지를 위해 cp949로 읽는다)
"""
import io
import time
import zipfile

import pandas as pd
import requests

from data.etl.config import (
    SAMPLE_DONG_CODE,
    SEMAS_BASE,
    SEMAS_ENDPOINTS,
    SEOUL_DOWNLOAD,
    SEOUL_FILES,
    SERVICE_KEY,
)


def semas_get(path, extra=None):
    """소상공인 API 한 번 호출. 실패하면 이유를 바로 보여 준다."""
    if not SERVICE_KEY:
        raise RuntimeError("data/.env 또는 루트 .env 에 DATA_GO_KR_KEY 를 넣어 주세요.")

    params = {"serviceKey": SERVICE_KEY, "type": "json"}
    if extra:
        params.update(extra)

    response = requests.get(SEMAS_BASE + path, params=params, timeout=30)
    response.raise_for_status()
    body = response.json()
    header = body.get("header", {})
    if str(header.get("resultCode")) not in ("00", "0", "000"):
        raise RuntimeError(f"소상공인 API 오류: {header}")
    return body


def fetch_semas_upjong():
    """업종 대분류 + 중분류 목록."""
    large = semas_get(SEMAS_ENDPOINTS["large_upjong"])
    middle = semas_get(SEMAS_ENDPOINTS["middle_upjong"])
    return large["body"]["items"], middle["body"]["items"]


def fetch_semas_dongs():
    """서울 25개 자치구 목록. (baroApi)

    행정동 단위 코드는 이 API 파라미터 조합이 자주 바뀌어,
    행정동 이름은 서울시 점포/변화지표 파일에서 가져온다.
    """
    districts = semas_get(
        SEMAS_ENDPOINTS["dong"],
        {"resId": "dong", "catId": "cty", "ctprvnCd": "11"},
    )["body"]["items"]
    return districts


def fetch_semas_stores(dong_code=SAMPLE_DONG_CODE, max_pages=3):
    """한 행정동의 업소 목록. (페이지를 조금만 받아서 샘플로 쓴다)"""
    rows = []
    page = 1
    while page <= max_pages:
        body = semas_get(
            SEMAS_ENDPOINTS["stores"],
            {"divId": "adongCd", "key": dong_code, "numOfRows": 100, "pageNo": page},
        )
        items = body["body"].get("items", [])
        rows.extend(items)
        total = int(body["body"].get("totalCount") or 0)
        if len(rows) >= total or not items:
            break
        page += 1
        time.sleep(0.1)
    return rows


def _read_csv_bytes(raw):
    """서울시 CSV는 보통 cp949 이다. 안 되면 utf-8 로 다시 시도한다."""
    for encoding in ("cp949", "utf-8-sig"):
        try:
            return pd.read_csv(io.BytesIO(raw), encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError("CSV 글자 코드를 알 수 없습니다.")


def _read_zip_csv(raw):
    """zip 안에 들어 있는 첫 번째 CSV를 표로 읽는다."""
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        name = next(n for n in archive.namelist() if n.lower().endswith(".csv"))
        return _read_csv_bytes(archive.read(name))


def download_seoul_zip(inf_id, seq):
    """서울 열린데이터광장 연도별 zip 파일을 받는다."""
    url = f"{SEOUL_DOWNLOAD}/inf/nio_download.do"
    response = requests.post(
        url,
        params={"useCache": "false"},
        data={"infId": inf_id, "seqNo": "", "seq": str(seq), "infSeq": "3"},
        timeout=120,
    )
    response.raise_for_status()
    return _read_zip_csv(response.content)


def download_seoul_sheet(inf_id):
    """서울 열린데이터광장 시트 전체를 CSV로 받는다."""
    url = f"{SEOUL_DOWNLOAD}/sheet/csv/download.do"
    response = requests.post(
        url,
        data={"infId": inf_id, "infSeq": "1", "serviceKind": "1", "download": "true"},
        timeout=120,
    )
    response.raise_for_status()
    return _read_csv_bytes(response.content)


def fetch_seoul_table(key):
    """SEOUL_FILES 의 키(store/sales/pop/change)에 맞는 표를 받는다.

    zip 은 여러 해를 이어 붙인다.
    """
    spec = SEOUL_FILES[key]
    if spec["kind"] == "sheet":
        print(f"  다운로드: {spec['name']}")
        return download_seoul_sheet(spec["inf_id"])

    parts = []
    for year, seq in spec["years"].items():
        print(f"  다운로드: {spec['name']} {year}")
        parts.append(download_seoul_zip(spec["inf_id"], seq))
    return pd.concat(parts, ignore_index=True)
