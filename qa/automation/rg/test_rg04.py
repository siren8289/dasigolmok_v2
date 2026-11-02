"""RG04 지원 정책 규칙."""
from datetime import datetime

import pytest

from rg_support import raw_policy
from src.features.commercial_rag_001.schemas import SupportPolicyQuery
from src.features.commercial_rag_001.support_policy.service import check_policy_status, search_policies


TARGET = "2026-11-02"


class Clock(datetime):
    current = datetime(2026, 11, 2)

    @classmethod
    def now(cls, tz=None):
        return cls.current


def _search(**kwargs):
    payload = dict(query="", target_date=TARGET, only_open=True, top_k=10)
    payload.update(kwargs)
    return search_policies(SupportPolicyQuery(**payload))


def test_RG04_001():
    """기준일 2026-11-02, 시작 2026-12-01 은 upcoming, false 이다."""
    assert check_policy_status("2026-12-01", "2026-12-31", TARGET) == ("upcoming", False)


def test_RG04_002():
    """시작 당일 2026-11-02 는 open, true 이다."""
    assert check_policy_status("2026-11-02", "2026-12-31", TARGET) == ("open", True)


def test_RG04_003():
    """기간 중간 2026-11-02 는 open, true 이다."""
    assert check_policy_status("2026-01-01", "2026-12-31", TARGET) == ("open", True)


def test_RG04_004():
    """마감 당일 2026-11-02 는 open, true 이다."""
    assert check_policy_status("2026-01-01", "2026-11-02", TARGET) == ("open", True)


def test_RG04_005():
    """마감 다음날 기준 2026-11-02, 종료 2026-11-01 은 closed, false 이다."""
    assert check_policy_status("2026-01-01", "2026-11-01", TARGET) == ("closed", False)


def test_RG04_006():
    """2024-06-30 종료 사업은 기준일 2026-11-02 에 closed, false 이다."""
    assert check_policy_status("2024-01-15", "2024-06-30", TARGET) == ("closed", False)


def test_RG04_007():
    """마감일 형식 오류는 closed, false 이다."""
    assert check_policy_status("2026-01-01", "2026/12/31", TARGET) == ("closed", False)


def test_RG04_008():
    """시작일 형식 오류는 closed, false 이다."""
    assert check_policy_status("2026/01/01", "2026-12-31", TARGET) == ("closed", False)


def test_RG04_009():
    """기준일 2026/11/02 는 오류로 알리고 오늘 날짜로 오판하면 안 된다."""
    try:
        result = check_policy_status("2026-01-01", "2026-12-31", "2026/11/02")
    except ValueError:
        return
    pytest.fail(f"기준일 2026/11/02 가 오류 없이 {result}로 판정됨")


def test_RG04_010(monkeypatch):
    """target_date 가 없으면 시스템 오늘(2026-11-02)로 판정한다."""
    import src.features.commercial_rag_001.support_policy.service as policy_svc

    Clock.current = datetime(2026, 11, 2)
    monkeypatch.setattr(policy_svc, "datetime", Clock)
    assert check_policy_status("2026-11-02", "2026-12-31", None) == ("open", True)
    assert check_policy_status("2026-12-01", "2026-12-31", None) == ("upcoming", False)


def test_RG04_011():
    """only_open=True, 기준 2026-11-02 는 마감 공고를 제외한다."""
    response = _search(only_open=True)
    ids = {item.id for item in response.policies}
    assert "pol-seoul-smart-store-2026" not in ids
    assert "pol-seoul-closed-special-2024" not in ids
    assert "pol-mapo-closed-localbrand-2025" not in ids
    assert all(item.is_open for item in response.policies)


def test_RG04_012():
    """only_open=False 는 마감 상태를 표기한 채 종료 공고를 포함한다."""
    response = _search(only_open=False)
    closed = [item for item in response.policies if item.id == "pol-seoul-closed-special-2024"]
    assert closed
    assert closed[0].status == "closed" and closed[0].is_open is False


