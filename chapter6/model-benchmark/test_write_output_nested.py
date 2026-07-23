"""Nested --output paths must create parent directories before writing."""
import json
import os
from pathlib import Path

import pytest

# Stub openai so benchmark import succeeds offline.
import sys
import types

if "openai" not in sys.modules:
    _oai = types.ModuleType("openai")
    _oai.OpenAI = object
    sys.modules["openai"] = _oai

from demo import write_output  # noqa: E402
from benchmark import ProviderSummary  # noqa: E402


def test_write_output_creates_nested_parents(tmp_path):
    path = tmp_path / "out" / "run1" / "result.json"
    write_output(str(path), {"mode": "test"}, [])
    assert path.is_file()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["meta"]["mode"] == "test"
    assert data["results"] == []


def test_write_output_bare_filename_ok(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_output("result.json", {"mode": "bare"}, [])
    assert (tmp_path / "result.json").is_file()
