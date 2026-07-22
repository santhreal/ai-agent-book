"""Null revise from Manager decision must behave like empty list."""

import json
import sys
from pathlib import Path
from types import ModuleType

sys.path.insert(0, str(Path(__file__).parent))

try:
    import openai  # noqa: F401
except ImportError:
    sys.modules["openai"] = ModuleType("openai")
    sys.modules["openai"].OpenAI = object
try:
    import tiktoken  # noqa: F401
except ImportError:
    _tk = ModuleType("tiktoken")
    _enc = type("Enc", (), {"encode": lambda self, t: list(t or "")})
    _tk.encoding_for_model = lambda model: _enc()
    _tk.get_encoding = lambda name: _enc()
    sys.modules["tiktoken"] = _tk

import agents

CHAPTERS = {"Chapter 1: Intro": "# Chapter 1\nSome text."}


def _install_fake_llm():
    def fake_llm_chat(client, tracker, agent, messages, json_mode=False, note=""):
        tracker.record(agent, 10, 5, note)
        if agent == "Glossary":
            return json.dumps({"glossary": [{"en": "token", "zh": "词元"}]})
        if agent == "Proofreading":
            return json.dumps({
                "issues": [],
                "chapters_need_revision": [],
                "summary": "ok",
            })
        if agent == "Manager":
            return json.dumps({"revise": None, "reason": "none"})
        return "译文"

    agents.get_client = lambda: object()
    agents.llm_chat = fake_llm_chat


def test_orchestration_tolerates_null_revise(tmp_path):
    _install_fake_llm()
    result = agents.run_orchestration(
        CHAPTERS, str(tmp_path), enable_glossary=True, enable_proofreading=True)
    assert result["translations"]["Chapter 1: Intro"] == "译文"
    assert (tmp_path / "chapter1_zh.md").read_text(encoding="utf-8") == "译文"
