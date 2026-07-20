"""Null optional max_length must use default 500."""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from filesystem_tools import summarize_text


def test_null_max_length_like_omit():
    text = "Hello world. " * 80
    out = asyncio.run(summarize_text(text, max_length=None, use_llm=False))
    payload = json.loads(out.text)
    assert payload["success"] is True
    summary = payload["message"]["summary"]
    assert len(summary) <= 500 + 10  # allow trailing ". "
    assert payload["message"]["original_length"] == len(text)
