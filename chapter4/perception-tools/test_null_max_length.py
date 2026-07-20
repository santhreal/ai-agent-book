"""Null optional max_length must use default 50000."""
import asyncio
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from filesystem_tools import read_file


def test_null_max_length_like_omit():
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write("hello world")
        path = f.name
    out = asyncio.run(read_file(path, max_length=None))
    payload = json.loads(out.text)
    assert payload["success"] is True
    assert payload["message"]["content"] == "hello world"
    assert payload["message"]["truncated"] is False
