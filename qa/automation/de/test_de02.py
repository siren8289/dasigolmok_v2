"""DE02 ZIP·CSV 인코딩. 파일은 메모리에서만 만든다."""
import io
import zipfile

import pandas as pd
import pytest

from data.etl.fetch import _read_csv_bytes, _read_zip_csv


def _zip_bytes(files):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    return buf.getvalue()


def test_DE02_001():
    raw = "동,값\n연남동,1\n".encode("cp949")
    df = _read_csv_bytes(raw)
    assert df.iloc[0]["동"] == "연남동"
    assert int(df.iloc[0]["값"]) == 1


def test_DE02_002(monkeypatch):
    tried = []
    real = pd.read_csv

    def wrapped(buf, encoding=None, **kwargs):
        tried.append(encoding)
        return real(buf, encoding=encoding, **kwargs)

    monkeypatch.setattr("data.etl.fetch.pd.read_csv", wrapped)
    raw = "동,값\n연남동,1\n".encode("utf-8-sig")
    df = _read_csv_bytes(raw)
    assert tried[0] == "cp949"
    assert "utf-8-sig" in tried
    assert df.iloc[0]["동"] == "연남동"


def test_DE02_003():
    raw = "동,값\n망원동,2\n".encode("utf-8")
    df = _read_csv_bytes(raw)
    assert df.iloc[0]["동"] == "망원동"
    assert len(df) == 1


def test_DE02_004():
    with pytest.raises(RuntimeError) as caught:
        _read_csv_bytes(bytes([0xFF, 0xFE, 0x00, 0x80]))
    assert "글자 코드" in str(caught.value)


def test_DE02_005():
    with pytest.raises(Exception) as caught:
        _read_csv_bytes(b"")
    assert type(caught.value).__name__ in {"EmptyDataError", "RuntimeError"}


def test_DE02_006():
    df = _read_csv_bytes("a,b\n".encode("cp949"))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
    assert list(df.columns) == ["a", "b"]


def test_DE02_007():
    raw = _zip_bytes({"only.csv": "동,값\n연남동,1\n".encode("cp949")})
    df = _read_zip_csv(raw)
    assert df.iloc[0]["동"] == "연남동"
    assert len(df) == 1


def test_DE02_008():
    raw = _zip_bytes(
        {
            "first.csv": "동,값\n첫번째,1\n".encode("cp949"),
            "second.csv": "동,값\n두번째,2\n".encode("cp949"),
        }
    )
    df = _read_zip_csv(raw)
    assert len(df) == 1
    assert df.iloc[0]["동"] == "첫번째"


def test_DE02_009():
    raw = _zip_bytes({"note.txt": b"hello"})
    with pytest.raises(Exception) as caught:
        _read_zip_csv(raw)
    assert not isinstance(caught.value, StopIteration)
    assert "csv" in str(caught.value).lower()


def test_DE02_010():
    raw = _zip_bytes({"reports/data.csv": "동,값\n합정동,9\n".encode("cp949")})
    df = _read_zip_csv(raw)
    assert df.iloc[0]["동"] == "합정동"


def test_DE02_011():
    raw = '이름,메모\n카페,"=HYPERLINK(""http://evil"")"\n'.encode("cp949")
    df = _read_csv_bytes(raw)
    value = str(df.iloc[0]["메모"])
    assert not value.startswith("="), f"수식 셀이 실행 가능한 원문으로 남음: {value}"


def test_DE02_012():
    raw = '업종,값\n"카페,음료",1\n'.encode("cp949")
    df = _read_csv_bytes(raw)
    assert df.iloc[0]["업종"] == "카페,음료"
    assert len(df.columns) == 2


def test_DE02_013():
    raw = '업종,값\n"두\n줄",2\n'.encode("cp949")
    df = _read_csv_bytes(raw)
    assert len(df) == 1
    assert df.iloc[0]["업종"] == "두\n줄"


def test_DE02_014():
    raw = "code,name\n01100000,테스트\n".encode("cp949")
    df = _read_csv_bytes(raw)
    assert str(df.iloc[0]["code"]) == "01100000"
    assert not isinstance(df.iloc[0]["code"], (int, float))


def test_DE02_015():
    raw = _zip_bytes({})
    with pytest.raises(Exception) as caught:
        _read_zip_csv(raw)
    message = str(caught.value).strip()
    assert message
    assert not isinstance(caught.value, StopIteration)
    assert "csv" in message.lower() or "zip" in message.lower()


def test_DE02_016():
    raw_csv = b"c1,c2\n" + b"9,9\n" * 100_000
    try:
        df = _read_zip_csv(_zip_bytes({"big.csv": raw_csv}))
    except RuntimeError as error:
        assert any(token in str(error) for token in ("크기", "제한", "size", "limit"))
    else:
        pytest.fail(f"압축해제 {len(raw_csv)}바이트를 크기 제한 없이 읽음 rows={len(df)}")


def test_DE02_017():
    import warnings

    text = "기준_년분기_코드,행정동_코드,폐업율\n20242,11440740,5\n"
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        df = _read_csv_bytes(text.encode("cp949"))
    notes = " ".join(str(item.message) for item in caught)
    assert ("폐업_률" in df.columns) or ("스키마" in notes), (
        f"폐업율 컬럼을 경고 없이 읽음 columns={list(df.columns)}"
    )


def test_DE02_018(monkeypatch):
    from data.etl.fetch import download_seoul_sheet

    html = b"<html><body>not a csv</body></html>"

    class Dummy:
        status_code = 200
        content = html
        headers = {"Content-Type": "text/html"}

        def raise_for_status(self):
            return None

    monkeypatch.setattr("data.etl.fetch.requests.post", lambda *a, **k: Dummy())
    with pytest.raises(Exception) as caught:
        download_seoul_sheet("OA-22178")
    message = str(caught.value)
    assert "HTML" in message or "html" in message or "형식" in message