def test_RG04_013(monkeypatch):
    """only_open=True 는 시작 전 예정 공고를 제외한다."""
    import src.features.commercial_rag_001.support_policy.service as policy_svc

    monkeypatch.setattr(
        policy_svc,
        "POLICY_DATABASE",
        [raw_policy(id="future", title="예정사업", start_date="2026-12-01", end_date="2026-12-31")],
    )
    response = _search(only_open=True)
    assert all(item.id != "future" for item in response.policies)


def test_RG04_014():
    """대상 지역이 없는 서울 전역 공고는 마포구 조회에 포함된다."""
    response = _search(district="마포구")
    matched = [item for item in response.policies if item.id == "pol-seoul-safe-loan-2026"]
    assert matched
    assert matched[0].target_district is None


def test_RG04_015():
    """마포구 지정 공고는 마포구 조회에 포함된다."""
    response = _search(district="마포구")
    assert any(item.id == "pol-mapo-youth-startup-2026" for item in response.policies)


def test_RG04_016():
    """마포구 조회에서 강남구 공고는 제외된다."""
    response = _search(district="마포구")
    assert all(item.id != "pol-gangnam-incubating-2026" for item in response.policies)


def test_RG04_017():
    """업종 제한이 없는 공고는 한식음식점 조회에 포함된다."""
    response = _search(industry="한식음식점")
    assert any(item.target_industry is None for item in response.policies)
    assert any(item.id == "pol-seoul-safe-loan-2026" for item in response.policies)


def test_RG04_018():
    """커피-음료는 마포 청년창업 대상 업종에 포함된다."""
    response = _search(district="마포구", industry="커피-음료")
    assert any(item.id == "pol-mapo-youth-startup-2026" for item in response.policies)


def test_RG04_019():
    """학원은 마포 청년창업 대상 업종이 아니므로 제외된다."""
    response = _search(industry="학원")
    assert all(item.id != "pol-mapo-youth-startup-2026" for item in response.policies)


def test_RG04_020(monkeypatch):
    """자치구가 맞는 정책 점수는 전역 정책보다 0.5 높다."""
    import src.features.commercial_rag_001.support_policy.service as policy_svc

    monkeypatch.setattr(
        policy_svc,
        "POLICY_DATABASE",
        [
            raw_policy(id="local", title="지역", target_district="마포구"),
            raw_policy(id="wide", title="전역", target_district=None),
        ],
    )
    response = _search(query="", district="마포구")
    scores = {item.id: item.score for item in response.policies}
    assert scores["local"] - scores["wide"] == pytest.approx(0.5)


def test_RG04_021(monkeypatch):
    """업종이 맞는 정책 점수는 전업종 정책보다 0.5 높다."""
    import src.features.commercial_rag_001.support_policy.service as policy_svc

    monkeypatch.setattr(
        policy_svc,
        "POLICY_DATABASE",
        [
            raw_policy(id="fit", title="맞춤", target_industry="한식음식점"),
            raw_policy(id="any", title="전업종", target_industry=None),
        ],
    )
    response = _search(query="", industry="한식음식점")
    scores = {item.id: item.score for item in response.policies}
    assert scores["fit"] - scores["any"] == pytest.approx(0.5)


def test_RG04_022(monkeypatch):
    """쿼리 토큰 1개 일치는 점수 0.3 을 더한다."""
    import src.features.commercial_rag_001.support_policy.service as policy_svc

    monkeypatch.setattr(
        policy_svc,
        "POLICY_DATABASE",
        [
            raw_policy(id="hit", title="청년창업 지원", description="설명"),
            raw_policy(id="miss", title="무관문구", description="설명"),
        ],
    )
    response = _search(query="청년창업")
    scores = {item.id: item.score for item in response.policies}
    assert scores["hit"] - scores["miss"] == pytest.approx(0.3)


