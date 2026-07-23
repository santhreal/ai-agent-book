"""Regression: --output with nested dirs must create parents before write."""
import json

from main import _save_output


def test_save_output_nested_parent(tmp_path):
    out = tmp_path / "reports" / "out.json"
    _save_output(str(out), {"question": "q", "answer": "a"})
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["question"] == "q"
    assert payload["answer"] == "a"


def test_save_output_bare_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _save_output("result.json", {"ok": True})
    assert (tmp_path / "result.json").exists()
