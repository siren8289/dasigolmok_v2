"""Gradle이 남긴 JUnit XML을 다시 읽어 실패 건수를 확인한다.

XML이 없으면 테스트를 실행한 것으로 보지 않는다.
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    folder = root / "back" / "build" / "test-results" / "test"
    files = sorted(folder.glob("TEST-*.xml")) if folder.exists() else []
    if not files:
        print("FAIL JUnit XML 없음. Gradle test가 결과를 남기지 않았다.")
        return 1
    tests = failures = errors = 0
    failed_names: list[str] = []
    for path in files:
        tree = ET.parse(path)
        node = tree.getroot()
        tests += int(node.attrib.get("tests", 0))
        failures += int(node.attrib.get("failures", 0))
        errors += int(node.attrib.get("errors", 0))
        for case in node.findall("testcase"):
            if case.find("failure") is not None or case.find("error") is not None:
                failed_names.append(f"{case.attrib.get('classname')}.{case.attrib.get('name')}")
    print(f"xml={len(files)} tests={tests} failures={failures} errors={errors}")
    if failed_names:
        print("failed=" + ",".join(failed_names[:20]))
    if tests == 0 or failures or errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
