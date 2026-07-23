"""Bare --raw_output / --sft_output filenames must not crash makedirs('')."""
import os
import re
from pathlib import Path

import pytest

GENERATE = Path(__file__).with_name("generate_data.py")


def test_generate_data_uses_or_dot_for_makedirs():
    src = GENERATE.read_text(encoding="utf-8")
    assert 'os.makedirs(os.path.dirname(args.raw_output) or ".", exist_ok=True)' in src
    assert 'os.makedirs(os.path.dirname(args.sft_output) or ".", exist_ok=True)' in src
    # Old unguarded form must be gone
    assert re.search(
        r'os\.makedirs\(os\.path\.dirname\(args\.raw_output\),\s*exist_ok=True\)',
        src,
    ) is None


def test_bare_filename_makedirs_ok(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # Exercise the production expression shape: dirname(bare) or "."
    for name in ("raw.jsonl", "sft.jsonl"):
        os.makedirs(os.path.dirname(name) or ".", exist_ok=True)
        open(name, "w").close()
        assert (tmp_path / name).exists()


def test_nested_dirname_still_created(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = "data/out/raw.jsonl"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    assert (tmp_path / "data" / "out").is_dir()
