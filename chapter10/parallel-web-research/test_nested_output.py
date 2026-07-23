"""Regression: --output with nested dirs must create parents before write."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo import write_conclusion_json


def test_nested_output_creates_parent(tmp_path):
    out = tmp_path / "out" / "conclusion.json"
    write_conclusion_json(str(out), {"winner": "geo-journal", "acks": 3})
    assert out.exists()
    with open(out, encoding="utf-8") as f:
        payload = json.load(f)
    assert payload["winner"] == "geo-journal"
    assert payload["acks"] == 3


def test_bare_filename_output(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_conclusion_json("conclusion.json", {"ok": True})
    assert (tmp_path / "conclusion.json").exists()
