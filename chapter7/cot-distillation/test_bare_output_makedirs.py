"""Bare --raw_output / --sft_output filenames must not crash makedirs('')."""
import os
import tempfile

import pytest


def _makedirs_like_generate(path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)


def test_bare_filename_makedirs_ok(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _makedirs_like_generate("raw.jsonl")
    _makedirs_like_generate("sft.jsonl")
    open("raw.jsonl", "w").close()
    open("sft.jsonl", "w").close()
    assert (tmp_path / "raw.jsonl").exists()
    assert (tmp_path / "sft.jsonl").exists()


def test_nested_dirname_still_created(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _makedirs_like_generate("data/out/raw.jsonl")
    assert (tmp_path / "data" / "out").is_dir()


def test_pristine_bare_dirname_empty():
    """Document the failure mode: dirname('out.jsonl') is ''."""
    assert os.path.dirname("out.jsonl") == ""
