"""테스트가 관측한 증적을 pytest 결과에 싣기 위한 공용 기록."""

NOTES: dict[str, str] = {}


def clip(text: str, limit: int = 400) -> str:
    clean = " ".join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3] + "..."


def note(case_id: str, text: str) -> None:
    NOTES[case_id] = clip(text)


def normalize_status(pytest_outcome: str) -> str:
    """실행된 결과만 그대로 남긴다. skipped를 passed로 올리지 않는다."""
    if pytest_outcome == "passed":
        return "passed"
    if pytest_outcome == "failed":
        return "failed"
    if pytest_outcome == "skipped":
        return "skipped"
    raise ValueError(pytest_outcome)
