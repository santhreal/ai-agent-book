"""Regression: --output with nested dirs must create parents before write."""
import json
from datetime import date

from demo import _write_output


def test_write_output_nested_parent(tmp_path):
    out = tmp_path / "reports" / "gold.json"
    _write_output(str(out), "gold", date(2024, 1, 1), 1, 1, [{"id": 1}])
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["mode"] == "gold"
    assert payload["passed"] == 1
    assert payload["total"] == 1


def test_write_output_bare_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _write_output("out.json", "gold", date(2024, 1, 1), 0, 1, [])
    assert (tmp_path / "out.json").exists()
