"""Regression: --output with nested dirs must create parents before write."""
import os
import sys
import types


def _stub():
    sys.modules.setdefault("openai", types.ModuleType("openai"))
    sys.modules["openai"].OpenAI = object
    agent = types.ModuleType("agent")

    class _Dummy:
        pass

    agent.MultimodalAgent = _Dummy
    agent.MultimodalContent = _Dummy
    sys.modules["agent"] = agent
    cfg = types.ModuleType("config")

    class ExtractionMode:
        pass

    cfg.ExtractionMode = ExtractionMode
    sys.modules["config"] = cfg


_stub()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo import open_output  # noqa: E402


def test_open_output_nested_parent(tmp_path):
    out = tmp_path / "out" / "transcript.txt"
    with open_output(str(out)) as fh:
        fh.write("ok\n")
    assert out.read_text(encoding="utf-8") == "ok\n"


def test_open_output_bare_filename(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with open_output("transcript.txt") as fh:
        fh.write("bare\n")
    assert (tmp_path / "transcript.txt").read_text(encoding="utf-8") == "bare\n"
