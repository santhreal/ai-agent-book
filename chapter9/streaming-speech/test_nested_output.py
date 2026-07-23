"""Regression: --output with nested dirs must create parents before write."""
import json
from pathlib import Path

import demo


def test_offline_nested_output(tmp_path):
    out = tmp_path / "nested" / "result.json"
    demo.main([
        "--offline",
        "--duration", "1",
        "--chunk-step", "1",
        "--sentence", "测",
        "--output", str(out),
    ])
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    assert payload


def test_offline_bare_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    demo.main([
        "--offline",
        "--duration", "1",
        "--chunk-step", "1",
        "--sentence", "测",
        "--output", "result.json",
    ])
    assert Path("result.json").exists()
