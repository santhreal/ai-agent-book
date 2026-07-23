"""Regression: save_checkpoint must create nested parent directories."""
import json

from runtime import AgentRuntime


def test_save_checkpoint_nested_parent(tmp_path):
    path = tmp_path / "nested" / "dir" / "ckpt.json"
    runtime = AgentRuntime(object(), "m")
    assert runtime.save_checkpoint(str(path)) == str(path)
    assert path.exists()
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert "trajectory" in payload
    assert "tasks" in payload


def test_save_checkpoint_bare_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runtime = AgentRuntime(object(), "m")
    runtime.save_checkpoint("ckpt.json")
    assert (tmp_path / "ckpt.json").exists()
