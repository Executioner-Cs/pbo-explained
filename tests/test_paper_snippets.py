"""Every code snippet in docs/paper.md must still be in the source files it names."""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = re.findall(r"```python\n# from: ([^\n]+)\n(.*?)```", (ROOT / "docs/paper.md").read_text(encoding="utf-8"), re.S)


def test_paper_has_snippets():
    assert len(BLOCKS) >= 5


@pytest.mark.parametrize("files, body", BLOCKS)
def test_snippet_lines_are_in_the_source(files, body):
    source = "\n".join((ROOT / f).read_text(encoding="utf-8") for f in files.split())
    for line in filter(None, (l.strip() for l in body.splitlines())):
        assert line in source, f"{line!r} not found in {files}"
