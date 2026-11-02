"""DE01 소상공인 API·서울시 수집. 네트워크는 mock만 사용한다."""
import io
import zipfile

import pandas as pd
import pytest
import requests

from data.etl import fetch
from data.etl.transform import clean_store


SECRET = "LEAKEDKEY123456789"


def _response(status=200, payload=None, content=b"", json_error=False):
    class Dummy:
        def __init__(self):
            self.status_code = status
            self.content = content
            self.headers = {}

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.HTTPError(f"{self.status_code} Server Error")

        def json(self):
            if json_error:
                raise requests.exceptions.JSONDecodeError("Expecting value", "<html>", 0)
            return payload

    return Dummy()


def _semas_body(code="00", items=None, total=0):
    return {
        "header": {"resultCode": code, "resultMsg": "OK"},
        "body": {"items": [] if items is None else items, "totalCount": total},
    }


def _patch_get(monkeypatch, handler):
    monkeypatch.setattr(fetch, "SERVICE_KEY", "test-key")
    monkeypatch.setattr(fetch.requests, "get", handler)
    monkeypatch.setattr(fetch.time, "sleep", lambda _s: None)


def _zip_bytes(files):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    return buf.getvalue()


def test_DE01_001(monkeypatch):
    monkeypatch.setattr(fetch, "SERVICE_KEY", "")
    with pytest.raises(RuntimeError) as caught:
        fetch.semas_get("/largeUpjongList")
    assert "DATA_GO_KR_KEY" in str(caught.value)


def test_DE01_002(monkeypatch):
    def handler(url, params=None, timeout=None):
        return _response(payload=_semas_body("00", [{"indsLclsCd": "Q"}]))

    _patch_get(monkeypatch, handler)
    body = fetch.semas_get("/largeUpjongList")
    assert body["header"]["resultCode"] == "00"
    assert body["body"]["items"] == [{"indsLclsCd": "Q"}]


def test_DE01_003(monkeypatch):
    def handler(url, params=None, timeout=None):
        return _response(payload=_semas_body("0", [{"ok": 1}]))

    _patch_get(monkeypatch, handler)
    body = fetch.semas_get("/largeUpjongList")
    assert body["body"]["items"] == [{"ok": 1}]


def test_DE01_004(monkeypatch):
    def handler(url, params=None, timeout=None):
        return _response(payload=_semas_body("000", [{"ok": 1}]))

    _patch_get(monkeypatch, handler)
    assert fetch.semas_get("/largeUpjongList")["body"]["items"][0]["ok"] == 1


def test_DE01_005(monkeypatch):
    def handler(url, params=None, timeout=None):
        return _response(payload=_semas_body("03", []))

    _patch_get(monkeypatch, handler)
    with pytest.raises(RuntimeError) as caught:
        fetch.semas_get("/largeUpjongList")
    assert "03" in str(caught.value)


def test_DE01_006(monkeypatch):
    seen = {}

    def handler(url, params=None, timeout=None):
        seen["timeout"] = timeout
        raise requests.Timeout("timed out")

    _patch_get(monkeypatch, handler)
    with pytest.raises(requests.Timeout):
        fetch.semas_get("/largeUpjongList")
    assert seen["timeout"] == 30


def test_DE01_007(monkeypatch):
    def handler(url, params=None, timeout=None):
        return _response(status=500, payload=_semas_body("00"))

    _patch_get(monkeypatch, handler)
    with pytest.raises(requests.HTTPError) as caught:
        fetch.semas_get("/largeUpjongList")
    assert "500" in str(caught.value)


def test_DE01_008(monkeypatch):
    calls = {"n": 0}

    def handler(url, params=None, timeout=None):
        calls["n"] += 1
        if calls["n"] == 1:
            return _response(payload=_semas_body("00", [{"name": "음식"}]))
        return _response(payload=_semas_body("00", [{"name": "한식"}]))

    _patch_get(monkeypatch, handler)
    large, middle = fetch.fetch_semas_upjong()
    assert large == [{"name": "음식"}]
    assert middle == [{"name": "한식"}]
    assert calls["n"] == 2