def test_RG04_023(monkeypatch):
    """점수가 높은 자치구 맞춤 정책이 앞에 온다."""
    import src.features.commercial_rag_001.support_policy.service as policy_svc

    monkeypatch.setattr(
        policy_svc,
        "POLICY_DATABASE",
        [
            raw_policy(id="wide", title="전역"),
            raw_policy(id="local", title="지역", target_district="마포구"),
        ],
    )
    response = _search(query="", district="마포구")
    assert [item.id for item in response.policies][0] == "local"
    assert response.policies[0].score >= response.policies[1].score


def test_RG04_024():
    """top_k=1 은 정책 1건만 반환한다."""
    response = _search(top_k=1)
    assert len(response.policies) == 1
    assert response.total_count == 1


def test_RG04_025():
    """top_k=5 는 5건 이하다."""
    response = _search(top_k=5)
    assert 1 <= len(response.policies) <= 5
    assert response.total_count == len(response.policies)


def test_RG04_026():
    """top_k=-1 은 마지막 항목을 잘라 반환하면 안 된다."""
    full = _search(only_open=False, top_k=100)
    try:
        bad = _search(only_open=False, top_k=-1)
    except (ValueError, TypeError):
        return
    pytest.fail(f"top_k=-1 이 검증 없이 {len(bad.policies)}건 반환(전체 {len(full.policies)})")


def test_RG04_027():
    """top_k=0 은 빈 배열이다."""
    response = _search(top_k=0)
    assert response.policies == []
    assert response.total_count == 0


def test_RG04_028():
    """정책 원천은 공식 공고 확인 전 실시간 단정 표시가 없어야 한다."""
    response = _search(query="안심창업", top_k=5)
    blob = response.model_dump_json()
    if not any(token in blob for token in ("미검증", "표본", "샘플", "미확인", "예시")):
        pytest.fail("정책 검색 결과에 공식 공고 미확인 표시가 없음")


def test_RG04_029():
    """접수 중 정책 결과에 예산 소진·출처 최신 확인 경고가 있어야 한다."""
    response = _search(query="안심창업", only_open=True, top_k=5)
    assert any(item.is_open for item in response.policies)
    blob = response.model_dump_json()
    if "예산" not in blob and "소진" not in blob and "최신" not in blob:
        pytest.fail("접수중 정책 결과에 예산 소진·출처 최신 확인 경고가 없음")


def test_RG04_030():
    """시작일 2026-12-31, 종료일 2026-01-01 역전 범위는 차단되어야 한다."""
    try:
        result = check_policy_status("2026-12-31", "2026-01-01", TARGET)
    except ValueError:
        return
    if result[0] in {"invalid", "error"}:
        return
    pytest.fail(f"시작>종료 범위가 {result}로 통과함")


def test_RG04_031(monkeypatch):
    """같은 id 정책 2건은 1건으로 정리되어야 한다."""
    import src.features.commercial_rag_001.support_policy.service as policy_svc

    monkeypatch.setattr(
        policy_svc,
        "POLICY_DATABASE",
        [
            raw_policy(id="same", title="동일제목"),
            raw_policy(id="same", title="동일제목"),
        ],
    )
    response = _search(top_k=5)
    count = [item.id for item in response.policies].count("same")
    if count != 1:
        pytest.fail(f"동일 id 정책이 {count}건 반환됨")


def test_RG04_032(monkeypatch):
    """Asia/Seoul 2026-11-02 00:00 이면 종료일 2026-11-01 정책은 closed 여야 한다."""
    import src.features.commercial_rag_001.support_policy.service as policy_svc

    class UtcClock(datetime):
        @classmethod
        def now(cls, tz=None):
            # 2026-11-02 00:00 KST == 2026-11-01 15:00 UTC
            return cls(2026, 11, 1, 15, 0, 0)

    monkeypatch.setattr(policy_svc, "datetime", UtcClock)
    status, is_open = check_policy_status("2026-01-01", "2026-11-01", None)
    if status != "closed" or is_open:
        pytest.fail(f"KST 2026-11-02 00:00 상당 시각인데 마감일 11-01 정책이 {status},{is_open}")
