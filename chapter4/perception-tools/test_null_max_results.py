"""Null optional max_results must use default 100."""
import asyncio
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from filesystem_tools import grep_search


def test_null_max_results_like_omit():
    d = tempfile.mkdtemp()
    Path(d, "a.txt").write_text("aaa\nbbb\n")
    out = asyncio.run(grep_search("a", d, max_results=None))
    payload = json.loads(out.text)
    assert payload["success"] is True
    assert "NoneType" not in str(payload)