def test_DE01_009(monkeypatch):
    seen = {}

    def handler(url, params=None, timeout=None):
        seen["params"] = params
        return _response(payload=_semas_body("00", [{"ctyCd": "11440", "ctyNm": "마포구"}]))

    _patch_get(monkeypatch, handler)
    rows = fetch.fetch_semas_dongs()
    assert seen["params"]["ctprvnCd"] == "11"
    assert rows[0]["ctyNm"] == "마포구"


def test_DE01_010(monkeypatch):
    pages = []

    def handler(url, params=None, timeout=None):
        pages.append(params["pageNo"])
        return _response(payload=_semas_body("00", [{"id": params["pageNo"]}], total=999))

    _patch_get(monkeypatch, handler)
    rows = fetch.fetch_semas_stores(max_pages=1)
    assert pages == [1]
    assert len(rows) == 1


def test_DE01_011(monkeypatch):
    pages = []

    def handler(url, params=None, timeout=None):
        pages.append(params["pageNo"])
        return _response(payload=_semas_body("00", [{"id": params["pageNo"]}], total=999))

    _patch_get(monkeypatch, handler)
    rows = fetch.fetch_semas_stores(max_pages=3)
    assert pages == [1, 2, 3]
    assert len(rows) == 3


def test_DE01_012(monkeypatch):
    pages = []

    def handler(url, params=None, timeout=None):
        pages.append(params["pageNo"])
        return _response(payload=_semas_body("00", [{"id": params["pageNo"]}], total=5))

    _patch_get(monkeypatch, handler)
    rows = fetch.fetch_semas_stores(max_pages=3)
    assert pages == [1, 2, 3]
    assert [row["id"] for row in rows] == [1, 2, 3]


def test_DE01_013(monkeypatch):
    pages = []

    def handler(url, params=None, timeout=None):
        pages.append(params["pageNo"])
        return _response(payload=_semas_body("00", [], total=10))

    _patch_get(monkeypatch, handler)
    rows = fetch.fetch_semas_stores(max_pages=3)
    assert rows == []
    assert pages == [1]


def test_DE01_014(monkeypatch):
    pages = []

    def handler(url, params=None, timeout=None):
        pages.append(params["pageNo"])
        return _response(payload=_semas_body("00", [{"id": 1}, {"id": 2}], total=2))

    _patch_get(monkeypatch, handler)
    rows = fetch.fetch_semas_stores(max_pages=3)
    assert len(rows) == 2
    assert pages == [1]


def test_DE01_015(monkeypatch):
    calls = {"n": 0}

    def handler(url, params=None, timeout=None):
        calls["n"] += 1
        return _response(payload=_semas_body("00", [{"id": 1}], total=10))

    _patch_get(monkeypatch, handler)
    assert fetch.fetch_semas_stores(max_pages=0) == []
    assert calls["n"] == 0


def test_DE01_016(monkeypatch):
    calls = {"n": 0}

    def handler(url, params=None, timeout=None):
        calls["n"] += 1
        if calls["n"] == 1:
            return _response(status=429)
        return _response(payload=_semas_body("00", [{"id": 1}]))

    _patch_get(monkeypatch, handler)
    body = fetch.semas_get("/largeUpjongList")
    assert calls["n"] >= 2
    assert body["body"]["items"] == [{"id": 1}]


def test_DE01_017(monkeypatch):
    def handler(url, params=None, timeout=None):
        return _response(content=b"<html>not json</html>", json_error=True)

    _patch_get(monkeypatch, handler)
    with pytest.raises(requests.exceptions.JSONDecodeError):
        fetch.semas_get("/largeUpjongList")


def test_DE01_018(monkeypatch, capsys):
    monkeypatch.setattr(fetch, "SERVICE_KEY", SECRET)

    def handler(url, params=None, timeout=None):
        return _response(
            payload={
                "header": {"resultCode": "03", "resultMsg": f"invalid {SECRET}"},
                "body": {},
            }
        )

    monkeypatch.setattr(fetch.requests, "get", handler)
    fetch_run = __import__("data.etl.run", fromlist=["_try_semas"])
    large, dongs = fetch_run._try_semas()
    logged = capsys.readouterr().out
    assert large == [] and dongs == []
    assert SECRET not in logged


