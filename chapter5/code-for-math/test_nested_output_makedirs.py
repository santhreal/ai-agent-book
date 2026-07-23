"""Nested --output paths must create parent directories before writing."""
import json
import os
from pathlib import Path
from types import SimpleNamespace

import demo as cfm


class _Resp:
    choices = [
        SimpleNamespace(
            message=SimpleNamespace(content="FINAL ANSWER: 1", tool_calls=None)
        )
    ]


class _Completions:
    @staticmethod
    def create(**kwargs):
        return _Resp()


class _Chat:
    completions = _Completions()


class _Client:
    chat = _Chat()


def test_nested_output_creates_parents(tmp_path, monkeypatch):
    problems = tmp_path / "empty.json"
    problems.write_text("[]", encoding="utf-8")
    out = tmp_path / "out" / "run1" / "result.json"
    monkeypatch.setattr(cfm, "build_client_and_model", lambda model_override=None: (_Client(), "fake"))
    # Empty problems still hits the output writer after the summary.
    # Need the empty-summary fix OR nonempty - use one problem to avoid depending on F-0748.
    problems.write_text(
        json.dumps([{"id": "1", "topic": "t", "question": "1+1?", "answer": 1}]),
        encoding="utf-8",
    )
    rc = cfm.main(["--problems", str(problems), "--mode", "cot", "--output", str(out)])
    assert rc == 0
    assert out.is_file()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["num_problems"] == 1
    assert data["mode"] == "cot"
