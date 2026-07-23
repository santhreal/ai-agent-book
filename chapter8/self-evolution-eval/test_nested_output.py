"""Regression: --output with nested dirs must create parents before write."""
import json
import os
import sys
from types import ModuleType

# demo imports openai via config; stub so the test runs offline.
sys.modules.setdefault("openai", ModuleType("openai"))
sys.modules["openai"].OpenAI = object

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo import write_reports_json


def test_nested_output_creates_parent(tmp_path):
    out = tmp_path / "reports" / "eval.json"
    write_reports_json(str(out), {"layers": ["L1"], "reports": [{"task_id": "t1"}]})
    assert out.exists()
    with open(out, encoding="utf-8") as f:
        payload = json.load(f)
    assert payload["layers"] == ["L1"]
    assert payload["reports"][0]["task_id"] == "t1"


def test_bare_filename_output(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_reports_json("eval.json", {"ok": True})
    assert (tmp_path / "eval.json").exists()