def test_DE01_019(monkeypatch):
    payload = _zip_bytes({"a.csv": "동,값\n연남동,3\n".encode("cp949")})

    def handler(url, params=None, data=None, timeout=None):
        return _response(content=payload)

    monkeypatch.setattr(fetch.requests, "post", handler)
    df = fetch.download_seoul_zip("OA-22172", 5)
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["동"] == "연남동"
    assert len(df) == 1


def test_DE01_020(monkeypatch):
    content = "동,값\n망원동,4\n".encode("cp949")

    def handler(url, params=None, data=None, timeout=None):
        return _response(content=content)

    monkeypatch.setattr(fetch.requests, "post", handler)
    df = fetch.download_seoul_sheet("OA-22178")
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["동"] == "망원동"


def test_DE01_021(monkeypatch):
    def handler(url, params=None, data=None, timeout=None):
        return _response(content=b"this is not a zip")

    monkeypatch.setattr(fetch.requests, "post", handler)
    with pytest.raises(Exception) as caught:
        fetch.download_seoul_zip("OA-22172", 5)
    message = str(caught.value)
    assert "재수집" in message or "다시 받" in message


def test_DE01_022(monkeypatch):
    seen = {}

    def handler(url, params=None, data=None, timeout=None):
        seen["timeout"] = timeout
        raise requests.Timeout("timed out")

    monkeypatch.setattr(fetch.requests, "post", handler)
    with pytest.raises(requests.Timeout):
        fetch.download_seoul_zip("OA-22172", 5)
    assert seen["timeout"] == 120


def test_DE01_023(monkeypatch):
    order = []

    def handler(inf_id, seq):
        order.append(seq)
        return pd.DataFrame({"year_seq": [seq]})

    monkeypatch.setattr(fetch, "download_seoul_zip", handler)
    monkeypatch.setitem(fetch.SEOUL_FILES["store"], "years", {2023: 5, 2024: 6})
    df = fetch.fetch_seoul_table("store")
    assert order == [5, 6]
    assert df["year_seq"].tolist() == [5, 6]


def test_DE01_024():
    with pytest.raises(KeyError) as caught:
        fetch.fetch_seoul_table("wrong")
    assert "wrong" in str(caught.value)


def test_DE01_025():
    raw = pd.DataFrame(
        [
            {
                "기준_년분기_코드": "20242",
                "행정동_코드": "11440740",
                "행정동_코드_명": "연남동",
                "서비스_업종_코드": "CS100001",
                "서비스_업종_코드_명": "한식음식점",
                "점포_수": "10",
                "개업_율": "1",
                "개업_점포_수": "1",
                "폐업_률": "1",
                "폐업_점포_수": "1",
                "프랜차이즈_점포_수": "1",
            },
            {
                "기준_년분기_코드": "20242",
                "행정동_코드": "26110510",
                "행정동_코드_명": "부산동",
                "서비스_업종_코드": "CS100001",
                "서비스_업종_코드_명": "한식음식점",
                "점포_수": "8",
                "개업_율": "1",
                "개업_점포_수": "1",
                "폐업_률": "1",
                "폐업_점포_수": "1",
                "프랜차이즈_점포_수": "1",
            },
        ]
    )
    df = clean_store(raw)
    assert len(df) == 1
    assert df.iloc[0]["district"] == "마포구"
    assert "26110510" not in set(df["dong_code"])


def test_DE01_026(monkeypatch):
    html = b"<html><body>redirected</body></html>"

    def handler(url, params=None, data=None, timeout=None):
        response = _response(content=html)
        response.headers["Content-Type"] = "text/html"
        return response

    monkeypatch.setattr(fetch.requests, "post", handler)
    with pytest.raises(Exception) as caught:
        fetch.download_seoul_zip("OA-22172", 5)
    message = str(caught.value)
    assert "파일" in message and ("타입" in message or "형식" in message)
