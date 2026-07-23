"""Regression: --output with nested dirs must create parents before write."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo import write_run_json


def test_write_run_json_nested_parent(tmp_path):
    out = tmp_path / "results" / "run.json"
    write_run_json(str(out), {"mode": "solver", "ok": True})
    assert out.exists()
    with open(out, encoding="utf-8") as f:
        payload = json.load(f)
    assert payload["ok"] is True
    assert payload["mode"] == "solver"


def test_write_run_json_bare_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_run_json("last_run.json", {"n": 1})
    assert (tmp_path / "last_run.json").exists()
